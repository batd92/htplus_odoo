# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   License URL : <https://store.webkul.com/license.html/>
#
#################################################################################

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from . lib import check_connectivity


import logging
import base64
import os

_logger = logging.getLogger(__name__)


class ProcessBackupDetail(models.Model):
    _name = 'backup.process.detail'
    _description = "Backup Process Details"
    _order = "id desc"

    name = fields.Char(string="Name")
    file_name = fields.Char(string="File Name")
    backup_process_id = fields.Many2one(string="Backup Process Id", comodel_name="backup.process")
    file_path = fields.Char(string="File Path")
    url = fields.Char(string="Url")
    backup_date_time = fields.Datetime(string="Backup Time")
    status = fields.Char(string="Status")
    message = fields.Char(string="Message")
    backup_location = fields.Selection(string="Backup Location", related="backup_process_id.backup_location", help="Server where the backup file will be stored.")

    def download_db_file(self):
        """
            Call by the download button over every backup detail record.
            Method download the zip file of backup, 
        """
        try:
            backup_file_path = None
            download_url = None
            if self.backup_location == 'local':
                backup_file_path = self.url
                download_url = f"/backupfile/download?path={backup_file_path}&backup_location=local"
            else:
                backup_copy_status = self.get_remote_backup_file()
                if backup_copy_status:
                    backup_file_path = self.backup_process_id.remote_server_id.temp_backup_dir+"/"+self.file_name
                    download_url = f"/backupfile/download?path={backup_file_path}&backup_location=remote"
                else:
                    raise UserError("Cannot download backup file from remote server. Follow logs for more details.")
                
            if self.status == "Success" and os.path.exists(backup_file_path):
                return  {
                            'type': 'ir.actions.act_url',
                            'url': download_url,
                            'target': 'new',
                        }
            else:
                raise UserError("Backup doesn't exists.")
        except Exception as e:
            raise UserError(f"Error Occured: {e}")
    
    
    def get_remote_backup_file(self):
        """
            Method to copy the backup file from the remote server to the main server

            Returns:
                [Boolean]: True in case file is successfully copied or False
        """
        try:
        
            host_server = self.backup_process_id.remote_server_id.get_server_details()
            temp_path = self.backup_process_id.remote_server_id.temp_backup_dir
            response = check_connectivity.ishostaccessible(host_server)
            
            if not response.get('status'):
                return False
            
            ssh_obj = response.get('result')
            sftp = ssh_obj.open_sftp()
            sftp.get(self.url, temp_path+'/'+self.file_name)
            sftp.close()
            _logger.info("======== Backup file successfully copied to the local server. ===========")
            return True
        except Exception as e:
            _logger.info(f"======= Exception while copying the backup file from the remote server ======= {e} ")
            return False
    
    def unlink_confirmation(self):
        for rec in self:
            if rec.status=="Success":
                msg = """ <span class="text-warning"><strong>Warning:</strong> After Deleting this record you will no longer be able to download the backup file associated with this record. However, after deletion the backup will still remain on server.
                        Are you sure you want to delete this backup record?<span>
                      """
                partial_id = self.env['backup.deletion.confirmation'].create({'backup_id': rec.id, 'message': msg})
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'Deletion Confirmation',
                    'view_mode': 'form',
                    'res_model': 'backup.deletion.confirmation',
                    'res_id': partial_id.id,
                    'target': 'new',
                }
            else:
                rec.unlink()
