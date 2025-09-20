from odoo import models, fields, api

class ModuleFormation(models.Model):
    _name = "formation.module"
    _description = "Module de formation"
    _order = "name"

    # ---- Informations générales ----
    name = fields.Char(string="Nom du module", required=True)
    code_module = fields.Char(string="Code du module", help="Code interne du module pour identification rapide.")
    description = fields.Text(string="Description", help="Description détaillée du module.")
    duree = fields.Float(string="Durée (heures)", help="Durée estimée du module en heures.")
    cout_par_heure = fields.Float(string="Coût (DH)/heure", help="Coût estimé pour dispenser ce module par heure.")
    cout_total = fields.Float(string="Coût (DH)", help="Coût estimé pour dispenser ce module.")

    niveau = fields.Selection([
        ("debutant", "Débutant"),
        ("intermediaire", "Intermédiaire"),
        ("avance", "Avancé"),
        ("expert", "Expert"),
    ], string="Niveau", default="debutant")
    methode_pedagogique = fields.Selection([
        ("presentiel", "Présentiel"),
        ("distanciel", "Distanciel"),
        ("hybride", "Hybride"),
        ("elearning", "E-learning"),
    ], string="Méthode pédagogique", default="presentiel")
    
    # ---- Relations ----
    theme_id = fields.Many2one('formation.theme', string="Thème", required=True, ondelete='cascade')

    fournisseur_ids = fields.Many2many(
    'res.partner',
    string="Fournisseurs",
    help="Fournisseurs qui peuvent dispenser ce module."
)

    formateur_ids = fields.Many2many(
    'formation.formateur',
    'formateur_module_rel',  # même table que côté formateur
    'module_id',             # colonne module
    'formateur_id',          # colonne formateur
    string="Formateurs"
)


    
    # ---- Suivi et logistique ----
    date_creation = fields.Datetime(string="Date de création", default=fields.Datetime.now)
    date_modification = fields.Datetime(string="Date de modification", tracking=True)
    actif = fields.Boolean(string="Actif", default=True)
    capacite_max = fields.Integer(string="Capacité maximale", help="Nombre maximum de participants.")

    # ---- KPI / indicateurs ----
    nb_participants = fields.Integer(string="Nombre de participants", compute="_compute_nb_participants", store=True)
    
    # ---- Méthodes ----
    @api.depends('formation_employe_ids')
    def _compute_nb_participants(self):
        for module in self:
            module.nb_participants = len(module.formation_employe_ids) if hasattr(module, 'formation_employe_ids') else 0

    # Relations avec les formations pour calculs/statistiques
    formation_employe_ids = fields.One2many('formation.employe', 'module_id', string="Formations liées")

