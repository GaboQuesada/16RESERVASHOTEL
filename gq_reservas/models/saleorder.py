# -*- coding: utf-8 -*-

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
from datetime import datetime, timedelta
from datetime import date
import pytz

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    

    esreserva  = fields.Boolean(string="Es una reserva")
    solicitadopor = fields.Many2one("res.partner" , string = 'Solicitado por' )
    canonsinac = fields.Char(string = "Boleta Sinac")
    
    #date_start = fields.Datetime(string='Fecha-Llegada', required=True, tracking=True, default=datetime.today())
    date_start = fields.Datetime(string='Fecha-Llegada', required=True, tracking=True, compute='_compute_date_start')
    #date_end = fields.Datetime(string='Fecha-Salida', required=True, tracking=True, default=datetime.today())
    date_end = fields.Datetime(string='Fecha-Salida', required=True, tracking=True, compute='_compute_date_end')
    days_count = fields.Integer(string='Días de estadía', compute='_compute_days_count')
    night_count = fields.Integer(string='Noches de estadía', compute='_compute_daysnight_count')
    totalADULTOS = fields.Integer(string='Total Adultos')
    totalGuias = fields.Integer(string='Total Guias')
    totalNINOS = fields.Integer(string='Total Niños')
    totalpersonas = fields.Integer(string='Total personas', compute='_compute_totalpersonas')
    mi_campo_time = fields.Char(string='Mi Campo Time', size=5, required=True,default='15:00')
    observacion = fields.Char(string = "Observación")
    
    esdelily             = fields.Boolean(string="Es Deily")
    esreservaconfirmada  = fields.Boolean(string="Confirmar Reserva")
    
    
    

    holamundowidget = fields.Text(string="a")
    
    payment_methods_id = fields.Many2one(
        comodel_name="payment.methods",
        string="Método de pago"
    )
  
    
    STATE_SELECTION = [('por_consumir', 'Por consumir'),
                       ('consumiendo', 'En consumo'),
                       ('consumido', 'Consumido'),
                       ('cancelado', 'Cancelado'),]

    estadoreserva = fields.Selection(STATE_SELECTION, string='Estado', default='por_consumir',tracking=True)
    
    TEMPLATE_SELECTION = [('original', 'Original'),('clientesimplificada', 'Cliente simplificada'),('clientedetallado', 'Cliente detallado')]

    plantillatosend = fields.Selection(TEMPLATE_SELECTION, string='Plantilla', default='clientesimplificada',tracking=True)
    politica = fields.Many2one("politicas" , string = 'Políticas' )
    
     
    @api.depends('totalNINOS','totalADULTOS','totalGuias')
    def _compute_totalpersonas(self):
      
        for record in self:
           
           record.totalpersonas = record.totalADULTOS + record.totalNINOS + record.totalGuias
           
            
    @api.depends('mi_campo_time')
    def _compute_date_start(self):
        tz = pytz.timezone('America/Costa_Rica')
        for record in self:
            # Obtener la hora de mi_campo_time
            if record.mi_campo_time:
                hour, minute = map(int, record.mi_campo_time.split(':'))
            else:
                hour, minute = 0, 0

            # Obtener la fecha actual
            current_date = fields.Datetime.now().date()

            # Crear un objeto de fecha y hora con la hora de mi_campo_time
            new_date_start = datetime(current_date.year, current_date.month, current_date.day, hour, minute)

            record.date_start = new_date_start
            
    @api.depends('date_start')
    def _compute_date_end(self):
     tz = pytz.timezone('America/Costa_Rica')
     for record in self:
        # Obtener la fecha calculada en date_start
        date_start = record.date_start

        if date_start and isinstance(date_start, datetime):
            # Asegurarse de que date_start sea una cadena en el formato "%Y-%m-%d %H:%M:%S"
            date_start_str = date_start.strftime("%Y-%m-%d %H:%M:%S")

            # Convertir date_start_str en un objeto datetime
            date_start_obj = datetime.strptime(date_start_str, "%Y-%m-%d %H:%M:%S")

            # Sumar un día a la fecha calculada en date_start
            date_end = date_start_obj + timedelta(days=1)

            record.date_end = date_end
    
    #producto
           
    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        for record in self:
            if record.date_start and record.date_end and record.date_start > record.date_end:
                raise ValidationError("La fecha de salida debe ser mayor a la fecha de llegada.")
            
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
    def _compute_daysnight_count(self):
        for record in self:
            if record.date_start and record.date_end:
                start_date = fields.Datetime.from_string(record.date_start)
                end_date = fields.Datetime.from_string(record.date_end)
                days_count = (end_date - start_date).days + 1
                record.night_count = days_count - 1
            else:
                record.night_count = 0
                

                
    @api.onchange('esreserva')
    def onchange_esreserva(self):
        if self.esreserva:
             #self.message_post(body='La orden se convirtio en reserva de hospedaje')
             self.message_notify(body='El checkbox se ha marcado')
        else:
             #self.message_post(body='La reserva de hospedaje, ahora solo es un presupuesto o pedido')
             self.message_notify(body='El checkbox se ha marcado')
             
             
    #modifica las list prices 
    
    def action_update_prices(self):
        self.ensure_one()

        self._recompute_prices()

        if self.pricelist_id:
            self.message_post(body=_(
                "Product prices have been recomputed according to pricelist %s.",
                self.pricelist_id._get_html_link(),
            ))   
            
    def _recompute_prices(self):
        lines_to_recompute = self._get_update_prices_lines()
        lines_to_recompute.invalidate_recordset(['pricelist_item_id'])
        lines_to_recompute._compute_price_unit()
        # Special case: we want to overwrite the existing discount on _recompute_prices call
        # i.e. to make sure the discount is correctly reset
        # if pricelist discount_policy is different than when the price was first computed.
        lines_to_recompute.discount = 0.0
        lines_to_recompute._compute_discount()
        self.show_update_pricelist = False     
        
    def _get_update_prices_lines(self):
        """ Hook to exclude specific lines which should not be updated based on price list recomputation """
        return self.order_line.filtered(lambda line: not line.display_type) 
            
    def create_wizard(self):   
        
        context = {
        'default_sale_order_id': self.id,
        'default_date_start': self.date_start,
        'default_date_end': self.date_end,
          }
        
        return {'type': 'ir.actions.act_window',
                'res_model' : 'saleorderadd',
                'view_mode':'form',
                'target':'new',
                'context':context}
        
    def create_wizardlines(self):   
        
        context = {
        'default_sale_order_id': self.id,
        'default_date_start': self.date_start,
        'default_date_end': self.date_end,
          }
        
        return {'type': 'ir.actions.act_window',
                'res_model' : 'saleorderaddlines',
                'view_mode':'form',
                'target':'new',
                'context':context}
        
    def action_quotation_send(self):
        
        self.ensure_one()
        self.order_line._validate_analytic_distribution()
        lang = self.env.context.get('lang')
        mail_template = self._find_mail_template()
        if mail_template and mail_template.lang:
            lang = mail_template._render_lang(self.ids)[self.id]
        ctx = {
            'default_model': 'sale.order',
            'default_res_id': self.id,
            'default_use_template': bool(mail_template),
            'default_template_id': mail_template.id if mail_template else None,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'default_email_layout_xmlid': 'mail.mail_notification_layout_with_responsible_signature',
            'proforma': self.env.context.get('proforma', False),
            'force_email': True,
            'model_description': self.with_context(lang=lang).type_name,
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }
        
    def _find_mail_template(self):
        
        self.ensure_one()
        if self.env.context.get('proforma') or self.state not in ('sale', 'done'):
            
            
                    return self.env.ref('sale.email_template_edi_sale', raise_if_not_found=False)
        else:
                    if self.esreserva == True:
                        return self._get_reservas_template()
                    else:
                        return self._get_confirmation_template()
                        
        
    def _get_confirmation_template(self):
        
        return self.env.ref('sale.mail_template_sale_confirmation', raise_if_not_found=False)
    
    def _get_reservas_template(self):
        
        return self.env.ref('reservas.mail_template_salereserva_confirmation', raise_if_not_found=False)