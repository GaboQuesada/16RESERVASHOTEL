# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
import time
from datetime import datetime, timedelta
from datetime import date
from odoo.exceptions import UserError, ValidationError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.misc import get_lang


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    checkin_date = fields.Datetime("Check In")
    checkout_date = fields.Datetime("Check Out")
    pricelist_id = fields.Many2one('product.pricelist', string='Tarifas',help="Diferentes Tarifas.",)
    
 
    
    
    @api.model
    def unlink(self):
        # Realizar acciones personalizadas antes de eliminar la línea
        
        # Eliminar registros de product.reservas donde el ID de la línea de orden de venta coincida
        self.env['productreservas'].search([('line_id', '=', self.id)]).unlink()
        
        

        # Llamar al método original para eliminar la línea
        result = super(SaleOrderLine, self).unlink()

        self.env.user.notify_success("Eliminada la reserva.")

        return result
    
    
    #PARA CAMBIAR EL PRICELIST
    
    price_unit = fields.Float(
        string="Unit Price",
        compute='_compute_price_unit',
        digits='Product Price',
        store=True, readonly=False, required=True, precompute=True)
    
    pricelist_item_id = fields.Many2one(
        comodel_name='product.pricelist.item',
        compute='_compute_pricelist_item_id')
    
    
    
    @api.onchange('pricelist_id')
    def _cambialatarifaporlinea(self):
        
        for linea in self:
            
            lines_to_recompute = linea
            lines_to_recompute.invalidate_recordset(['pricelist_item_id'])
            lines_to_recompute._compute_price_unit()
            # Special case: we want to overwrite the existing discount on _recompute_prices call
            # i.e. to make sure the discount is correctly reset
            # if pricelist discount_policy is different than when the price was first computed.
            lines_to_recompute.discount = 0.0
            lines_to_recompute._compute_discount()
 
            
    
    
    @api.depends('product_id', 'product_uom', 'product_uom_qty')
    def _compute_price_unit(self):
        for line in self:
            # check if there is already invoiced amount. if so, the price shouldn't change as it might have been
            # manually edited
            if line.qty_invoiced > 0 or (line.product_id.expense_policy == 'cost' and line.is_expense):
                continue
            if not line.product_uom or not line.product_id:
                line.price_unit = 0.0
            else:
                line = line.with_company(line.company_id)
                price = line._get_display_price()
                line.price_unit = line.product_id._get_tax_included_unit_price_from_price(
                    price,
                    line.currency_id or line.order_id.currency_id,
                    product_taxes=line.product_id.taxes_id.filtered(
                        lambda tax: tax.company_id == line.env.company
                    ),
                    fiscal_position=line.order_id.fiscal_position_id,
                )
                
    def _get_display_price(self):
        """Compute the displayed unit price for a given line.

        Overridden in custom flows:
        * where the price is not specified by the pricelist
        * where the discount is not specified by the pricelist

        Note: self.ensure_one()
        """
        self.ensure_one()

        pricelist_price = self._get_pricelist_price()

        if self.order_id.pricelist_id.discount_policy == 'with_discount':
            return pricelist_price

        if not self.pricelist_item_id:
            # No pricelist rule found => no discount from pricelist
            return pricelist_price

        base_price = self._get_pricelist_price_before_discount()

        # negative discounts (= surcharge) are included in the display price
        return max(base_price, pricelist_price)
                
                
    def _get_pricelist_price(self):
        """Compute the price given by the pricelist for the given line information.

        :return: the product sales price in the order currency (without taxes)
        :rtype: float
        """
        self.ensure_one()
        self.product_id.ensure_one()

        pricelist_rule = self.pricelist_item_id
        order_date = self.order_id.date_order or fields.Date.today()
        product = self.product_id.with_context(**self._get_product_price_context())
        qty = self.product_uom_qty or 1.0
        uom = self.product_uom or self.product_id.uom_id
        currency = self.currency_id or self.order_id.company_id.currency_id

        price = pricelist_rule._compute_price(
            product, qty, uom, order_date, currency=currency)

        return price
    
    
    #este es el que debo cambiar para que tome el pricelist_id de la linea de existir
    @api.depends('product_id', 'product_uom', 'product_uom_qty')
    def _compute_pricelist_item_id(self):
        for line in self:
            if not line.product_id or line.display_type or not line.order_id.pricelist_id:
                line.pricelist_item_id = False
            else:
                
                if line.pricelist_id:
                
                    line.pricelist_item_id = line.pricelist_id._get_product_rule(
                        line.product_id,
                        line.product_uom_qty or 1.0,
                        uom=line.product_uom,
                        date=line.order_id.date_order,
                    )
                
                else:
                    
                    line.pricelist_item_id = line.order_id.pricelist_id._get_product_rule(
                        line.product_id,
                        line.product_uom_qty or 1.0,
                        uom=line.product_uom,
                        date=line.order_id.date_order,
                    )
    
    
    


    
    