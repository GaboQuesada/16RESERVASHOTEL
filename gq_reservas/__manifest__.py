# -*- coding: utf-8 -*-
{
    'name': "gq_reservas",

    'summary': """
        Módulo de reservas y hotelería """,

    'description': """
        Módulo de reservas y hotelería 
    """,

    'author': "GQSOLUCIONES DEELSA - GABRIEL QUESADA SANCHEZ",
    'website': "https://gqsoluciones.com/reservas",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base','account','sale','stock','sale_stock','sale_management','saldosfe'],
    'data': [
        
        'security/groups.xml',
        'security/ir.model.access.csv',
        'wizards/saleorderadd.xml',
        'wizards/saleorderaddlines.xml',
        'wizards/showhabitaciones.xml',
        'wizards/otrosproductos.xml',
        'report/ir_actions_report.xml',
        'report/ir_actions_report_templates.xml',
        'report/ir_actions_report_reserva_templates.xml',
        'data/reservacioneshotel.xml',
        'data/mail_template_data.xml',
        'data/mail_template_reserva_data.xml',
        'views/product_reserva.xml',
        'views/product_template.xml',
        'views/reservahotel.xml',
        'views/saleorder.xml',
        'views/saleorder.xml',
        'views/sale_order_line_view.xml',
        'views/resconfig.xml',
        'views/resumen.xml',
        'views/daily_report.xml',
        'views/politicas.xml',
        'views/menus.xml',
    ],
    "assets": {
        "web.assets_qweb": [
            "reservas/static/src/xml/hotel_room_summary.xml",
        ],
        "web.assets_backend": [
            "reservas/static/src/css/room_summary.css",
            "reservas/static/src/js/hotel_room_summary.js",
        ],
    },
    "external_dependencies": {"python": ["dateutil"]},
    'application': False,
    'auto_install': False,
}
