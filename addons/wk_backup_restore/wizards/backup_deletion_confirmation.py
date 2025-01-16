# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   License URL : <https://store.webkul.com/license.html/>
# 
#################################################################################

from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)



class BackupDeletionConfirmation(models.TransientModel):
    _name = "backup.deletion.confirmation"
    _description = 'Backup Deletion Confirmation Wizard'
    
    backup_id = fields.Many2one(comodel_name="backup.process.detail", string="Backup Process Detail")
    message = fields.Html(string="Message")
    
    
    def action_delete_backup_detail(self):
        for rec in self:
            rec.backup_id.unlink()
    
