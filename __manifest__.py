#-*- coding: utf-8 -*-
{
    'name': "Video Club",

    'summary': """
        Aplicacion donde se almacenan peliculas""",

    'description': """
        Modulo para la organizacion de peliculas por genero cinematografico
    """,

    'author': "Luciano",
    'website': "https://www.almacendefilms.com",

    # Categories can be used to filter modules in modules listing
    'category': 'Uncategorized',
    'license': 'LGPL-3',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/grupos.xml',
        'security/reglas_acceso.xml',
        'views/views.xml',
        'views/templates.xml',
        'report/informe_template.xml',
        'report/informe_pelicula.xml',
        'data/cron_jobs.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
    'installable': True,
}
