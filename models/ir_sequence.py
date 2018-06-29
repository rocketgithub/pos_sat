# -*- encoding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import logging

class IrSequence(models.Model):
    _inherit = "ir.sequence"

    resolucion_id = fields.Many2one('pos_sat.resolucion', string='Resolucion')

    @api.onchange('resolucion_id')
    def onchange_resolucion(self):
        if self.resolucion_id:
            self.prefix = self.resolucion_id.serie+'-'
            self.suffix = ''
            self.padding = 8
            self.number_increment = 1
            self.number_next_actual = self.resolucion_id.inicial
            self.use_date_range = False

    def create(self, vals):
        if vals.get('resolucion_id', False):
            r = self.env['pos_sat.resolucion'].browse(vals['resolucion_id'])
            vals.update({
                'prefix': r.serie+'-',
                'suffix': '',
                'padding': 8,
                'number_increment': 1,
                'number_next_actual': r.inicial,
                'use_date_range': False,
            })
        for diario in self.env['account.journal'].search([('sequence_id','=',self.id)]):
            diario.ultimo_numero_factura = r.inicial - 1
        return super(IrSequence, self).create(vals)

    def write(self, vals):
        if vals.get('resolucion_id', False):
            if vals['resolucion_id'] != self.resolucion_id.id:
                r = self.env['pos_sat.resolucion'].browse(vals['resolucion_id'])
                vals.update({
                    'prefix': r.serie+'-',
                    'suffix': '',
                    'padding': 8,
                    'number_increment': 1,
                    'number_next_actual': r.inicial,
                    'use_date_range': False
                })
                for diario in self.env['account.journal'].search([('sequence_id','=',self.id)]):
                    diario.ultimo_numero_factura = r.inicial - 1
        return super(IrSequence, self).write(vals)
