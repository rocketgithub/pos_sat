# -*- encoding: utf-8 -*-

from openerp.osv import fields, osv
from datetime import datetime
import logging

class resolucion(osv.osv):
    _name = 'pos_sat.resolucion'
    _description = 'Resolucion de la SAT'

    _columns = {
        'name': fields.char('Numero de resolucion', size=40, required=True),
        'fecha': fields.date('Fecha de resolucion', required=True),
        'serie': fields.char('Serie', size=10, required=True),
        'direccion': fields.char('Direccion', required=True),
        'inicial': fields.integer('Del', required=True),
        'final': fields.integer('Al', required=True),
        'primera': fields.boolean('Primera'),
        'valido': fields.boolean('Valido', readonly=True),
        'tipo_doc': fields.selection((('Factura','Factura'),), 'Tipo', required=True),
        'fecha_ingreso': fields.date('Fecha de ingreso', required=True, readonly=True),
        'fecha_vencimiento': fields.date('Fecha de vencimiento', readonly=True),
    }
    _order = 'fecha desc'

    _defaults = {
        'fecha_ingreso': fields.date.context_today,
    }

    def _revisar_fecha(self, cr, uid, ids, context=None):
        r = self.browse(cr, uid, ids[0], context=context)
        f = datetime.strptime(r.fecha, '%Y-%m-%d')
        fi = datetime.strptime(r.fecha_ingreso, '%Y-%m-%d')
        if (fi - f).days > 10:
            return False
        return True

    def _revisar_rango(self, cr, uid, ids, context=None):
        r = self.browse(cr, uid, ids[0], context=context)
        anterior = self.search(cr, uid, [('serie','=',r.serie),('id','not in',ids)], order="final desc")
        if len(anterior) > 0:
            a = self.browse(cr, uid, anterior[0], context=context)
            if r.inicial != a.final + 1:
                return False
        else:
            if r.inicial != 1:
                return False
        if int(r.final) <= int(r.inicial):
            return False
        cruzados = self.search(cr, uid, [('serie','=',r.serie),('inicial','<=',r.inicial),('final','>=',r.inicial)])
        if len(cruzados) > 1:
            return False
        cruzados = self.search(cr, uid, [('serie','=',r.serie),('inicial','<=',r.final),('final','>=',r.final)])
        if len(cruzados) > 1:
            return False
        cruzados = self.search(cr, uid, [('serie','=',r.serie),('inicial','>=',r.inicial),('inicial','<=',r.final)])
        if len(cruzados) > 1:
            return False
        return True

    _constraints = [
        (_revisar_fecha, 'La fecha de ingreso no debe de ser mayor a 10 dias de la fecha de la resolucion', ['fecha_ingreso']),
        (_revisar_rango, 'El rango de la resolucion es incorrecto', ['inicial','final']),
    ]

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'La resolucion debe de ser unica.'),
    ]

    def create(self, cr, uid, vals, context=None):
        vals.update({'valido': True})
        anio = vals['fecha'][0:4]
        resto = vals['fecha'][4:]
        if vals['primera']:
            vals.update({'fecha_vencimiento': str(int(anio)+1)+resto})
        else:
            vals.update({'fecha_vencimiento': str(int(anio)+2)+resto})
        return super(resolucion, self).create(cr, uid, vals, context)
