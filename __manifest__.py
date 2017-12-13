# -*- encoding: utf-8 -*-

{
    'name': 'POS SAT',
    'version': '1.0',
    'category': 'Custom',
    'description': """ POS con cambios para cumplir con la SAT """,
    'author': 'Rodrigo Fernandez',
    'website': 'http://aquih.com/',
    'depends': ['account', 'point_of_sale'],
    'data': [
        'view/resolucion_view.xml',
        # 'account_view.xml',
        # 'point_of_sale_view.xml',
        # 'ir_sequence.xml',
        # 'report.xml',
        # 'views/report_bitacora_factura.xml',
        # 'views/report_bitacora_resolucion.xml',
    ],
    'installable': True
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
