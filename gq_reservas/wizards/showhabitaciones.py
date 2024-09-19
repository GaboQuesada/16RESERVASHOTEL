
from odoo import fields, models, api
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
from datetime import datetime, timedelta
from datetime import date


class showhabitaciones(models.TransientModel):
    _name = "showhabitaciones"
    _description = "Show Habitaciones"
    
    lineascamas_id = fields.One2many('lineahabitacion', 'habitacion_id', string='Cama')
    
    
    
class lineahabitacion(models.TransientModel):
    _name = "lineahabitacion"
    _description = "Lineas Habitaciones"
    

    
    habitacion_id = fields.Many2one('showhabitaciones',string='habitacion')
    product_id = fields.Many2one('product.product', string='Product')
    date_1 = fields.Char(string='1')
    date_2 = fields.Char(string='2')
    date_3 = fields.Char(string='3')
    date_4 = fields.Char(string='4')
    date_5 = fields.Char(string='5')
    date_6 = fields.Char(string='6')
    date_7 = fields.Char(string='7')
    date_8 = fields.Char(string='8')
    date_9 = fields.Char(string='9')
    date_10 = fields.Char(string='10')
    date_11 = fields.Char(string='11')
    date_12 = fields.Char(string='12')
    date_13 = fields.Char(string='13')
    date_14 = fields.Char(string='14')
    date_15 = fields.Char(string='15')
    date_16 = fields.Char(string='16')
    date_17 = fields.Char(string='17')
    date_18 = fields.Char(string='18')
    date_19 = fields.Char(string='19')
    date_20 = fields.Char(string='20')
    date_21 = fields.Char(string='21')
    date_22 = fields.Char(string='22')
    date_23 = fields.Char(string='23')
    date_24 = fields.Char(string='24')
    date_25 = fields.Char(string='25')
    date_26 = fields.Char(string='26')
    date_27 = fields.Char(string='27')
    date_28 = fields.Char(string='28')
    date_29 = fields.Char(string='29')
    date_30 = fields.Char(string='30')
    date_31 = fields.Char(string='31')
    
    @api.model
    def create():
        
        
        field = self.env['ir.model.fields'].search([
            ('model', '=', 'lineahabitacion'),
            ('name', '=', 'date_1'),
        ])
        nuevo_texto = 'hola'
        
        if field:
            field.write({
                'field_description': nuevo_texto,
            })
        
        return True
        

    
    
    