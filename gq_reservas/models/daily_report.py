from odoo import api, fields, models, tools


class DailyReport(models.Model):
    _name  = "dailyreport"
    
    
    
    name  =  fields.Datetime("Fecha")
    contador  = fields.Float(string="Cantidad", default=0.0) 
    saleOrderLines_ids   = fields.One2many('sale.order.line','dailyReport_id',string='Sale Order Lines')
   
    
    

    def _sumaCantidad(self, nuevaCantidad):
        for rec in self:
            rec.contador = rec.contador + nuevaCantidad
           
            
         