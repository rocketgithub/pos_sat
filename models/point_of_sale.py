# -*- encoding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime

import logging

class PosSession(models.Model):
    _inherit = "pos.session"

    @api.model
    def create(self, vals):
        if vals.get('config_id', False):
            config = self.env['pos.config'].browse(vals['config_id'])
            if config.journal_id and config.journal_id.resolucion_id:
                if config.journal_id.ultimo_numero_factura > config.journal_id.resolucion_id.final:
                    raise ValidationError('Ya no quedan facturas en esta resolución, no puede abrir la sesión hasta ingresar una nueva resoución.')
                if config.journal_id.resolucion_id.fecha_vencimiento < datetime.today().strftime('%Y-%m-%d'):
                    raise ValidationError('La resolución se ha vencido, no puede abrir la sesión hasta ingresar una nueva resoución.')

        return super(PosSession, self).create(vals)

class PosOrder(models.Model):
    _inherit = "pos.order"

    numero_factura_impreso = fields.Integer('Numero Factura Impreso')

    @api.model
    def _order_fields(self, ui_order):
        fields = super(PosOrder, self)._order_fields(ui_order)
        if 'numero_factura_impreso' in ui_order:
            fields['numero_factura_impreso'] = ui_order['numero_factura_impreso']
        return fields

    @api.model
    def _process_order(self, pos_order):
        order = super(PosOrder, self)._process_order(pos_order)
        if order.numero_factura_impreso and order.numero_factura_impreso > order.sale_journal.ultimo_numero_factura:
            order.sale_journal.ultimo_numero_factura = order.numero_factura_impreso
        return order

    @api.model
    def _prepare_invoice(self):
        fields = super(PosOrder, self)._prepare_invoice()
        if self.numero_factura_impreso:
            fields['name'] = self.sale_journal.resolucion_id.serie+'-'+str(self.numero_factura_impreso)
        return fields
