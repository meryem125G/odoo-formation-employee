# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError

class DossierAccidentAssurance(models.Model):
    _name = "dossier.accident.assurance"
    _description = "Dossier Accident Assurance"
    _order = "date_creation desc"

    # ============================
    # Champs principaux
    # ============================
    name = fields.Char(string="Numéro de dossier", required=True, copy=False)
    date_creation = fields.Datetime(string="Date de création", default=fields.Datetime.now)
    date_declaration_assurance = fields.Datetime(string="Date de déclaration dans assurance")
    date_cloture = fields.Datetime(string="Date de clôture du dossier")
    statut = fields.Selection([
        ('en_cours', 'En cours'),
        ('valide', 'Validé'),
        ('refuse', 'Refusé'),
        ('cloture', 'Clôturé')
    ], string="Statut du dossier", default='en_cours', tracking=True)
    commentaires = fields.Text(string="Commentaires généraux")

    # ============================
    # Liens avec accidents
    # ============================
    accidents_ids = fields.One2many(
        'accident.travail',
        'dossier_id',
        string="Accidents liés au dossier"
    )
    accidents_selection_ids = fields.Many2many(
    'accident.travail',
    string="Sélection des accidents",
    domain="[('statutNouv','=','valide'),('dossier_id','=',False)]",
  
)

    Motif_temp = fields.Text(string="Motif temporaire", help="Saisir le motif avant validation")
    Motif_refus = fields.Text(string="Motif de refus", readonly=True)

    # ============================
    # Assurance
    # ============================
    organisme_assurance_id = fields.Many2one('assurance.organisme', string="Organisme d'assurance", required=True)
    contact_assurance_id = fields.Many2one(
        'assurance.contact',
        string="Contact assurance",
        domain="[('organisme_id', '=', organisme_assurance_id)]"
    )
    numero_police = fields.Char(string="Numéro de police / contrat")
    montant_indemnisation = fields.Float(string="Montant d'indemnisation estimé")
    documents_ids = fields.Many2many('ir.attachment', string="Documents liés au dossier")

    # ============================
    # Suivi et validation
    # ============================
    responsable = fields.Many2one('res.users', string="Créé par", default=lambda self: self.env.user)
    valide_par = fields.Many2one('res.users', string="Validé par")
    date_validation = fields.Datetime(string="Date de validation")
    notes_suivi = fields.Text(string="Notes de suivi")

    # ============================
    # Liens avec employés / entreprise
    # ============================
    employe_ids = fields.Many2many('hr.employee', string="Employés concernés")
    entreprise_id = fields.Many2one('res.company', string="Entreprise concernée")

    # ============================
    # Calculs
    # ============================
    total_accidents = fields.Integer(string="Nombre d'accidents liés", compute='_compute_total_accidents', store=True)
    montant_total_accidents = fields.Float(string="Montant total accidents", compute='_compute_total_accidents', store=True)

    cloture_par = fields.Many2one('res.users', string="Cloturé par")
    refuse_par = fields.Many2one('res.users', string="Refusé par")
    date_refus = fields.Datetime(string="Date de refus de dossier")



    @api.depends('accidents_ids', 'accidents_ids.montant_indemnisation')
    def _compute_total_accidents(self):
        for record in self:
            record.total_accidents = len(record.accidents_ids)
            record.montant_total_accidents = sum(record.accidents_ids.mapped('montant_indemnisation'))

    # ============================
    # Actions sur le statut
    # ============================
    def action_valider(self):
        for record in self:
            if record.statut=="valide":
                raise UserError("Le dossier est déjà validé.")
            if record.statut=="refuse":
                raise UserError("Ce dossier est refusé.")
            if record.statut=="cloture":
                raise UserError("Ce dossier est déjà cloturé.")
            
            record.statut = 'valide'
            record.valide_par = self.env.user
            record.date_validation = fields.Datetime.now()
            record.date_declaration_assurance = fields.Datetime.now()
            
            for accident in record.accidents_ids:
                # Marquer accident comme déclaré
                accident.assurance_declaree = True
                accident.declare_par = self.env.user
                accident.declarer_par = self.env.user

                accident.date_declaration = fields.Datetime.now()


                # Copier les infos du dossier vers l'accident
                accident.numero_dossier = record.name
                accident.organisme_assurance_id = record.organisme_assurance_id.id
                accident.date_Assurance_Accident = record.date_declaration_assurance
                accident.montant_indemnisation = record.montant_indemnisation
                


    def action_ajouter_accidents(self):
        for record in self:
            if not record.accidents_selection_ids:
                raise UserError("Veuillez sélectionner au moins un accident à ajouter.")
            for accident in record.accidents_selection_ids:
                if accident.assurance_declaree:
                    raise UserError(f"L’accident {accident.name} est déjà déclaré par une assurance.")
                accident.dossier_id = record.id  # l'accident prend le dossier actuel
            record.accidents_selection_ids = [(5, 0, 0)]  # vide la sélection
        return True

    def action_refuser(self):
        for record in self:
            if record.statut=="refuse":
                raise UserError("Le dossier est déjà refusé.")
            if record.statut=="valide":
                raise UserError("Ce dossier est déja validé.")
            if record.statut=="cloture":
                raise UserError("Un dossier cloturé ne peut pas etre refusé.")
        
        # Changer d'abord le statut pour que le formulaire se mette à jour
            record.statut = 'refuse'
        # Vérification que le motif temporaire est rempli
            if not record.Motif_temp:
                raise UserError("Veuillez saisir le motif de refus dans le champ temporaire.")

        # Transférer le motif temporaire vers le champ définitif
            record.Motif_refus = record.Motif_temp
            record.Motif_temp = False  # vider le champ temporaire
            record.refuse_par=self.env.user
            record.date_refus=fields.Datetime.now()

        # Retirer le lien dossier_id de tous les accidents liés
            for accident in record.accidents_ids:
                accident.dossier_id = False
                accident.assurance_declaree = False
                

    def action_cloturer(self):
        for record in self:
            if record.statut=="cloture":
                raise UserError("Le dossier est déjà cloture.")
            if record.statut=="refuse":
                raise UserError("Ce dossier est refusé.")
            if record.statut=="en_cours":
                raise UserError("Le dossier n'est pas validé encore")
            record.statut = 'cloture'
            record.date_cloture = fields.Datetime.now()
            record.cloture_par = self.env.user

