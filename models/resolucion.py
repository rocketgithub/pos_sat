# -*- encoding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime

import logging

class Resolucion(models.Model):
    _name = 'pos_sat.resolucion'
    _description = 'Resolucion de la SAT'
    _order = 'fecha desc'

    name = fields.Char('Numero de resolucion', size=40, required=True)
    fecha = fields.Date('Fecha de resolucion', required=True)
    serie = fields.Char('Serie', size=10, required=True)
    direccion = fields.Char('Direccion', required=True)
    inicial = fields.Integer('Del', required=True)
    final = fields.Integer('Al', required=True)
    primera = fields.Boolean('Primera')
    valido = fields.Boolean('Valido', readonly=True)
    tipo_doc = fields.Selection([('Factura','Factura')], 'Tipo', required=True)
    fecha_ingreso = fields.Date('Fecha de ingreso', required=True, readonly=True, default=lambda self: fields.Date.context_today(self))
    fecha_vencimiento = fields.Date('Fecha de vencimiento')

    @api.one
    @api.constrains('name')
    def _revisar_name(self):
        r = self.search([('name','=',self.name)], order="final desc")
        if len(r) > 1:
            raise ValidationError('El numero de resolució ya existe en el sistema.')

    @api.one
    @api.constrains('fecha_ingreso')
    def _revisar_fecha(self):
        f = datetime.strptime(self.fecha, '%Y-%m-%d')
        fi = datetime.strptime(self.fecha_ingreso, '%Y-%m-%d')
        if (fi - f).days > 10:
            raise ValidationError('La fecha de ingreso no debe de ser mayor a 10 dias de la fecha de la resolucion')

    @api.one
    @api.constrains('inicial','final')
    def _revisar_rango(self):
        ant = self.search([('serie','=',self.serie),('id','!=',self.id)], order="final desc")
        if len(ant) > 0:
            if self.inicial != ant[0].final + 1:
                raise ValidationError('El número inicial de esta resolución no es el final + 1 de la resolución anterior de la misma serie')
        else:
            if self.inicial != 1:
                raise ValidationError('El número inicial de esta resolución debe ser 1, pues es una nueva serie')
        if int(self.final) <= int(self.inicial):
            raise ValidationError('El número inicial de esta resolución es mayor que el final de esta resolución')
        cruzados = self.search([('serie','=',self.serie),('inicial','<=',self.inicial),('final','>=',self.inicial)])
        if len(cruzados) > 1:
            raise ValidationError('Ya existe otra resolución con esta serie y en el mismo rango')
        cruzados = self.search([('serie','=',self.serie),('inicial','<=',self.final),('final','>=',self.final)])
        if len(cruzados) > 1:
            raise ValidationError('Ya existe otra resolución con esta serie y en el mismo rango')
        cruzados = self.search([('serie','=',self.serie),('inicial','>=',self.inicial),('inicial','<=',self.final)])
        if len(cruzados) > 1:
            raise ValidationError('Ya existe otra resolución con esta serie y en el mismo rango')

    @api.model
    def create_old(self, vals):
        vals.update({'valido': True})
        anio = vals['fecha'][0:4]
        resto = vals['fecha'][4:]
        if vals['primera']:
            vals.update({'fecha_vencimiento': str(int(anio)+1)+resto})
        else:
            vals.update({'fecha_vencimiento': str(int(anio)+2)+resto})
        return super(Resolucion, self).create(vals)
