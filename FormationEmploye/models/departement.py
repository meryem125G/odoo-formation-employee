from odoo import models, fields, api

class FormationDepartement(models.Model):
    _name = "formation.departement"
    _description = "Département de formation"
    _order = "name"

    # ---------------- Informations générales ----------------
    name = fields.Char(string="Nom du département", required=True, index=True)
    code = fields.Char(string="Code du département", help="Code interne du département pour identification rapide")
    description = fields.Text(string="Description", help="Description détaillée du département")
    responsable_id = fields.Many2one('res.users', string="Responsable", help="Responsable du département")
    parent_id = fields.Many2one('formation.departement', string="Département parent", help="Pour les hiérarchies de départements")
    child_ids = fields.One2many('formation.departement', 'parent_id', string="Sous-départements")
    actif = fields.Boolean(string="Actif", default=True)

    # ---------------- Suivi et logistique ----------------
    date_creation = fields.Datetime(string="Date de création", default=fields.Datetime.now, readonly=True)
    date_modification = fields.Datetime(string="Date de modification", tracking=True)
    capacite_max = fields.Integer(string="Capacité maximale", help="Nombre maximum de participants pour le département")

    # ---------------- Relations ----------------
    formation_ids = fields.One2many('formation.employe', 'departement_id', string="Formations liées")
    module_ids = fields.Many2many('formation.module', string="Modules disponibles")
    employe_ids = fields.Many2many('res.partner', string="Employés associés", domain=[('employee', '=', True)])

    # ---------------- KPI / indicateurs ----------------
    nb_formations = fields.Integer(string="Nombre de formations", compute="_compute_nb_formations", store=True)
    nb_modules = fields.Integer(string="Nombre de modules", compute="_compute_nb_modules", store=True)
    nb_employes = fields.Integer(string="Nombre d'employés", compute="_compute_nb_employes", store=True)

    @api.depends('formation_ids')
    def _compute_nb_formations(self):
        for dept in self:
            dept.nb_formations = len(dept.formation_ids)

    @api.depends('module_ids')
    def _compute_nb_modules(self):
        for dept in self:
            dept.nb_modules = len(dept.module_ids)

    @api.depends('employe_ids')
    def _compute_nb_employes(self):
        for dept in self:
            dept.nb_employes = len(dept.employe_ids)

    # ---------------- Méthodes utilitaires ----------------
    def toggle_actif(self):
        for dept in self:
            dept.actif = not dept.actif

    def name_get(self):
        """Affiche le nom avec le code pour plus de lisibilité"""
        result = []
        for dept in self:
            name = f"[{dept.code}] {dept.name}" if dept.code else dept.name
            result.append((dept.id, name))
        return result
