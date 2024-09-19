from odoo import api, fields, models, tools
from datetime import datetime
from datetime import timedelta


class reservaHotelLinea(models.Model):
    _name =  "reservahotellinea"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    reservahotel_id = fields.Many2one('reservahotel',string='Reserva')
    huesped  = fields.Many2one('res.partner', string='Huésped', tracking=True )
    tarifa  = fields.Many2one('product.pricelist', string='Tarifa', tracking=True )
    fechaHoraInicio = fields.Datetime("Fecha Hora Check IN",required=True,tracking=True)
    fechaHoraFin = fields.Datetime("Fecha Hora Check OUT",required=True,tracking=True)
    diasdeestadia  = fields.Float(string="Días de alojamiento", tracking=True, compute='_compute_dias_alojamiento') 
    product_id = fields.Many2one(
        'product.product', string='Habitación', domain="[('es_habitacion', '=', True)]",
        change_default=True, ondelete='restrict', check_company=True, create=False) 
    
    @api.depends('fechaHoraInicio', 'fechaHoraFin')
    def _compute_dias_alojamiento(self):
        for rec in self:
            if rec.fechaHoraInicio and rec.fechaHoraFin:
                fecha_inicio = fields.Datetime.from_string(rec.fechaHoraInicio)
                fecha_fin = fields.Datetime.from_string(rec.fechaHoraFin)
                diferencia = fecha_fin - fecha_inicio
                rec.diasdeestadia = diferencia.days + diferencia.seconds / 86400  # Convertir segundos a días
            else:
                rec.diasdeestadia = 0.0
                
    @api.model
    def create(self, vals):
        
        # setiamos las fechas segun los dias de la reserva 
        
        self.fechaHoraInicio = self.reservahotel_id.fechaHoraInicio
        self.fechaHoraFin    = self.reservahotel_id.fechaHoraFin
        self.diasdeestadia    = self.reservahotel_id.diasdeestadia
        self.tarifa    = self.reservahotel_id.tarifa
        
        
        
        return
                
    
    
   