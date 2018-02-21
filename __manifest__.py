# -*- encoding: utf-8 -*-

{
    'name': 'POS SAT',
    'version': '1.0',
    'category': 'Custom',
    'description': """ POS con cambios para cumplir con la SAT """,
    'author': 'Rodrigo Fernandez',
    'website': 'http://aquih.com/',
    'depends': ['account', 'point_of_sale', 'pos_gt'],
    'data': [
        'views/resolucion_view.xml',
        'views/account_view.xml',
        'views/ir_sequence.xml',
        # 'views/point_of_sale_view.xml',
        'views/report.xml',
        'views/report_bitacora_factura.xml',
        'views/report_bitacora_resolucion.xml',
        'views/templates.xml',
    ],
    'qweb': [
        'static/src/xml/pos_sat.xml',
    ],
    'installable': True
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
