from odoo import models, fields , api

class FormationOrganisme(models.Model):
    _name = "formation.organisme"
    _description = "Organisme de formation"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # =======================
    # Informations générales
    # =======================
    name = fields.Char(string="Nom de l’organisme", required=True, tracking=True)
    code_ref = fields.Char(string="Code interne / Référence")
    logo = fields.Binary(string="Logo", attachment=True)

    responsable = fields.Char(string="Responsable / Contact principal")
    email = fields.Char(string="Email principal")
    phone = fields.Char(string="Téléphone principal")
    mobile = fields.Char(string="Mobile")
    fax = fields.Char(string="Fax")
    adresse = fields.Char(string="Adresse")
    ville = fields.Char(string="Ville")
    pays_id = fields.Many2one("res.country", string="Pays")
    site_web = fields.Char(string="Site web")

    # =======================
    # Informations légales
    # =======================
    rc = fields.Char(string="Registre de commerce")
    ice = fields.Char(string="Identifiant Commun de l’Entreprise (ICE)")
    ifu = fields.Char(string="Identifiant Fiscal / TVA")
    statut_juridique = fields.Selection([
        ('sarl', 'SARL'),
        ('sa', 'SA'),
        ('sasu', 'SASU'),
        ('association', 'Association'),
        ('autre', 'Autre')
    ], string="Statut juridique")

    # =======================
    # Accréditations et agréments
    # =======================
    agrement_giac = fields.Boolean(string="Agréé GIAC ?")
    num_agrement = fields.Char(string="Numéro d’agrément")
    date_agrement = fields.Date(string="Date d’agrément")
    date_expiration_agrement = fields.Date(string="Expiration agrément")
    certifications = fields.Text(string="Certifications et accréditations (ISO, Qualiopi, etc.)")
    document_agrement = fields.Binary(string="Document d’agrément", attachment=True)

    # =======================
    # Suivi qualité
    # =======================
    evaluation_moyenne = fields.Float(string="Note moyenne (sur 5)", digits=(2, 1))
    nb_formations_realisees = fields.Integer(
    string="Nombre de formations réalisées",
    compute="_compute_nb_formations_realisees",
    store=True
)

    

    taux_satisfaction = fields.Float(string="Taux de satisfaction (%)")
    commentaires_evaluation = fields.Text(string="Commentaires des évaluations")

    # =======================
    # Liens internes
    # =======================
    formateur_ids = fields.One2many('formation.formateur', 'organisme_id', string="Formateurs")
    formation_ids = fields.One2many('formation.employe', 'organisme_id', string="Formations réalisées")

    # =======================
    # Suivi administratif
    # =======================
    statut = fields.Selection([
        ('actif', 'Actif'),
        ('inactif', 'Inactif'),
        ('suspendu', 'Suspendu')
    ], string="Statut", default="actif", tracking=True)

    note = fields.Text(string="Notes internes")
    @api.depends('formation_ids')
    def _compute_nb_formations_realisees(self):
        for rec in self:
            # recalcule le nombre de formations liées
            rec.nb_formations_realisees = self.env['formation.employe'].search_count([('organisme_id','=',rec.id)])