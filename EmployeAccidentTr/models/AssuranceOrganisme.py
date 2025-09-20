# -*- coding: utf-8 -*-
from odoo import models, fields, api

class AssuranceOrganisme(models.Model):
    _name = "assurance.organisme"
    _description = "Organisme d'Assurance"
    _rec_name = "name"  # Pour afficher le nom dans les relations Many2one

    # Informations générales
    name = fields.Char(string="Nom de l'organisme", required=True)
    code = fields.Char(string="Code interne", help="Code unique de l'organisme pour suivi interne")
    type_assurance = fields.Selection([
        ('sante', 'Assurance santé'),
        ('accident', 'Assurance accident'),
        ('vie', 'Assurance vie'),
        ('multirisque', 'Assurance multirisque'),
        ('autre', 'Autre')
    ], string="Type d'assurance", default='accident')
    description = fields.Text(string="Description / Informations complémentaires")
    
    # Coordonnées
    telephone = fields.Char(string="Téléphone")
    fax = fields.Char(string="Fax")
    email = fields.Char(string="Email")
    site_web = fields.Char(string="Site web")
    adresse = fields.Text(string="Adresse")

    # Contacts internes / responsables
    contact_person_ids = fields.One2many(
        'assurance.contact',
        'organisme_id',
        string="Personnes de contact"
    )

    accident_ids = fields.One2many(
    'accident.travail',
    'organisme_assurance_id',  # Maintenant ça existe
    string="Accidents déclarés"
)


    actif = fields.Boolean(string="Actif", default=True, help="Si l'organisme est toujours actif dans le système")
