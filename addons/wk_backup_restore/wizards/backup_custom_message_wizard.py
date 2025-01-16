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


class BackupCustomMessage(models.TransientModel):
    _name = "backup.custom.message.wizard"
    _description = 'Backup Custom Message Wizard'
    
    message = fields.Html(string="Message", readonly=True)