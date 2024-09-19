
from odoo import fields, models, api
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
import itertools
from datetime import datetime, timedelta
from datetime import date


class saleorderaddlines(models.TransientModel):
    _name = "saleorderaddlines"
    _description = "Sale order"
    name = fields.Char('Agregar lineas')  # Cambia 'Nuevo Título del Wizard' al título deseado
    

    date_start = fields.Datetime(string='Fecha Llegada', required=True, tracking=True, default=datetime.today())
    date_end = fields.Datetime(string='Fecha Salida', required=True, tracking=True, default=datetime.today())
    days_count = fields.Integer(string='Días de estadía', compute='_compute_days_count')
    night_count = fields.Integer(string='Noches de estadía', compute='_compute_night_count')
    sale_order_id = fields.Many2one('sale.order', string='Orden de Venta')
    product_id = fields.Many2one('product.product', string='Product',  domain=lambda self: self._compute_product_domain())
    detalle_ids = fields.One2many('otrosproductos', 'wizard_id', string='Detalles')
    pricelist_id = fields.Many2one('product.pricelist', string='Tarifas',help="Diferentes Tarifas.")
    totalhabitaciones = fields.Integer(string='Total habitación')
    
    def _compute_product_domain(self):
        domain = [('es_habitacion', '=', True)]
        
        fechaini = self.date_start
        fechafin = self.date_end

        if self.date_start and self.date_end:
            overlapping_reservations = self.env['productreservas'].search(['|', '&', ('date_start', '<=', fechafin), ('date_end', '>=', fechaini), '&', ('date_start', '<=', fechaini), ('date_end', '>=', fechaini)])
            reserved_product_ids = overlapping_reservations.mapped('product_id.id')
            domain.append(('id', 'not in', reserved_product_ids))

        return domain
    
    def _compute_otherproduct_domain(self):
        domain = [('es_habitacion', '=', False)]
    
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
                
                
    @api.depends('date_start', 'date_end')
    def _compute_night_count(self):
        for record in self:
            if record.date_start and record.date_end:
                start_date = fields.Datetime.from_string(record.date_start)
                end_date = fields.Datetime.from_string(record.date_end)
                days_count = (end_date - start_date).days + 1
                record.night_count = days_count  - 1
            else:
                record.night_count = 0
    
    def generarlineas(self):
        
        
        #obtener el numero de habitaciones disponibles
            
        domain = [('es_habitacion', '=', True)]
        
        fechaini = self.date_start
        fechafin = self.date_end

        if self.date_start and self.date_end:
            overlapping_reservations = self.env['productreservas'].search(['|', '&', ('date_start', '<=', fechafin), ('date_end', '>=', fechaini), '&', ('date_start', '<=', fechaini), ('date_end', '>=', fechaini)])
            reserved_product_ids = overlapping_reservations.mapped('product_id.id')
            domain.append(('id', 'not in', reserved_product_ids))

    
        record_count = self.env['product.product'].search_count(domain)
        if record_count >= self.totalhabitaciones:
            records = self.env['product.product'].search(domain)
            
            for record in itertools.islice(records, self.totalhabitaciones):
            
                    
                    #recoger lo que hay en el manytomany y lo agrega 
                    
                    #for recordotros in self.otherproduct_ids:detalle_ids
                    
                        
                        
                    # Realiza alguna acción con cada registro, por ejemplo, imprimirlo
                    nuevalinea = self.env['sale.order.line'].create({
                    'checkin_date':self.date_start,
                    'checkout_date':self.date_end,
                    'pricelist_id':self.pricelist_id.id,
                    'product_id': record.id,
                    'name': 'Hospedaje',
                    'product_uom_qty': float(self.night_count),
                    'order_id': self.sale_order_id.id,
                    })
                
                    self.sale_order_id.order_line += nuevalinea
                
                    self.env['productreservas'].create({
                    'product_id': record.id,
                    'date_start': self.date_start,
                    'date_end':   self.date_end,
                    'order_id':   self.sale_order_id.id,
                    'line_id':    nuevalinea.id,
                    })
                    
                    
                    for recordotros in self.detalle_ids:
                        
                        night_count = self.night_count
                        checkin_date = self.date_start
    
    
                        for night in range(night_count):
                            
                            
                            
                            nuevalinea = self.env['sale.order.line'].create({
                                'checkin_date': checkin_date,
                                'checkout_date':checkin_date,
                                'pricelist_id': self.pricelist_id.id,
                                'product_id': recordotros.elproducto.id,
                                'name': recordotros.elproducto.name,
                                'product_uom_qty': 1,
                                'order_id': self.sale_order_id.id,
                            })
                            checkin_date = checkin_date + timedelta(days=1)

                            self.sale_order_id.order_line += nuevalinea
                            
        else:
            raise UserError('Cantidad no disponible para demanda.')
       
            
   
        
        

    def agregarlineas(self):
         for record in self:
           
                if record.totalhabitaciones or record.totalhabitaciones <= 0:
                    
                    if self.pricelist_id:
                    
                        self.generarlineas()
                    
                    else: 
                        raise UserError('Necesitas definir una tarifa.') 
                    
                else: 
                    raise UserError('Indica la cantidad de habitaciones.')   
           
                   
       