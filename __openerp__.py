# -*- encoding: utf-8 -*-

#
# Status 1.0 - tested on Open ERP 7
#

{
    'name': 'POS con cambios para cumplir con la SAT',
    'version': '1.0',
    'category': 'Custom',
    'description': """
POS con cambios para cumplir con la SAT
""",
    'author': 'Rodrigo Fernandez',
    'website': 'http://solucionesprisma.com/',
    'depends': ['account_voucher', 'point_of_sale'],
    'data': [
        'resolucion_view.xml',
        'account_view.xml',
        'point_of_sale_view.xml',
        'ir_sequence.xml',
        'report.xml',
        'views/report_bitacora_factura.xml',
        'views/report_bitacora_resolucion.xml',
    ],
    'demo': [],
    'installable': True
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
