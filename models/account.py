# -*- encoding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class AccountJournal(models.Model):
    _inherit = "account.journal"

    resolucion_id = fields.Many2one('pos_sat.resolucion', string='Resolucion', readonly=True, related='sequence_id.resolucion_id')

    # _columns = {
    #     'name': fields.char('Nombre', size=40, required=True),
    #     'resolucion': fields.related('sequence_id', 'resolucion', type='many2one', relation='pos_sat.resolucion', string='Resolucion', readonly=True),
    # }

# class account_move(osv.osv):
#     _inherit = "account.move"
#
#     def post(self, cr, uid, ids, context=None):
#         if context is None:
#             context = {}
#         invoice = context.get('invoice', False)
#         valid_moves = self.validate(cr, uid, ids, context)
#
#         if not valid_moves:
#             raise osv.except_osv(_('Error!'), _('You cannot validate a non-balanced entry.\nMake sure you have configured payment terms properly.\nThe latest payment term line should be of the "Balance" type.'))
#         obj_sequence = self.pool.get('ir.sequence')
#         for move in self.browse(cr, uid, valid_moves, context=context):
#             if move.name =='/':
#                 new_name = False
#                 journal = move.journal_id
#
#                 if invoice and invoice.internal_number:
#                     new_name = invoice.internal_number
#                 else:
#                     if journal.sequence_id:
#                         c = {'fiscalyear_id': move.period_id.fiscalyear_id.id}
#                         new_name = obj_sequence.next_by_id(cr, uid, journal.sequence_id.id, c)
#                         logging.warn(new_name)
#                         if journal.resolucion:
#                             r = re.compile('\d+')
#                             m = r.search(new_name)
#                             if m:
#                                 numero = m.group()
#                                 logging.warn(numero)
#                                 if int(numero) > journal.resolucion.final:
#                                     raise osv.except_osv(_('Error!'), _('Se ha llegado al final de la resolucion, ya no se puede continuar facturando.'))
#                             fecha = datetime.datetime.strptime(journal.resolucion.fecha, '%Y-%m-%d')
#                             hoy = datetime.datetime.today()
#                             anios = 0
#                             if hoy.year > fecha.year:
#                                 logging.warn(hoy.year)
#                                 if hoy.month >= fecha.month:
#                                     logging.warn(hoy.month)
#                                     if hoy.day >= fecha.day:
#                                         logging.warn(hoy.day)
#                                         anios = hoy.year - fecha.year
#                             logging.warn(anios)
#
#                             if journal.resolucion.primera and anios >= 1:
#                                 raise osv.except_osv(_('Error!'), _('La resolucion se ha vencido'))
#                             if not journal.resolucion.primera and anios >= 2:
#                                 raise osv.except_osv(_('Error!'), _('La resolucion se ha vencido'))
#
#                     else:
#                         raise osv.except_osv(_('Error!'), _('Please define a sequence on the journal.'))
#
#                 if new_name:
#                     self.write(cr, uid, [move.id], {'name':new_name})
#
#         cr.execute('UPDATE account_move '\
#                    'SET state=%s '\
#                    'WHERE id IN %s',
#                    ('posted', tuple(valid_moves),))
#         return True
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
