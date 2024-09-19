from odoo import api, fields, models, tools
from datetime import datetime
from datetime import timedelta


class reservaHotel(models.Model):

    _name =  "reservahotel"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    
    
    name  = fields.Char(string='# Reservación', required=True, copy=False, tracking=True, readonly=True, index=True, default=lambda self: ('New'))
    
     # GENERANDO EL NOMBRE DE LA PLANILLA
    @api.model
    def create(self, vals):
        if vals.get('name', ('# Reservación')) == ('# Reservación'):
            vals['name'] = self.env['ir.sequence'].next_by_code('reservahotel') or ('# Reservación')
        result = super(reservaHotel, self).create(vals)
        return result
    
    estado = fields.Selection( selection=[("abierto", "Abierta"),("enviada", "Enviada"),("generada", "Propuesta generada"), ], required=True, copy=False,default="abierto", tracking=True)
    
    
    @api.model
    def _get_checkin_date(self):
        self._context.get("tz") or self.env.user.partner_id.tz or "UTC"
        fechaHoraInicio = fields.Datetime.context_timestamp(self, fields.Datetime.now())
        return fields.Datetime.to_string(fechaHoraInicio)

    @api.model
    def _get_checkout_date(self):
        self._context.get("tz") or self.env.user.partner_id.tz or "UTC"
        fechaHoraFin = fields.Datetime.context_timestamp(
            self, fields.Datetime.now() + timedelta(days=1)
        )
        return fields.Datetime.to_string(fechaHoraFin)
    
    
    fechaHoraInicio = fields.Datetime(
        "Fecha Hora Check IN",
        required=True,
        readonly=True,
        estado={"abierto": [("readonly", False)]},
        default=_get_checkin_date,
        tracking=True
    )
    
    fechaHoraFin = fields.Datetime(
        "Fecha Hora Check OUT",
        required=True,
        readonly=True,
        estado={"abierto": [("readonly", False)]},
        default=_get_checkout_date,
        tracking=True
    )
    
    diasdeestadia  = fields.Float(string="Días de alojamiento", tracking=True, compute='_compute_dias_alojamiento') 
    
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
    
    facturara     = fields.Many2one('res.partner', string='Facturar a', tracking=True )
    encargado     = fields.Many2one('res.partner', string='Encargado general', tracking=True )
    touroperador  = fields.Many2one('res.partner', string='Tour Operador', tracking=True )
    
    reservahotellinea_ids  = fields.One2many('reservahotellinea', 'reservahotel_id')
    
    tarifageneral  = fields.Many2one('product.pricelist', string='Tarifa', tracking=True )