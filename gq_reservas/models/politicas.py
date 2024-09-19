# -*- coding: utf-8 -*-

import logging
from odoo import _, api, fields, models
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from odoo.http import request
import locale
import base64
import io
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as dt

_logger = logging.getLogger(__name__)
try:
    import pytz
except (ImportError, IOError) as err:
    _logger.debug(err)

class politicas(models.Model):
    
     _name = 'politicas'
     _description = 'politicas'
     
     
     name = fields.Char("Nombre")
     terminos = fields.Html('Términos y condiciones ')