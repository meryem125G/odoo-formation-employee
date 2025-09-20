# -*- coding: utf-8 -*-
{
    'name': "Formation Employé",
    'version': "1.0",
    'category': "Human Resources",
    'summary': "Gestion complète des formations des employés",

    'description': """
    <h2>Gestion des formations des employés</h2>
    <ul>
    <li>Planification des sessions de formation</li>
    <li>Suivi administratif des participants</li>
    <li>Suivi des compétences et indicateurs (KPI)</li>
    <li>Gestion des formateurs et organismes</li>
    <li>Organisation par thèmes et modules</li>
    <li>Analyse et reporting</li>
    </ul>
    <p>Vidéo de démonstration :</p>
    <!--
    <iframe width="560" height="315" src="https://www.youtube.com/embed/TON_ID_VIDEO" frameborder="0" allowfullscreen></iframe>
    -->

    """
    ,
    'author': "Meravox",
    'website': "http://www.meravox.com",
    'depends': ['base', 'hr', 'mail', 'calendar'],
    'license': 'LGPL-3',  # ou MIT si tu choisis
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
