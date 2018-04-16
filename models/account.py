# -*- encoding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class AccountJournal(models.Model):
    _inherit = "account.journal"

    requiere_resolucion = fields.Boolean(string='Requiere Resolucion')
    resolucion_id = fields.Many2one('pos_sat.resolucion', string='Resolucion', readonly=True, related='sequence_id.resolucion_id')
    name_resolucion = fields.Char(string='Final', readonly=True, related='sequence_id.resolucion_id.name')
    serie_resolucion = fields.Char(string='Final', readonly=True, related='sequence_id.resolucion_id.serie')
    fecha_resolucion = fields.Date(string='Final', readonly=True, related='sequence_id.resolucion_id.fecha')
    fecha_vencimiento_resolucion = fields.Date(string='Final', readonly=True, related='sequence_id.resolucion_id.fecha_vencimiento')
    final_resolucion = fields.Integer(string='Final', readonly=True, related='sequence_id.resolucion_id.final')
    inicial_resolucion = fields.Integer(string='Inicial', readonly=True, related='sequence_id.resolucion_id.inicial')
    direccion_resolucion = fields.Char(string='Inicial', readonly=True, related='sequence_id.resolucion_id.direccion')
    ultimo_numero_factura = fields.Integer('Ultimo numero')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
