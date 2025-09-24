# -*- coding: utf-8 -*-
{
    'name': "Formation Employé",
    'version': "1.0",
    'category': "Human Resources",
    'summary': "Gestion complète des formations des employés",

    'description': """
<h2>Formation Employé</h2>
<p>Gestion complète des formations des employés</p>
<ul>
  <li>Planification des sessions de formation</li>
  <li>Suivi administratif des participants</li>
  <li>Suivi des compétences et indicateurs (KPI)</li>
  <li>Gestion des formateurs et organismes</li>
  <li>Organisation par thèmes et modules</li>
  <li>Analyse et reporting</li>
</ul>
<p>Vidéo de démonstration (commentée pour l'instant)</p>
""",

    'price': 35.0,          # valeur float, pas string
    'currency': 'USD',
    'author': "Meravox",
    'website': "http://www.meravox.com",
    'depends': ['base', 'hr', 'mail', 'calendar'],
    'license': 'LGPL-3',
    'images': ['static/description/cover.png'],
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
