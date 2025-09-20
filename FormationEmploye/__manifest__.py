# -*- coding: utf-8 -*-
{
    'name': "Formation Employé",
    'version': "1.0",
    'category': "Human Resources",
    'summary': "Gestion des formations des employés",
    'description': """
        Ce module permet de gérer les formations suivies par les employés,
        avec suivi administratif, planification et analyse des compétences.
    """,
    'author': "Votre Nom",
    'website': "http://www.votresite.com",
    'depends': ['base', 'hr', 'mail'],
    'data': [
        'views/formation_views.xml',
        'views/dossier_giac_view.xml',
        'views/formationOrganisme_views.xml',
        'views/Formateur_views.xml',
        'views/formationTheme.xml',
        'views/ThemeModule.xml',
        'views/departement_view.xml',




        'views/formation_menus.xml',
        'security/ir.model.access.csv',
    ],
     'assets': {
        'web.assets_backend': [
            'FormationEmploye/static/src/css/formation_styles.css',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
