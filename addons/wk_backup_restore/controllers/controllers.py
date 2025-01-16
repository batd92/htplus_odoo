# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   License URL : <https://store.webkul.com/license.html/>
#
#################################################################################
import os
import logging
import datetime
import pytz
import shutil
import subprocess
import tempfile
import json

import odoo
from odoo import http, _
from odoo.http import request
from odoo.exceptions import AccessError, UserError
from odoo.tools.misc import exec_pg_environ, find_pg_tool

_logger = logging.getLogger(__name__)

class BackupController(http.Controller):


    @http.route('/backupfile/download', type='http', auth='user')
    def file_download(self, **kwargs):
        file_path = request.httprequest.args.get('path')   # The actual file path
        backup_location = request.httprequest.args.get('backup_location') or 'local'
        _logger.info(f"=====backup_location========= {backup_location} ====== file_path ====== {file_path}")
        try:
            # Read the file and return it as a response
            file_data = None
            with open(file_path, 'rb') as file:
                file_data = file.read()

            # Set the response headers for file download
            response = request.make_response(file_data)
            response.headers['Content-Disposition'] = f"attachment; filename={file_path.split('/')[-1]}" 
            response.mimetype = 'application/octet-stream'

            # Delete the remote backup file from Main Server
            if backup_location == 'remote':
                os.remove(file_path)

            return response
        except Exception as e:
            _logger.info(f"======= Backup File Download Error ======= {e} ========")
            raise UserError(e)
 


    @http.route('/saas/database/backup', type='http', auth="none", methods=['POST'], csrf=False)
    def db_backup(self, **kwargs):
        master_pwd = kwargs.get('master_pwd')
        dbname = kwargs.get('name')
        backup_format = kwargs.get('backup_format') or 'zip'
        response = None
        user = request.env['res.users'].sudo().browse([2]) 
        tz = pytz.timezone(user.tz) if user.tz else pytz.utc
        time_now = pytz.utc.localize(datetime.datetime.now()).astimezone(tz)
        ts = time_now.strftime("%m-%d-%Y-%H.%M.%S")
        filename = "%s_%s.%s" % (dbname, ts, backup_format)
        try:
            odoo.service.db.check_super(master_pwd)
            dump_stream = self.dump_db(dbname, None, backup_format)
            response = request.make_response(dump_stream)
            response.headers['Content-Disposition'] = f"attachment; filename={filename}"
            response.mimetype = 'application/octet-stream'
        except Exception as e:
            error = "Database backup error: %s" % (str(e) or repr(e))
            _logger.exception('Database.backup --- %r', error)
            response = request.make_response(error)
            response.mimetype = 'text/html'

        response.headers['Backup-Filename'] = filename
        response.headers['Backup-Time'] = time_now.strftime("%m-%d-%Y-%H:%M:%S")
        return response


    def dump_db_manifest(self, cr):
        pg_version = "%d.%d" % divmod(cr._obj.connection.server_version / 100, 100)
        cr.execute("SELECT name, latest_version FROM ir_module_module WHERE state = 'installed'")
        modules = dict(cr.fetchall())
        manifest = {
            'odoo_dump': '1',
            'db_name': cr.dbname,
            'version': odoo.release.version,
            'version_info': odoo.release.version_info,
            'major_version': odoo.release.major_version,
            'pg_version': pg_version,
            'modules': modules,
        }
        return manifest
    
    def dump_db(self, db_name, stream, backup_format='zip'):
        """Dump database `db` into file-like object `stream` if stream is None
        return a file object with the dump """

        _logger.info('DUMP DB: %s format %s', db_name, backup_format)

        cmd = [find_pg_tool('pg_dump'), '--no-owner', db_name]
        env = exec_pg_environ()

        if backup_format == 'zip':
            with tempfile.TemporaryDirectory() as dump_dir:
                filestore = odoo.tools.config.filestore(db_name)
                if os.path.exists(filestore):
                    shutil.copytree(filestore, os.path.join(dump_dir, 'filestore'))
                with open(os.path.join(dump_dir, 'manifest.json'), 'w') as fh:
                    db = odoo.sql_db.db_connect(db_name)
                    with db.cursor() as cr:
                        json.dump(self.dump_db_manifest(cr), fh, indent=4)
                cmd.insert(-1, '--file=' + os.path.join(dump_dir, 'dump.sql'))
                subprocess.run(cmd, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, check=True)
                if stream:
                    odoo.tools.osutil.zip_dir(dump_dir, stream, include_dir=False, fnct_sort=lambda file_name: file_name != 'dump.sql')
                else:
                    t=tempfile.TemporaryFile()
                    odoo.tools.osutil.zip_dir(dump_dir, t, include_dir=False, fnct_sort=lambda file_name: file_name != 'dump.sql')
                    t.seek(0)
                    return t
        else:
            cmd.insert(-1, '--format=c')
            stdout = subprocess.Popen(cmd, env=env, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE).stdout
            if stream:
                shutil.copyfileobj(stdout, stream)
            else:
                return stdout
