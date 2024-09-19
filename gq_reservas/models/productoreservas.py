from odoo import api, fields, models, tools


class ProductReservas(models.Model):

    _name  = "productreservas"
    
    
    
    name  = fields.Char(string='Reservación',    compute='_compute_name')
    date_start = fields.Datetime(string='Fecha-Llegada', required=True)
    date_end = fields.Datetime(string='Fecha-Salida', required=True)
    product_id = fields.Many2one('product.template', string='Habitación') 
    order_id = fields.Many2one('sale.order', string='Reserva') 
    line_id = fields.Many2one('sale.order.line', string='Reserva') 
    
    
    @api.depends('order_id')
    def _compute_name(self):
        for rec in self:
            nombrecama = rec.product_id.name or ''
            nombrereserva = rec.order_id.name or ''
            cliente = rec.order_id.partner_id.name or ''
            rec.name = f"{nombrecama} {nombrereserva} {cliente}"
            
         