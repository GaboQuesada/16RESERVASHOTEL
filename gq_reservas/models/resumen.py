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

class resumen(models.Model):
    
     _name = 'resumen'
     _description = 'resumen'
     
     
     name = fields.Char("Reservation Summary", default="Reservations Summary")
     date_from = fields.Datetime(default=lambda self: fields.Date.today())
     date_to   = fields.Datetime(default=lambda self: fields.Date.today() + relativedelta(days=30),)
     summary_header = fields.Text()
     room_summary = fields.Text()
     
     @api.onchange("date_from", "date_to")  # noqa C901 (function is too complex)
     def get_room_summary(self):  # noqa C901 (function is too complex)
        res = {}
        all_detail = []
        all_room_detail = []
        room_detail = {}
        summary_header_list = ["Rooms"]
        summary_header_list.append("01/02/23")
        main_header = []
        all_room_detail.append(room_detail)
        main_header.append({"header": summary_header_list})
        self.summary_header = str(main_header)
        self.room_summary = str(all_room_detail)
        return res