# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import UserError

class AccidentTravail(models.Model):
    _name = "accident.travail"
    _description = "Accident de Travail"
    _order = "date_accident desc"
    _inherit = ['mail.thread']
    partie_corps = fields.Selection([
    ('tete', 'Tête'),
    ('cou', 'Cou'),
    ('epaule_droite', 'Épaule droite'),
    ('epaule_gauche', 'Épaule gauche'),
    ('bras_droit', 'Bras droit'),
    ('bras_gauche', 'Bras gauche'),
    ('main_droite', 'Main droite'),
    ('main_gauche', 'Main gauche'),
    ('poitrine', 'Poitrine / Torse'),
    ('dos', 'Dos'),
    ('ventre', 'Ventre / Abdomen'),
    ('bassin', 'Bassin / Hanche'),
    ('jambe_droite', 'Jambe droite'),
    ('jambe_gauche', 'Jambe gauche'),
    ('genou_droit', 'Genou droit'),
    ('genou_gauche', 'Genou gauche'),
    ('pied_droit', 'Pied droit'),
    ('pied_gauche', 'Pied gauche'),
    ], string="Partie du corps touchée")


    # Champs existants...
    dossier_id = fields.Many2one('dossier.accident.assurance', string="Dossier Assurance", ondelete='set null')

     # Champs pour suivre l'assurance
    assurance_declaree = fields.Boolean(string="Assurance déclarée", default=False)
    declare_par = fields.Many2one('res.users', string="Déclaré par")
    date_declaration = fields.Datetime(string="Date de déclaration")

    # Identification
    accident_code = fields.Char(
        string="ID Accident",
        required=True,
        copy=False,
        readonly=True,
        index=True,
        default=lambda self: 'New'
    )
    name = fields.Char(string="Référence", required=True)
    
    recurrence_risque = fields.Selection([
        ('faible', 'Faible'),
        ('moyen', 'Moyen'),
        ('eleve', 'Élevé')
    ], string="Risque de récurrence", default='faible', tracking=True)


    # Informations principales
    date_accident = fields.Date(string="Date de l'accident", required=True)  # à garder obligatoire si nécessaire
    date_Creation_Accident = fields.Datetime(string="Date de création d'accident", readonly=True)
    date_Cloture_Accident = fields.Datetime(string="Date de Clôture dossier accident", readonly=True)
    date_Assurance_Accident = fields.Datetime(string="Date Déclaration Assurance d'accident", readonly=True)
    date_Refus_Accident = fields.Datetime(string="Date Refus d'accident", readonly=True)


    heure_accident = fields.Float(string="Heure de l'accident")
    employe_id = fields.Many2one('hr.employee', string="Employé concerné", required=True)
    lieu_accident = fields.Char(string="Lieu de l'accident")
    description = fields.Text(string="Description de l'accident")
    cause_accident = fields.Text(string="Cause de l'accident")
    mesures_correctives = fields.Text(string="Mesures correctives")
    x_click = fields.Float(string="Position X")
    y_click = fields.Float(string="Position Y")

    montant_indemnisation = fields.Float(string="Montant d'indemnisation")


    # Champs calculés pour les statistiques
    total_accidents = fields.Integer(string="Total accidents", compute="_compute_stats", store=False, readonly=True)
    total_en_cours = fields.Integer(string="Accidents en cours", compute="_compute_stats", store=False, readonly=True)
    total_valides = fields.Integer(string="Accidents validés", compute="_compute_stats", store=False, readonly=True)
    total_refuses = fields.Integer(string="Accidents refusés", compute="_compute_stats", store=False, readonly=True)

    @api.depends('statutNouv')
    def _compute_stats(self):
        total = self.env['accident.travail'].search_count([])
        en_cours = self.env['accident.travail'].search_count([('statutNouv', '=', 'en_cours')])
        valides = self.env['accident.travail'].search_count([('statutNouv', '=', 'valide')])
        refuses = self.env['accident.travail'].search_count([('statutNouv', '=', 'refuse')])
        for record in self:
            record.total_accidents = total
            record.total_en_cours = en_cours
            record.total_valides = valides
            record.total_refuses = refuses

    # Détails de l’accident
    gravite = fields.Selection([
        ('leger', 'Léger'),
        ('moyen', 'Moyen'),
        ('grave', 'Grave'),
        ('mortel', 'Mortel')
    ], string="Gravité", default='leger')
    blessure = fields.Char(string="Nature de la blessure")
    hospitalisation = fields.Boolean(string="Hospitalisation nécessaire ?", default=False)
    type_accident = fields.Selection([
        ('chute', 'Chute'),
        ('coup', 'Coup / Impact'),
        ('brulure', 'Brûlure'),
        ('electrique', 'Électrique'),
        ('intoxication', 'Intoxication'),
        ('machine', 'Machine / Outil'),
        ('circulation', 'Accident de circulation'),
        ('autre', 'Autre')
    ], string="Type d'accident", default='autre')

    date_creation = fields.Date(string="Date Création", default=fields.Date.today)

    # Suivi médical
    temoins_ids = fields.Many2many(
    'hr.employee',
    string="Témoins de l'accident",
    help="Sélectionner les employés témoins de l'accident")    
    premier_soin = fields.Text(string="Premiers soins administrés")
    medecin_traitant = fields.Char(string="Médecin traitant")
    date_consultation = fields.Date(string="Date de la consultation médicale")
    certificat_medical = fields.Binary(string="Certificat médical", attachment=True)
 

    # Suivi RH / administratif
    service_id = fields.Many2one('hr.department', string="Service")
    poste_occupe = fields.Char(string="Poste occupé")
    anciennete = fields.Integer(string="Ancienneté (années)")
    commentaire = fields.Text(string="Commentaire")
    documents = fields.Binary(string="Documents joints", attachment=True)
    date_documents = fields.Datetime(string="Date soumission desdocuments", required=True)
    date_refus_documents = fields.Datetime(string="Date refus desdocuments")


    responsable_securite_id = fields.Many2one('hr.employee', string="Responsable Sécurité")

    date_reprise = fields.Date(string="Date de reprise prévue")

    # Date effective calculée (accident + prolongations)
    date_reprise_effective = fields.Date(
        string="Date de reprise effective",
        compute="_compute_dates_effectives",
        store=True,
        readonly=True
    )

    # Nombre de jours d'arrêt calculé
    jours_arret = fields.Integer(
        string="Nombre de jours d'arrêt",
        compute="_compute_dates_effectives",
        store=True,
        readonly=True
    )

    # Prolongations
    prolongation_ids = fields.One2many(
        'accident.travail.prolongation',
        'accident_id',
        string="Prolongations"
    )

    date_accident = fields.Date(string="Date de l'accident")

    @api.depends('prolongation_ids.date_fin', 'date_accident')
    def _compute_dates_effectives(self):
        for rec in self:
            if rec.prolongation_ids:
                # Récupérer la prolongation avec la date_fin la plus tardive
                derniere_prolongation = max(rec.prolongation_ids, key=lambda p: p.date_fin or rec.date_accident)
                rec.date_reprise_effective = derniere_prolongation.date_fin
            else:
                # Pas de prolongation → reprise = date prévue
                rec.date_reprise_effective = rec.date_reprise

            # Calcul du nombre de jours d’arrêt
            if rec.date_accident and rec.date_reprise_effective:
                rec.jours_arret = (rec.date_reprise_effective - rec.date_accident).days
            else:
                rec.jours_arret = 0

                
    incapacite_permanente = fields.Boolean(string="Incapacité permanente")
    taux_incapacite = fields.Float(string="Taux d’incapacité (%)")

    # Suivi administratif et légal
    numero_dossier = fields.Char(string="N° Dossier Assurance")
   
    organisme_assurance_id = fields.Many2one(
    'assurance.organisme',
    string="Organisme Assurance",
    ondelete='set null',
    help="Choisir l'organisme d'assurance responsable de l'accident")   

    declaration_cnas = fields.Boolean(string="Déclaration CNAS", default=False)
    date_declaration = fields.Date(string="Date de déclaration")
    pv_police = fields.Binary(string="PV Police", attachment=True)
    date_pv_police = fields.Date(string="Date PV Police")
    declarer_assurance = fields.Boolean(string="Déclaré Assurance ?", default=False, tracking=True)
    declarer_par = fields.Boolean(string="Déclaré Assurance par", default=False, tracking=True)


    # Aspects financiers
    cout_estime = fields.Float(string="Coût estimé de l’accident")
    remboursement = fields.Boolean(string="Remboursement accordé ?", default=False)
    montant_avance = fields.Float(string="Montant avancé")
    mode_paiement = fields.Selection([
        ('espece', 'Espèces'),
        ('virement', 'Virement bancaire'),
        ('cheque', 'Chèque'),
        ('autre', 'Autre')
    ], string="Mode de paiement")
    reglement_global = fields.Boolean(string="Règlement global effectué ?", default=False)
    montant_regle = fields.Float(string="Montant réglé")
    mode_reglement = fields.Selection([
        ('espece', 'Espèces'),
        ('virement', 'Virement bancaire'),
        ('cheque', 'Chèque'),
        ('autre', 'Autre')
    ], string="Mode du règlement")

    statutNouv = fields.Selection([
    ('en_cours', 'En cours'),
    ('valide', 'Validé'),
    ('refuse', 'Refusé')
    ], string="Statut", default='en_cours', tracking=True, required=True)


    responsable_id = fields.Many2one(
        'hr.employee',
        string="Responsable du dossier",
        default=lambda self: self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
    )


    date_validation = fields.Datetime(string="Date de validation")

    valide_par = fields.Many2one('res.users', string="Validé par")
    cloture_par = fields.Many2one('res.users', string="Cloturé par")
    refuse_par = fields.Many2one('res.users', string="Refuse par")
    assurance_par = fields.Many2one('res.users', string="Déclaré en assurance par")
    reste_a_regler = fields.Float(
        string="Reste à régler",
        compute="_compute_finances",
        store=True
    )

    ecart_cout = fields.Float(
        string="Écart avec coût estimé",
        compute="_compute_finances",
        store=True
    )

    prise_en_charge_assurance = fields.Float(
        string="Prise en charge Assurance",
        compute="_compute_finances",
        store=True
    )

    reste_a_charge_entreprise = fields.Float(
        string="Reste à charge Entreprise",
        compute="_compute_finances",
        store=True
    )

    @api.depends('montant_indemnisation', 'montant_avance', 'montant_regle', 'cout_estime')
    def _compute_finances(self):
        for rec in self:
            indemn = rec.montant_indemnisation or 0.0
            avance = rec.montant_avance or 0.0
            regle = rec.montant_regle or 0.0
            cout = rec.cout_estime or 0.0

            # 1. Ce que l’assurance prend en charge
            rec.prise_en_charge_assurance = indemn

            # 2. Ce qu’il reste à charge pour l’entreprise
            rec.reste_a_charge_entreprise = max(cout - indemn, 0.0)

            # 3. Ce qu’il reste encore à régler (par rapport au coût prévu)
            rec.reste_a_regler = max(cout - (indemn + avance + regle), 0.0)

            # 4. Écart entre payé (avance + regle + indemnisation) et coût estimé
            rec.ecart_cout = (avance + regle + indemn) - cout


    def action_valider(self):
        for record in self:
            if record.statutNouv == 'refuse':
                raise UserError("Un accident refusé ne peut pas être validé.")
            if record.statutNouv == 'valide':
                raise UserError("Cet accident est déjà validé.")
        record.statutNouv = 'valide'
        record.date_validation = fields.Datetime.now()
        record.valide_par = self.env.user
        return True

    def action_refuser(self):
        for record in self:
            if record.statutNouv == 'valide':
                raise UserError("Un accident validé ne peut pas être refusé.")
            if record.statutNouv == 'refuse':
                raise UserError("Cet accident est déjà refusé.")
        record.statutNouv = 'refuse'
        record.date_Refus_Accident = fields.Datetime.now()
        record.refuse_par = self.env.user
        return True

    def action_assurance(self):
        for record in self:
            if record.statutNouv == 'refuse':
                raise UserError("Un accident refusé ne peut pas etre assuré")
            if record.statutNouv == 'cloture':
                raise UserError("Cet accident est deja cloture")
            record.declarer_assurance = True
            record.date_Assurance_Accident = fields.Datetime.now()
            record.assurance_par = self.env.user
        return {
        'type': 'ir.actions.client',
        'tag': 'display_notification',
        'params': {
            'title': 'Succès',
            'message': "L’accident a été déclaré avec succès !, n'oubliez pas de déclarer l'organisme de l'assurance et le numéro de dossier",
            'type': 'success',
            'sticky': False,
        }
    }
    # ---------------- Création ----------------
    @api.model
    def create(self, vals):
        if vals.get('accident_code', 'New') == 'New':
            vals['accident_code'] = self.env['ir.sequence'].next_by_code('accident.travail') or 'New'
        if not vals.get('date_Creation_Accident'):
            vals['date_Creation_Accident'] = fields.Datetime.now()  
        return super(AccidentTravail, self).create(vals)
    
    
    
