from odoo import api, fields, models, tools
from datetime import datetime
from datetime import timedelta


class reservaconfig(models.Model):
      _name =  "reservaconfig"
      
      time_in  = fields.Float(string='Hora Check IN', required=True,  widget='time')
      time_out = fields.Float(string='Hora Check OUT', required=True, widget='time')
      es_actual = fields.Boolean(default=False, string="En uso")