# -*- coding: utf-8 -*-
from odoo import models, fields
class AssuranceContact(models.Model):
    _name = "assurance.contact"
    _description = "Contact d'un organisme d'assurance"
    _rec_name = "name"

    # Informations principales
    name = fields.Char(string="Nom et prénom", required=True, help="Nom complet du contact")
    fonction = fields.Char(string="Fonction", help="Rôle ou fonction dans l'organisme")
    email = fields.Char(string="Email principal")
    email_secondaire = fields.Char(string="Email secondaire")
    telephone_fixe = fields.Char(string="Téléphone fixe")
    telephone_mobile = fields.Char(string="Téléphone mobile")
    adresse = fields.Text(string="Adresse du contact")
    notes = fields.Text(string="Notes internes")
    actif = fields.Boolean(string="Actif", default=True)

    # Relation avec l'organisme
    organisme_id = fields.Many2one(
        'assurance.organisme',
        string="Organisme d'assurance",
        ondelete='cascade',
        required=True,
        help="Organisme auquel ce contact est rattaché"
    )
