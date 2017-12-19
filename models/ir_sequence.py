# -*- encoding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class IrSequence(models.Model):
    _inherit = "ir.sequence"

    valido = fields.Boolean('Valido', readonly=True)
    resolucion_id = fields.Many2one('pos_sat.resolucion', string='Resolucion')

    # def onchange_resolucion(self, cr, uid, ids, resolucion=False, context=None):
    #     if not resolucion:
    #         return {'value': {}}
    #     else:
    #         r = self.pool.get('pos_sat.resolucion').browse(cr, uid, resolucion, context=context)
    #         return {
    #             'value': {
    #                 'prefix': r.serie+'-',
    #                 'suffix': '',
    #                 'padding': 8,
    #                 'number_increment': 1,
    #                 'number_next_actual': r.inicial
    #             }
    #         }
    #
    # def create(self, cr, uid, vals, context=None):
    #     if 'resolucion' in vals and vals['resolucion']:
    #         r = self.pool.get('pos_sat.resolucion').browse(cr, uid, vals['resolucion'], context=context)
    #         vals.update({
    #             'prefix': r.serie+'-',
    #             'suffix': '',
    #             'padding': 8,
    #             'number_increment': 1,
    #             'number_next_actual': r.inicial,
    #             'valido': True
    #         })
    #     return super(ir_sequence, self).create(cr, uid, vals, context)
    #
    # def write(self, cr, uid, ids, vals, context=None):
    #     if 'resolucion' in vals and vals['resolucion']:
    #         r = self.pool.get('pos_sat.resolucion').browse(cr, uid, vals['resolucion'], context=context)
    #         vals.update({
    #             'prefix': r.serie+'-',
    #             'suffix': '',
    #             'padding': 8,
    #             'number_increment': 1,
    #             'number_next_actual': r.inicial,
    #             'valido': True
    #         })
    #     return super(ir_sequence, self).write(cr, uid, ids, vals, context)
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
