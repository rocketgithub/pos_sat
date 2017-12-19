# -*- encoding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class IrSequence(models.Model):
    _inherit = "ir.sequence"

    valido = fields.Boolean('Valido', readonly=True)
    resolucion_id = fields.Many2one('pos_sat.resolucion', string='Resolucion')

    @api.onchange('resolucion_id')
    def onchange_resolucion(self):
        if self.resolucion_id:
            self.prefix = self.resolucion_id.serie+'-'
            self.suffix = ''
            self.padding = 8
            self.number_increment = 1
            self.number_next_actual = self.resolucion_id.inicial

    def create(self, vals):
        if vals.get('resolucion_id', False):
            r = self.env['pos_sat.resolucion'].browse(cr, uid, vals['resolucion_id'], context=context)
            vals.update({
                'prefix': r.serie+'-',
                'suffix': '',
                'padding': 8,
                'number_increment': 1,
                'number_next_actual': r.inicial,
                'valido': True
            })
        return super(IrSequence, self).create(vals)

    def write(self, vals):
        if vals.get('resolucion_id', False):
            r = self.env['pos_sat.resolucion'].browse(cr, uid, vals['resolucion_id'], context=context)
            vals.update({
                'prefix': r.serie+'-',
                'suffix': '',
                'padding': 8,
                'number_increment': 1,
                'number_next_actual': r.inicial,
                'valido': True
            })
        return super(IrSequence, self).write(vals)
