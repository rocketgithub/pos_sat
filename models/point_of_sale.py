# -*- encoding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class PosSession(models.Model):
    _inherit = "pos.session"

    @api.model
    def create(self, vals):
        if vals.get('config_id', False):
            config = self.env['pos.config'].browse(vals['config_id'])
            if config.journal_id and config.journal_id.resolucion_id:
                if config.journal_id.sequence_id.number_next_actual > config.journal_id.resolucion_id.final:
                    raise ValidationError('Ya no quedan facturas en esta resolución, no puede abrir la sesión hasta ingresar una nueva resoución.')
        return super(PosSession, self).create(vals)

# class pos_order(osv.osv):
#     _inherit = "pos.order"
#
#     def _serie(self, cr, uid, ids, field_name, arg, context):
#         result = {}
#         for o in self.browse(cr, uid, ids, context=context):
#             if o.invoice_id and o.invoice_id.number:
#                 result[o.id] = o.invoice_id.number.split("-")[0]
#             else:
#                 result[o.id] = ''
#         return result
#
#     def _numero(self, cr, uid, ids, field_name, arg, context):
#         result = {}
#         for o in self.browse(cr, uid, ids, context=context):
#             if o.invoice_id and o.invoice_id.number:
#                 result[o.id] = o.invoice_id.number.split("-").pop()
#             else:
#                 result[o.id] = ''
#         return result
#
#     def _estado(self, cr, uid, ids, field_name, arg, context):
#         result = {}
#         estados = {
#             'draft': 'Borrador',
#             'cancel': 'Anulado',
#             'paid': 'Emitido',
#             'done': 'Emitido',
#             'invoiced': 'Emitido'
#         }
#         for o in self.browse(cr, uid, ids, context=context):
#             result[o.id] = estados[o.state]
#         return result
#
#     _columns = {
#         'impreso': fields.integer('Impreso', required=True),
#         'serie': fields.function(_serie, type='char', method=True, string='Serie'),
#         'numero': fields.function(_numero, type='char', method=True, string='Numero'),
#         'estado': fields.function(_estado, type='char', method=True, string='Estado'),
#     }
#
#     _defaults = {
#         'impreso': 0,
#     }
#
#     def onchange_session_id(self, cr, uid, ids, session_id=False, context=None):
#         if not session_id:
#             return {'value': {}}
#         sesion = self.pool.get('pos.session').browse(cr, uid, session_id, context=context)
#         diario = sesion.config_id.journal_id
#         if not diario.resolucion:
#             return {
#                 'value': {'session_id':False},
#                 'warning':{'title':'Error', 'message':'No existe resolucion para el punto de venta'},
#             }
#         if diario.resolucion:
#             if int(diario.sequence_id.number_next_actual) > diario.resolucion.final*0.75:
#                 return {
#                     'warning':{'title':'Advertencia', 'message':'Se estan por acabar los numeros de factura en la resolucion.'}
#                 }
#         return {'value': {}}
#
#     def action_paid(self, cr, uid, ids, context=None):
#         self.write(cr, uid, ids, {'state': 'paid'}, context=context)
#         self.create_picking(cr, uid, ids, context=context)
#         res = self.action_invoice(cr, uid, ids, context=context)
#         inv_id = res['res_id']
#         self.pool.get('account.invoice').action_date_assign(cr, uid, [inv_id])
#         self.pool.get('account.invoice').action_move_create(cr, uid, [inv_id])
#         self.pool.get('account.invoice').action_number(cr, uid, [inv_id])
#         self.pool.get('account.invoice').invoice_validate(cr, uid, [inv_id])
#         return True
#
# class pos_session(osv.osv):
#     _inherit = "pos.session"
#     def wkf_action_close(self, cr, uid, ids, context=None):
#         res = super(pos_session, self).wkf_action_close(cr, uid, ids, context=context)
#         pedidos = self.pool.get('pos.order').search(cr, uid, [('session_id','in',ids),('impreso','=',0)])
#         if len(pedidos) > 0:
#             raise osv.except_osv('Error!', "No se puede cerrar las cajas por que existen facturas pendientes de imprimir")
#
# class pos_make_payment(osv.osv):
#     _inherit = "pos.make.payment"
#     def check(self, cr, uid, ids, context=None):
#         """Check the order:
#         if the order is not paid: continue payment,
#         if the order is paid print ticket.
#         """
#         context = context or {}
#         order_obj = self.pool.get('pos.order')
#         active_id = context and context.get('active_id', False)
#
#         order = order_obj.browse(cr, uid, active_id, context=context)
#         amount = order.amount_total - order.amount_paid
#         data = self.read(cr, uid, ids, context=context)[0]
#         # this is probably a problem of osv_memory as it's not compatible with normal OSV's
#         data['journal'] = data['journal_id'][0]
#
#         if amount != 0.0:
#             order_obj.add_payment(cr, uid, active_id, data, context=context)
#
#         if order_obj.test_paid(cr, uid, [active_id]):
#             order_obj.signal_workflow(cr, uid, [active_id], 'paid')
#             return self.print_report(cr, uid, ids, active_id, context=context)
#
#         return self.launch_payment(cr, uid, ids, context=context)
#
#     def print_report(self, cr, uid, ids, order_id, context=None):
#         active_id = context.get('active_id', [])
#         datas = {
#             'ids': [order_id],
#             'model': 'pos.order',
#         }
#         return {
#             'type': 'ir.actions.report.xml',
#             'report_name': 'point_of_sale.report_receipt',
#             'context': {'active_model': 'pos.order'},
#             'datas': datas,
#         }
# # vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
