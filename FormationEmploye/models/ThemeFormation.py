from odoo import models, fields, api


class ThemeFormation(models.Model):
    _name = "formation.theme"
    _description = "Thème de formation"
    _order = "name"

# ---- Suivi et logistique ----
    

    # ---- Informations générales ----
    name = fields.Char(
        string="Nom du thème",
        required=True,
        index=True,
        translate=True
    )
    description = fields.Text(
        string="Description",
        help="Description détaillée du thème de formation."
    )
    objectif = fields.Text(
        string="Objectifs pédagogiques",
        help="Quels sont les objectifs attendus de ce thème ?"
    )
    domaine = fields.Selection(
        [
            ("informatique", "Informatique"),
            ("management", "Management"),
            ("finance", "Finance"),
            ("langues", "Langues"),
            ("communication", "Communication"),
            ("ressources_humaines", "Ressources humaines"),
            ("qualite", "Qualité"),
            ("autres", "Autres"),
        ],
        string="Domaine",
        required=True,
        default="autres"
    )
    mots_cles = fields.Char(
        string="Mots-clés",
        help="Tags ou mots-clés pour faciliter la recherche (ex: Python, Leadership)."
    )
    objectifs_mesurables = fields.Text(
        string="Résultats attendus",
        help="Quels résultats mesurables doivent être atteints après la formation."
    )
    langue = fields.Selection(
        [
            ("fr", "Français"),
            ("en", "Anglais"),
            ("es", "Espagnol"),
            ("ar", "Arabe"),
        ],
        string="Langue principale",
        default="fr"
    )
    certification = fields.Boolean(
        string="Certifiant",
        help="Indique si ce thème de formation donne lieu à une certification."
    )

    # ---- Relations ----
    module_ids = fields.One2many(
        "formation.module",
        "theme_id",
        string="Modules associés"
    )
    responsable_id = fields.Many2one(
        "res.users",
        string="Responsable pédagogique",
        help="La personne responsable de ce thème."
    )

    formation_employe_ids = fields.One2many('formation.employe', 'theme_id', string="Formations")
    duree_totale_theme = fields.Float(string="Durée totale du thème", compute="_compute_duree_totale_theme", store=True)
    @api.depends('formation_employe_ids.duree')
    def _compute_duree_totale_theme(self):
        for theme in self:
            theme.duree_totale_theme = sum(theme.formation_employe_ids.mapped('duree'))

    formateur_ids = fields.Many2many(
        "formation.formateur",
        "formation_theme_formateur_rel",
        "theme_id",
        "formateur_id",
        string="Formateurs spécialisés"
    )


   
    niveau = fields.Selection(
        [
            ("debutant", "Débutant"),
            ("intermediaire", "Intermédiaire"),
            ("avance", "Avancé"),
            ("expert", "Expert"),
        ],
        string="Niveau",
        default="debutant"
    )
    prerequis = fields.Text(
        string="Pré-requis",
        help="Compétences ou connaissances nécessaires avant de suivre ce thème."
    )
    public_cible = fields.Char(
        string="Public cible",
        help="Exemple : Étudiants, Managers, Développeurs, etc."
    )
    methode_pedagogique = fields.Selection(
        [
            ("presentiel", "Présentiel"),
            ("distanciel", "Distanciel"),
            ("hybride", "Hybride"),
            ("elearning", "E-learning"),
        ],
        string="Méthode pédagogique",
        default="presentiel"
    )
    support_cours = fields.Binary(
        string="Support de cours",
        help="Documents PDF, PowerPoint ou autres supports pédagogiques."
    )
    support_nom = fields.Char(string="Nom du fichier")

    lieu = fields.Char(
        string="Lieu de formation",
        help="Lieu habituel où se déroule ce thème de formation."
    )
    capacite_max = fields.Integer(
        string="Capacité maximale",
        help="Nombre maximum de participants conseillés pour ce thème."
    )
    date_Creation=fields.Datetime(string="Date de Création", tracking=True)
    date_Modification=fields.Datetime(string="Date de Modification", tracking=True)

    
    
    actif = fields.Boolean(
        string="Actif",
        default=True,
        help="Désactivez ce thème pour le retirer du catalogue sans le supprimer."
    )

    # ---- KPI / Indicateurs ----
    nombre_modules = fields.Integer(
        string="Nombre de modules",
        compute="_compute_nombre_modules",
        store=True
    )
    taux_satisfaction = fields.Float(
        string="Taux de satisfaction (%)",
        help="Indice moyen basé sur les évaluations."
    )
    nb_participants = fields.Integer(
        string="Nombre total de participants",
        help="Nombre de participants ayant suivi ce thème (statistique globale)."
    )
    cout_moyen = fields.Float(
        string="Coût moyen (DH)",
        help="Coût estimé moyen pour dispenser ce thème."
    )

    # ---- Méthodes ----
    
    @api.depends("module_ids")
    def _compute_nombre_modules(self):
        for theme in self:
            theme.nombre_modules = len(theme.module_ids)
