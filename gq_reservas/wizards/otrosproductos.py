
from odoo import fields, models, api
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
import itertools
from datetime import datetime, timedelta
from datetime import date


class otrosproductos(models.TransientModel):
    _name = "otrosproductos"
    _description = "Otros productos"
    
    elproducto = fields.Many2one('product.product', string='Product',  domain=lambda self: self._compute_otherproduct_domain())
    capacidad = fields.Float(string="Cantidad", default=1.0)
    wizard_id = fields.Many2one('saleorderaddlines', string='Wizard')
    
    
    def _compute_otherproduct_domain(self):
        domain = [('es_habitacion', '=', False)]
    
        return domain