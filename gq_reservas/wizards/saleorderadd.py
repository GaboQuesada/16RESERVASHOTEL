
from odoo import fields, models, api
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
from datetime import datetime, timedelta
from datetime import date


class saleorderadd(models.TransientModel):
    _name = "saleorderadd"
    _description = "Sale order"
    name = fields.Char('Agregar linea')  # Cambia 'Nuevo Título del Wizard' al título deseado

    date_start = fields.Datetime(string='Fecha Llegada', required=True, tracking=True, default=datetime.today())
    date_end = fields.Datetime(string='Fecha Salida', required=True, tracking=True, default=datetime.today())
    days_count = fields.Integer(string='Días de estadía', compute='_compute_days_count')
    sale_order_id = fields.Many2one('sale.order', string='Orden de Venta')
    product_id = fields.Many2one('product.product', string='Product',  domain=lambda self: self._compute_product_domain())
    pricelist_id = fields.Many2one(
        'product.pricelist', string='Tarifas',
        help="Diferentes Tarifas.",
    )
    
    def _compute_product_domain(self):
        domain = [('es_habitacion', '=', True)]
        
        fechaini = self.date_start
        fechafin = self.date_end

        if self.date_start and self.date_end:
            overlapping_reservations = self.env['productreservas'].search(['|', '&', ('date_start', '<=', fechafin), ('date_end', '>=', fechaini), '&', ('date_start', '<=', fechaini), ('date_end', '>=', fechaini)])
            reserved_product_ids = overlapping_reservations.mapped('product_id.id')
            domain.append(('id', 'not in', reserved_product_ids))

        return domain
    
    @api.onchange('date_start', 'date_end')  
    def _onchange_values(self):
        
   
        
        fechaini = self.date_start
        fechafin = self.date_end
       
        # buscamos todas las reservas y comparamos las fechas 
        reservas = self.env['productreservas'].search(['|', '&', ('date_start', '<=', fechafin), ('date_end', '>=', fechaini), '&', ('date_start', '<=', fechaini), ('date_end', '>=', fechaini)])

       
        new_domain = [('es_habitacion', '=', True),('id', 'not in', reservas.mapped('product_id.id'))]  
        
        self.product_id = False  
        
        
        #self.env.user.notify_success("Se ha notificado a los aprobadores.")
        return {'domain': {'product_id': new_domain}}
    
    
    @api.depends('date_start', 'date_end')
    def _compute_days_count(self):
        for record in self:
            if record.date_start and record.date_end:
                start_date = fields.Datetime.from_string(record.date_start)
                end_date = fields.Datetime.from_string(record.date_end)
                days_count = (end_date - start_date).days + 1
                record.days_count = days_count
            else:
                record.days_count = 0
    
    def generarlineaUnica(self):
            
            nuevalinea = self.env['sale.order.line'].create({
                'product_id': self.product_id.id,
                'pricelist_id':self.pricelist_id.id,
                'name': 'Hospedaje',
                'product_uom_qty': float(self.days_count),
                'order_id': self.sale_order_id.id,
            })
            
            self.sale_order_id.order_line += nuevalinea
            
            self.env['productreservas'].create({
                'product_id': self.product_id.id,
                'date_start': self.date_start,
                'date_end':   self.date_end,
                'order_id':   self.sale_order_id.id,
                'line_id':    nuevalinea.id,
            })
            
            self._compute_product_domain()
            
   
        
        

    def agregarlinea(self):
         for record in self:
            if record.sale_order_id.state == 'draft':
                if record.product_id :
                    
                    
                    
                    if record.pricelist_id :
                    
                        self.generarlineaUnica()
                    
                    else: 
                        raise UserError('Necesitas definir una tarifa.') 
                    
                else: 
                    raise UserError('Debes seleccionar una habitación disponible.')   
           
                   
            else:
                raise UserError('Solo se pueden agregar líneas a presupuestos no confirmados.')
