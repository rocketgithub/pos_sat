# -*- encoding: utf-8 -*-

from odoo import api, fields, models, _

class Resolucion(models.Model):
    _name = 'pos_sat.resolucion'
    _description = 'Resolucion de la SAT'
    _order = 'fecha desc'

    name = fields.Char('Numero de resolucion', size=40, required=True),
    fecha = fields.Date('Fecha de resolucion', required=True, default=lambda self: fields.Date.context_today(self)),
    serie = fields.Char('Serie', size=10, required=True),
    direccion = fields.Char('Direccion', required=True),
    inicial = fields.Integer('Del', required=True),
    final = fields.Integer('Al', required=True),
    primera = fields.Boolean('Primera'),
    valido = fields.Boolean('Valido', readonly=True),
    tipo_doc = fields.Selection([('Factura','Factura')], 'Tipo', required=True),
    fecha_ingreso = fields.Date('Fecha de ingreso', required=True, readonly=True),
    fecha_vencimiento = fields.Date('Fecha de vencimiento', readonly=True),

    # @api.one
    # @api.constrains('fecha_ingreso')
    # def _revisar_fecha(self, cr, uid, ids, context=None):
    #     r = self.browse(cr, uid, ids[0], context=context)
    #     f = datetime.strptime(r.fecha, '%Y-%m-%d')
    #     fi = datetime.strptime(r.fecha_ingreso, '%Y-%m-%d')
    #     if (fi - f).days > 10:
    #         return False
    #     return True
    #
    # @api.one
    # @api.constrains('inicial','final')
    # def _revisar_rango(self, cr, uid, ids, context=None):
    #     r = self.browse(cr, uid, ids[0], context=context)
    #     anterior = self.search(cr, uid, [('serie','=',r.serie),('id','not in',ids)], order="final desc")
    #     if len(anterior) > 0:
    #         a = self.browse(cr, uid, anterior[0], context=context)
    #         if r.inicial != a.final + 1:
    #             return False
    #     else:
    #         if r.inicial != 1:
    #             return False
    #     if int(r.final) <= int(r.inicial):
    #         return False
    #     cruzados = self.search(cr, uid, [('serie','=',r.serie),('inicial','<=',r.inicial),('final','>=',r.inicial)])
    #     if len(cruzados) > 1:
    #         return False
    #     cruzados = self.search(cr, uid, [('serie','=',r.serie),('inicial','<=',r.final),('final','>=',r.final)])
    #     if len(cruzados) > 1:
    #         return False
    #     cruzados = self.search(cr, uid, [('serie','=',r.serie),('inicial','>=',r.inicial),('inicial','<=',r.final)])
    #     if len(cruzados) > 1:
    #         return False
    #     return True
    #
    # _constraints = [
    #     (_revisar_fecha, 'La fecha de ingreso no debe de ser mayor a 10 dias de la fecha de la resolucion', ['fecha_ingreso']),
    #     (_revisar_rango, 'El rango de la resolucion es incorrecto', ['inicial','final']),
    # ]
    #
    # _sql_constraints = [
    #     ('name_uniq', 'unique (name)', 'La resolucion debe de ser unica.'),
    # ]
    #
    # def create(self, cr, uid, vals, context=None):
    #     vals.update({'valido': True})
    #     anio = vals['fecha'][0:4]
    #     resto = vals['fecha'][4:]
    #     if vals['primera']:
    #         vals.update({'fecha_vencimiento': str(int(anio)+1)+resto})
    #     else:
    #         vals.update({'fecha_vencimiento': str(int(anio)+2)+resto})
    #     return super(resolucion, self).create(cr, uid, vals, context)
