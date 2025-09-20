from odoo import models, fields, api

class FormationFormateur(models.Model):
    _name = "formation.formateur"
    _description = "Formateur de la formation"
    _inherit = ['mail.thread', 'mail.activity.mixin']  # suivi et chatter

    module_ids = fields.Many2many(
    'formation.module',
    'formateur_module_rel',
    'formateur_id',
    'module_id',
    string="Modules associés",
    tracking=True
    )
    # ==========================
    # Infos générales
    # ==========================
    name = fields.Char(string="Nom complet", required=True, tracking=True)
    type_formateur = fields.Selection([
        ('interne', 'Interne (de l’entreprise)'),
        ('externe', 'Externe (non GIAC)'),
        ('giac', 'Externe agréé GIAC'),
    ], string="Type de formateur", required=True, default='externe', tracking=True)
    organisme_id = fields.Many2one('formation.organisme', string="Organisme / Société")
    fonction = fields.Char(string="Poste / Fonction")
    contact_email = fields.Char(string="Email")
    contact_phone = fields.Char(string="Téléphone")
    adresse = fields.Char(string="Adresse")
    domaine = fields.Char(string="Domaine d’expertise", tracking=True)
    photo = fields.Binary(string="Photo", attachment=True)

    # ==========================
    # Infos administratives
    # ==========================
    cin = fields.Char(string="CIN / Identifiant")
    diplome = fields.Char(string="Diplôme principal")
    certifications = fields.Text(string="Certifications obtenues")
    experience = fields.Integer(string="Années d’expérience")
    cv_document = fields.Binary(string="CV du formateur", attachment=True)

    # ==========================
    # Suivi GIAC
    # ==========================
    certification_giac = fields.Boolean(string="Agréé GIAC ?")
    num_agrement_giac = fields.Char(string="Numéro d’agrément GIAC")
    date_agrement = fields.Date(string="Date d’agrément")
    date_expiration_agrement = fields.Date(string="Date d’expiration agrément")
    documents_giac = fields.Binary(string="Documents GIAC", attachment=True)

    # ==========================
    # Tarification
    # ==========================
    tarif_horaire = fields.Float(string="Tarif horaire (MAD)")
    tarif_journalier = fields.Float(string="Tarif journalier (MAD)")
    devise_id = fields.Many2one('res.currency', string="Devise", default=lambda self: self.env.company.currency_id.id)

    # ==========================
    # Lien avec les formations
    # ==========================
    formation_ids = fields.One2many('formation.employe', 'formateur_id', string="Formations animées")
    note = fields.Text(string="Notes internes")

    # ==========================
    # Évaluations
    # ==========================
    
    # ==========================
    # Disponibilité
    # ==========================
    disponibilite = fields.Selection([
        ('disponible', 'Disponible'),
        ('occupe', 'Occupé'),
        ('indisponible', 'Indisponible')
    ], string="Disponibilité", default="disponible")

   
