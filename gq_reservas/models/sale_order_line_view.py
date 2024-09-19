# -*- coding: utf-8 -*-


from odoo import models, fields


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    es_alimentacion = fields.Boolean(default=False, string="Producto Alimentación")
    es_orderDeily   = fields.Boolean(default=False, string="Orden tipo Daily") 
    canonsinac      = fields.Char(string = "Boleta Sinac", related='order_id.canonsinac')
    dailyReport_id  = fields.Many2one('dailyreport', string='DailyReport') 
    
    
class SaleOrder(models.Model):
    _inherit = 'sale.order'  
    
    
    
    def action_confirm(self):
        
            res = super(SaleOrder, self).action_confirm()
        
            for lines in self.order_line:
                
           
                    if lines.product_template_id.es_alimentacion == True:
                        lines.es_alimentacion = True
                        
                        
                    if self.esdelily == True:
                        lines.es_orderDeily  = True
                        
                        
                        # buscar si ya existe un registro en esa fecha
                        # crearlo o actualizarlo 
                        
                        
                        registroexistente = self.env['dailyreport'].search([('name', '=', lines.checkin_date),], limit=1)
                        
                        if registroexistente:
                            #actualizar contador 
                            
                            registroexistente._sumaCantidad(lines.product_uom_qty)
                            lines.dailyReport_id = registroexistente.id
                            
                            
                            
                        else:
                            #crea el registro
                            nuevoregistro = self.env['dailyreport'].create({
                                          'name': lines.checkin_date,
                                          'contador': lines.product_uom_qty})
                            lines.dailyReport_id = nuevoregistro.id
                
               
                        
            return res
                        

                    
   