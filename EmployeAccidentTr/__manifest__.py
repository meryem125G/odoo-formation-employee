# -*- coding: utf-8 -*-
{
    'name': "Accidents Travail des Employés",
    'summary': "Gestion des accidents de travail des employés",
    'description': """
Module de base pour gérer les accidents de travail des employés.
(Pas encore de vues, de modèles ou de fichiers de données créés)
    """,
    'author': "meravox",
    'website': "https://www.meravox.com",
    'category': 'Human Resources',
    'version': '1.0',
    'depends': ['base','hr','web'],   # dépendance minimale pour tout module Odoo
    'data': [
        'views/accident_views.xml',
        'views/assurance_view.xml',
        'views/dossierAccidentAssurance_view.xml',
        'views/contact_views.xml',
        'views/accident_menus.xml',
        'data/accident_sequence.xml',
        'security/ir.model.access.csv'
    ],
    'assets': {
        'web.assets_backend': [
            'EmployeAccidentTr/static/src/js/body_map.js'
            
        ],
    },
 
    'installable': True,
    'application': True,

}