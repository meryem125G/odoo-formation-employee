# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError

class FormationEmploye(models.Model):
    _name = "formation.employe"
    _description = "Formation Employé"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "date_debut desc"

    # Liste des modules et formateurs associés
    module_line_ids = fields.One2many(
        'formation.employe.module.line',
        'formation_id',
        string="Modules et Formateurs"
    )

    total_tarif_modules = fields.Float(string="Total Tarif Modules", compute="_compute_total_tarifs", store=True)
    total_tarif_formateurs = fields.Float(string="Total Tarif Formateurs", compute="_compute_total_tarifs", store=True)

    budget_alloue = fields.Float(string="Budget alloué")
    budget_reel_modules = fields.Float(string="Budget réel Modules", compute="_compute_budget_reel", store=True)
    budget_reel_formateurs = fields.Float(string="Budget réel Formateurs", compute="_compute_budget_reel", store=True)
    budget_total_reel = fields.Float(string="Budget total réel", compute="_compute_budget_reel", store=True)

    budget_modules_ok = fields.Boolean(string="Modules dans budget alloué", compute="_compute_budget_reel", store=True)
    budget_formateurs_ok = fields.Boolean(string="Formateurs dans budget alloué", compute="_compute_budget_reel", store=True)
    budget_total_ok = fields.Boolean(string="Budget total dans budget alloué", compute="_compute_budget_reel", store=True)
    
    @api.depends('module_line_ids.tarif_modules', 'module_line_ids.tarif_formateurs')
    def _compute_total_tarifs(self):
        for formation in self:
            formation.total_tarif_modules = sum(formation.module_line_ids.mapped('tarif_modules'))
            formation.total_tarif_formateurs = sum(formation.module_line_ids.mapped('tarif_formateurs'))
    theme_id = fields.Many2one('formation.theme', string="Thème de formation", tracking=True)

    @api.onchange('theme_id')
    def _onchange_theme(self):
        """Copier le thème dans les lignes existantes et filtrer les modules"""
        for line in self.module_line_ids:
            line.theme_id = self.theme_id

    # Multiple formateurs pour le module
   


    formateur_id = fields.Many2one('formation.formateur', string="Formateur")
    module_id = fields.Many2one('formation.module', string="Module de formation", tracking=True)
    # Informations principales
    name = fields.Char(string="Titre de la formation", required=True, tracking=True)
    employe_ids = fields.Many2many(
    'hr.employee',                # modèle cible
    'formation_employe_rel',      # table de relation
    'formation_id',               # colonne pour formation.employe
    'employee_id',                # colonne pour hr.employee
    string="Employés participants",
    tracking=True)    
    organisme = fields.Char(string="Organisme formateur", tracking=True)
    organisme_id = fields.Many2one('formation.organisme', string="Organisme formateur", tracking=True)

    type_formation = fields.Selection([
        ('interne', 'Interne'),
        ('externe', 'Externe'),
        ('online', 'En ligne')
    ], string="Type de formation", default='interne', tracking=True)
    niveau = fields.Selection([
        ('debutant', 'Débutant'),
        ('intermediaire', 'Intermédiaire'),
        ('avance', 'Avancé')
    ], string="Niveau", default='debutant', tracking=True)
    public_cible = fields.Char(string="Public cible / Département", tracking=True)
    
    departement_id = fields.Many2one(
    'formation.departement', 
    string="Département",
    required=True,
    help="Sélectionnez le département associé à cette formation"
)

    priorite = fields.Selection([
        ('haute', 'Haute'),
        ('moyenne', 'Moyenne'),
        ('basse', 'Basse')
    ], string="Priorité", default='moyenne', tracking=True)
    lieu = fields.Char(string="Lieu de la formation")
    date_debut = fields.Datetime(string="Date de début", required=True, tracking=True)
    duree = fields.Float(string="Durée (heures)", compute="_compute_duree", store=True)
    duree_Jours = fields.Float(string="Durée (Jours)", compute="_compute_duree", store=True)
    
    autres_frais = fields.Float(string="autres frais")
    cout = fields.Float(string="Coût réel de la formation")
    certificate = fields.Binary(string="Certificat", attachment=True)
    description = fields.Text(string="Description / Objectifs")
    programme = fields.Binary(string="Programme de formation", attachment=True)
    supports = fields.Binary(string="Supports pédagogiques", attachment=True)
    # Documents complémentaires
    rapport_formation = fields.Binary(string="Rapport de formation", attachment=True)
    document_giac = fields.Binary(string="Document GIAC", attachment=True)

    
    # GIAC
    giac_id = fields.Many2one('formation.giac', string="Dossier GIAC")
    declare_giac = fields.Boolean(string="Déclarée au GIAC", default=False)
    impact_formation = fields.Text(string="Impact attendu sur l'employé / département")
    plan_action_post_formation = fields.Text(string="Plan d'action post-formation")
    giac_eligibilite = fields.Boolean(string="Eligibilité GIAC")  # ajouté car utilisé dans la vue
    giac_reference = fields.Char(string="Référence GIAC")
    giac_statut = fields.Selection([
        ('en_cours', 'En cours'),
        ('valide', 'Validé'),
        ('refuse', 'Refusé'),
        ('cloture', 'Clôturé')
    ], string="Statut GIAC")
    giac_budget_accorde = fields.Float(string="Budget accordé")
    giac_budget_demande = fields.Float(string="Budget demandé")
    giac_date_demande = fields.Datetime(string="Date demande")
    giac_date_validation = fields.Datetime(string="Date validation")
    giac_date_cloture = fields.Datetime(string="Date de clôture")
    giac_organisme_agree = fields.Char(string="Organisme agréé GIAC")
    giac_contact_responsable = fields.Char(string="Contact responsable GIAC")
    giac_programme_valide = fields.Boolean(string="Programme validé GIAC")
    giac_observations = fields.Text(string="Observations GIAC")
    giac_commentaires_comite = fields.Text(string="Commentaires du comité GIAC")
    responsable_giac_id = fields.Many2one('res.users', string="Responsable suivi GIAC")
    date_soumission = fields.Datetime(string="Date soumission au GIAC")
    date_notification = fields.Datetime(string="Date notification")
    date_rapport_envoye = fields.Datetime(string="Date rapport formation envoyé")
    notes_internes = fields.Text(string="Notes internes")

    statut = fields.Selection([
        ('en_cours', 'En cours'),
        ('valide', 'Validée'),
        ('terminee', 'Terminée'),
        ('annulee', 'Annulée')
    ], string="Statut", default='en_cours', tracking=True)
    responsable_id = fields.Many2one('hr.employee', string="Responsable formation")

    date_validation = fields.Datetime(string="Date de validation")
    valide_par = fields.Many2one('res.users', string="Validé par")

    date_annulation = fields.Datetime(string="Date d'annulation de la formation")
    annule_par = fields.Many2one('res.users', string="Annulé par")
    motif_annulation = fields.Text(string="Motif de l'annulation")

    date_fin = fields.Datetime(string="Date de fin", tracking=True)
    termine_par = fields.Many2one('res.users', string="Terminé par")


    # Évaluation & compétences
    evaluation = fields.Selection([
        ('faible', 'Faible'),
        ('moyenne', 'Moyenne'),
        ('bonne', 'Bonne'),
        ('excellente', 'Excellente')
    ], string="Evaluation")
    score = fields.Float(string="Score de réussite (%)")
    competences_acquises = fields.Text(string="Compétences acquises")
    commentaires = fields.Text(string="Commentaires de l'évaluation")

    # Suivi administratif et financement
    reference = fields.Char(string="Référence interne")
    numero_demande = fields.Char(string="N° Demande")
    date_demande = fields.Datetime(string="Date de la demande")
    type_budget = fields.Selection([
        ('societe', 'Budget Société'),
        ('departement', 'Budget Département')
    ], string="Type de budget")

    # Avancement
    avancement = fields.Float(string="Avancement (%)", compute="_compute_avancement", store=True)


    @api.onchange('theme_id')
    def _onchange_theme(self):
        if self.theme_id:
            return {'domain': {'module_id': [('theme_id', '=', self.theme_id.id)]}}
        else:
            return {'domain': {'module_id': []}}

    @api.onchange('formateur_id')
    def _onchange_formateur(self):
        domain_modules = []
        if self.formateur_id:
            domain_modules = [('formateur_ids', 'in', self.formateur_id.id)]
            if self.theme_id:
                domain_modules.append(('theme_id', '=', self.theme_id.id))
        return {'domain': {'module_id': domain_modules}}


    def action_valider(self):
        for record in self:
            if record.statut in ['terminee', 'annulee']:
                raise UserError("Impossible de valider une formation terminée ou annulée.")
            if record.statut == 'valide':
                raise UserError("Cette formation est déja validée.")
            if record.giac_statut == 'cloture':
                raise UserError("Impossible de valider, dossier GIAC clôturé.")
            record.statut = 'valide'
            record.date_validation = fields.Datetime.now()
            record.valide_par = self.env.user.id  # ou juste self.env.user si Many2one

    def action_terminer(self):
        for record in self:
            if record.statut == 'annulee':
                raise UserError("Impossible de terminer une formation annulée.")
            if record.statut == 'terminee':
                raise UserError("Cette formation est deja términée.")
            if record.statut == 'en_cours':
                raise UserError("Il faut d'abord valider la formation.")
            
            record.statut = 'terminee'
            record.date_fin = fields.Datetime.now()
            record.termine_par = self.env.user.id  # ou juste self.env.user si Many2one


    def action_annuler(self):
        for record in self:
            if record.statut == 'terminee':
                raise UserError("Impossible d'annuler une formation terminée.")
            if record.statut == 'annulee':
                raise UserError("la formation est déja annulée.")
            
            if record.giac_statut == 'cloture':
                raise UserError("Impossible d'annuler, dossier GIAC clôturé.")
            record.statut = 'annulee'
            record.date_annulation = fields.Datetime.now()
            record.annule_par = self.env.user.id  # ou juste self.env.user si Many2one


    @api.depends('date_debut', 'date_fin')
    def _compute_duree(self):
        for record in self:
            if record.date_debut and record.date_fin:
                delta = record.date_fin - record.date_debut
                # durée en heures
                record.duree = delta.total_seconds() / 3600
                # durée en jours
                record.duree_Jours = delta.total_seconds() / (24 * 3600)
            else:
                record.duree = 0
                record.duree_Jours = 0

    @api.depends('date_debut', 'date_fin', 'statut')
    def _compute_avancement(self):
        for record in self:
            if record.statut == 'terminee':
                record.avancement = 100
            elif record.statut == 'valide':
                record.avancement = 50
            elif record.statut == 'en_cours':
                record.avancement = 25
            elif record.statut in ['annulee', 'planifie', 'refuse']:
                record.avancement = 0
            elif record.date_debut and record.date_fin:
                total = (record.date_fin - record.date_debut).total_seconds()
                elapsed = max(0, (min(fields.Datetime.now(), record.date_fin) - record.date_debut).total_seconds())
                record.avancement = min(100, int((elapsed / total) * 100))
            else:
                record.avancement = 0


    @api.model
    def create(self, vals):
        record = super().create(vals)
    # Copier le thème parent dans toutes les lignes existantes
        for line in record.module_line_ids:
            line.theme_id = record.theme_id
        return record
    
    
    marge_modules = fields.Float(string="Marge Modules", compute="_compute_budget_reel", store=True)
    marge_formateurs = fields.Float(string="Marge Formateurs", compute="_compute_budget_reel", store=True)
    marge_totale = fields.Float(string="Marge Totale", compute="_compute_budget_reel", store=True)

    
    @api.depends('module_line_ids.tarif_modules',
             'module_line_ids.tarif_formateurs',
             'module_line_ids.autres_frais',
             'budget_alloue',
             'autres_frais')
    def _compute_budget_reel(self):
        for formation in self:
            total_modules = sum(formation.module_line_ids.mapped('tarif_modules'))
            total_formateurs = sum(formation.module_line_ids.mapped('tarif_formateurs'))
            total_autres_frais_lignes = sum(formation.module_line_ids.mapped('autres_frais'))

            #  autres frais de la formation (champ principal) + des lignes
            total_autres_frais = (formation.autres_frais or 0.0) + total_autres_frais_lignes

            # Budgets réels
            formation.budget_reel_modules = total_modules + total_autres_frais
            formation.budget_reel_formateurs = total_formateurs + total_autres_frais
            formation.budget_total_reel = total_modules + total_formateurs + total_autres_frais

            # Comparaison budget alloué
            formation.budget_modules_ok = formation.budget_alloue >= formation.budget_reel_modules if formation.budget_alloue else False
            formation.budget_formateurs_ok = formation.budget_alloue >= formation.budget_reel_formateurs if formation.budget_alloue else False
            formation.budget_total_ok = formation.budget_alloue >= formation.budget_total_reel if formation.budget_alloue else False

            # Marges
            formation.marge_modules = (formation.budget_alloue - formation.budget_reel_modules) if formation.budget_alloue else 0.0
            formation.marge_formateurs = (formation.budget_alloue - formation.budget_reel_formateurs) if formation.budget_alloue else 0.0
            formation.marge_totale = (formation.budget_alloue - formation.budget_total_reel) if formation.budget_alloue else 0.0
