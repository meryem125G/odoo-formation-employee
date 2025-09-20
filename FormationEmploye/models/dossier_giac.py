# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError

class DossierGIAC(models.Model):
    _name = "formation.giac"
    _description = "Dossier GIAC pour formation"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "creation_date desc"

    formation_id = fields.Many2one('formation.employe', string="Formation liée")

    # Lien vers les formations
    formation_ids = fields.Many2many(
        'formation.employe',
        'giac_formation_rel',   # table de relation spécifique
        'giac_id',              # colonne pour la formation.giac
        'formation_id',         # colonne pour la formation.employe
        string="Formations sélectionnées",
        domain="[('statut','=','valide'), ('declare_giac','=', False)]",
        help="Sélectionnez uniquement les formations validées et non encore déclarées au GIAC"
    )

    formations_selection_ids = fields.Many2many(
        'formation.employe',
        'giac_selection_tmp_rel',
        'giac_id',
        'formation_id',
        string="Sélection temporaire des formations",
        domain="[('statut','=','valide'), ('declare_giac','=', False)]",
        help="Sélectionnez ici les formations validées et non déclarées à ajouter au dossier"
    )

    # Informations GIAC
    giac_reference = fields.Char(string="Référence dossier GIAC", required=True, tracking=True)
    giac_statut = fields.Selection([
        ('en_cours', 'En cours'),
        ('valide', 'Validé'),
        ('refuse', 'Refusé'),
        ('cloture', 'Clôturé')
    ], string="Statut dossier GIAC", default='en_cours', tracking=True)

    giac_budget_accorde = fields.Float(string="Montant accordé par GIAC")
    giac_budget_demande = fields.Float(string="Budget demandé")
    giac_date_demande = fields.Datetime(string="Date demande GIAC")
    giac_date_validation = fields.Datetime(string="Date validation GIAC")

    giac_date_validation_dossier = fields.Datetime(string="Date Validation dossier GIAC")
    giac_date_cloture = fields.Datetime(string="Date de clôture GIAC")
    giac_date_refus = fields.Datetime(string="Date refus dossier GIAC")

    valide_par = fields.Many2one('res.users', string="Validé par")
    cloture_par = fields.Many2one('res.users', string="Cloturé par")
    refuse_par = fields.Many2one('res.users', string="Refusé par")


    
    giac_organisme_agree = fields.Char(string="Organisme agréé GIAC")
    giac_contact_responsable = fields.Char(string="Contact responsable GIAC")
    giac_programme_valide = fields.Boolean(string="Programme validé GIAC")
    giac_observations = fields.Text(string="Observations GIAC")
    giac_commentaires_comite = fields.Text(string="Commentaires du comité GIAC")

    # Suivi administratif
    responsable_giac_id = fields.Many2one('res.users', string="Responsable suivi GIAC")
    date_soumission = fields.Datetime(string="Date soumission au GIAC")
    date_notification = fields.Datetime(string="Date notification GIAC")
    date_rapport_envoye = fields.Datetime(string="Date rapport formation envoyé")
    notes_internes = fields.Text(string="Notes internes")
    creation_date = fields.Datetime(string="Date création", default=fields.Datetime.now)

    # Documents
    document_giac = fields.Binary(string="Documents justificatifs GIAC", attachment=True)
    rapport_formation = fields.Binary(string="Rapport formation envoyé au GIAC", attachment=True)
    plan_action_post_formation = fields.Text(string="Plan d'action post-formation")
    Motif_temp = fields.Text(string="Motif temporaire", help="Saisir le motif avant validation")
    Motif_refus = fields.Text(string="Motif de refus", readonly=True)

    supports_annexes = fields.Binary(string="Supports annexes / complémentaires", attachment=True)
    certificats = fields.Binary(string="Certificat de formation", attachment=True)
    autres_documents = fields.Text(string="Autres documents / liens")

    # Évaluation & impact
    evaluation = fields.Selection([
        ('faible', 'Faible'),
        ('moyenne', 'Moyenne'),
        ('bonne', 'Bonne'),
        ('excellente', 'Excellente')
    ], string="Évaluation formation GIAC")
    score = fields.Float(string="Score (%) obtenu")
    impact_formation = fields.Text(string="Impact attendu sur l'employé / département")
    competences_acquises = fields.Text(string="Compétences acquises")
    retour_employe = fields.Text(string="Retour de l'employé")

    # Budget
    budget_initial = fields.Float(string="Budget initial")
    budget_reel = fields.Float(string="Budget réel dépensé")
    autres_financements = fields.Float(string="Autres financements")
    observations_budget = fields.Text(string="Observations budget")
    details_depenses = fields.Text(string="Détail des dépenses (libellé, montant, date)")
    justification_depenses = fields.Text(string="Justification des dépenses")

    # Timeline
    avancement = fields.Float(string="Avancement (%)", compute="_compute_avancement", store=True)
    etapes = fields.Text(string="Historique des étapes / commentaires")
    date_derniere_etape = fields.Datetime(string="Date dernière étape")

    @api.depends('giac_statut')
    def _compute_avancement(self):
        for rec in self:
            if rec.giac_statut == 'cloture':
                rec.avancement = 100
            elif rec.giac_statut == 'valide':
                rec.avancement = 50
            elif rec.giac_statut == 'en_cours':
                rec.avancement = 25
            elif rec.giac_statut == 'refuse':
                rec.avancement = 0
            else:
                rec.avancement = 0


    def action_ajouter_formations(self):
        for rec in self:
            if not rec.formations_selection_ids:
                raise UserError("Veuillez sélectionner au moins une formation.")
            already_declared = rec.formations_selection_ids.filtered(lambda f: f.declare_giac)
            if already_declared:
                raise UserError(
                    "Certaines formations sont déjà déclarées au GIAC : %s" %
                    ', '.join(already_declared.mapped('name'))
                )
            rec.formation_ids = [(4, f.id) for f in rec.formations_selection_ids]
            rec.formations_selection_ids = [(5, 0, 0)]

    def action_valider(self):
        for rec in self:
            if rec.giac_statut == 'valide':
                raise UserError("Ce dossier est déjà validé.")
            if rec.giac_statut == 'cloture':
                raise UserError("Un dossier cloturé ne peut pas etre validé.")
            if rec.giac_statut == 'refuse':
                raise UserError("Un dossier refusé ne peut pas etre validé.")
            rec.giac_statut = 'valide'
            rec.giac_date_validation = fields.Datetime.now()
            rec.giac_date_validation_dossier=fields.Datetime.now()
            rec.valide_par = self.env.user.id 
            rec.date_derniere_etape = fields.Datetime.now()
            rec.etapes = (rec.etapes or "") + "\n{}: Dossier validé".format(fields.Datetime.now())
            if rec.formation_ids:
                rec.formation_ids.write({
                    'declare_giac': True,
                    'giac_id': rec.id,
                    'giac_reference': rec.giac_reference,
                    'giac_statut': rec.giac_statut,
                    'giac_budget_accorde': rec.giac_budget_accorde,
                    'giac_budget_demande': rec.giac_budget_demande,
                    'giac_date_demande': rec.giac_date_demande,
                    'giac_date_validation': rec.giac_date_validation,
                    'giac_date_cloture': rec.giac_date_cloture,
                    'giac_organisme_agree': rec.giac_organisme_agree,
                    'giac_contact_responsable': rec.giac_contact_responsable,
                    'giac_programme_valide': rec.giac_programme_valide,
                    'giac_observations': rec.giac_observations,
                    'giac_commentaires_comite': rec.giac_commentaires_comite,
                    'responsable_giac_id': rec.responsable_giac_id.id,
                    'impact_formation': rec.impact_formation,
                    'plan_action_post_formation': rec.plan_action_post_formation,
                })
 
    def action_refuser(self):
        for rec in self:
        # Si déjà refusé, on bloque
            if rec.giac_statut == 'refuse':
                raise UserError("Ce dossier est déjà refusé.")
            if rec.giac_statut == 'valide':
                raise UserError("Un dossier validé ne peut pas etre refuse.")
            if rec.giac_statut == 'cloture':
                raise UserError("Ce dossier est déjà cloture.")
        
        # On change d'abord le statut pour que le formulaire se mette à jour
        rec.giac_statut = 'refuse'
        rec.giac_date_refus = fields.Datetime.now()
        rec.refuse_par = self.env.user.id  
        rec.date_derniere_etape = fields.Datetime.now()
        rec.etapes = (rec.etapes or "") + "\n{}: Dossier refusé".format(fields.Datetime.now())

        # Vérification du motif
        if not rec.Motif_temp:
            raise UserError("Veuillez saisir le motif de refus dans le champ temporaire.")
        
        # On applique le motif définitif et on vide le temporaire
        rec.Motif_refus = rec.Motif_temp
        rec.Motif_temp = False

        # On met à jour les formations
        if rec.formation_ids:
            rec.formation_ids.write({'declare_giac': False})

        

    def action_cloturer(self):
        for rec in self:
            if rec.giac_statut != 'valide':
                raise UserError("Seul un dossier validé peut être clôturé.")
            rec.giac_statut = 'cloture'
            rec.giac_date_cloture = fields.Datetime.now()
            rec.cloture_par = self.env.user.id  

            rec.date_derniere_etape = fields.Datetime.now()
            rec.etapes = (rec.etapes or "") + "\n{}: Dossier clôturé".format(fields.Datetime.now())
            if rec.formation_ids:
                rec.formation_ids.write({
                    'giac_statut': 'cloture',
                    'giac_date_cloture': rec.giac_date_cloture,
                    'declare_giac': True,
                    'giac_id': rec.id,
                    'giac_reference': rec.giac_reference,
                    'giac_budget_accorde': rec.giac_budget_accorde,
                    'giac_budget_demande': rec.giac_budget_demande,
                    'giac_date_demande': rec.giac_date_demande,
                    'giac_date_validation': rec.giac_date_validation,
                    'giac_organisme_agree': rec.giac_organisme_agree,
                    'giac_contact_responsable': rec.giac_contact_responsable,
                    'giac_programme_valide': rec.giac_programme_valide,
                    'giac_observations': rec.giac_observations,
                    'giac_commentaires_comite': rec.giac_commentaires_comite,
                    'responsable_giac_id': rec.responsable_giac_id.id,
                    'impact_formation': rec.impact_formation,
                    'plan_action_post_formation': rec.plan_action_post_formation,
                })

    budget_utilise = fields.Float(string="Budget utilisé", compute="_compute_budget_synthese", store=True)
    budget_restant = fields.Float(string="Budget restant", compute="_compute_budget_synthese", store=True)
    giac_pourcentage = fields.Float(string="% Budget GIAC accordé", compute="_compute_budget_synthese", store=True)
    total_financements = fields.Float(string="Total financements (GIAC + autres)", compute="_compute_budget_synthese", store=True)
    reste_a_charge = fields.Float(string="Reste à charge", compute="_compute_budget_synthese", store=True)
    budget_reel_total = fields.Float(string="Budget réel total", compute="_compute_budget_synthese", store=True)

    @api.depends('budget_initial', 'budget_reel', 'giac_budget_accorde', 'giac_budget_demande', 'autres_financements')
    def _compute_budget_synthese(self):
        for rec in self:
            # Budget total disponible : initial + autres financements
            total_disponible = (rec.budget_initial or 0.0) + (rec.autres_financements or 0.0)

            # Budget utilisé
            rec.budget_utilise = rec.budget_reel or 0.0

            # Budget restant
            rec.budget_restant = (rec.budget_initial or 0.0) - (rec.budget_reel or 0.0)

            # Pourcentage du budget GIAC accordé
            if rec.giac_budget_demande:
                rec.giac_pourcentage = min(100.0, (rec.giac_budget_accorde or 0.0) / rec.giac_budget_demande * 100)
            else:
                rec.giac_pourcentage = 0.0

            # Reste à charge pour l'entreprise
            rec.reste_a_charge = max(0.0, total_disponible - (rec.giac_budget_accorde or 0.0 + rec.autres_financements or 0.0))