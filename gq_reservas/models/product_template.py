from odoo import api, fields, models, tools


class ProductProduct(models.Model):

    _inherit = "product.template"
    
    es_habitacion   = fields.Boolean(help="Es habitación",string="Es habitación", default=False)
    es_alimentacion = fields.Boolean(default=False, string="Producto Alimentación")
    
    
    es_habilitada   = fields.Boolean(default=True, string="Habitación habilitada")
    capacidad       = fields.Float(string="Capacidad", default=1.0)
    
    numerocama       = fields.Float(string="Numero Cama")
    
    reservaproductolinea_ids  = fields.One2many('productreservas', 'product_id')
    