# -*- coding: utf-8 -*-
{
    'name': "Formation Employé",
    'version': "1.0",
    'category': "Human Resources",
    'summary': "Gestion complète des formations des employés",
    'description': """
Gestion des formations des employés :
- Planification des sessions de formation
- Suivi administratif des participants
- Suivi des compétences et indicateurs (KPI)
- Gestion des formateurs et organismes
- Organisation par thèmes et modules
- Analyse et reporting
""",
    'author': "Meravox",
    'website': "http://www.meravox.com",
    'depends': ['base', 'hr', 'mail', 'calendar'],
    'data': [
        'security/ir.model.access.csv',
        'views/formation_views.xml',
        'views/dossier_giac_view.xml',
        'views/formationOrganisme_views.xml',
        'views/Formateur_views.xml',
        'views/formationTheme.xml',
        'views/ThemeModule.xml',
        'views/departement_view.xml',
        'views/formation_menus.xml',
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
