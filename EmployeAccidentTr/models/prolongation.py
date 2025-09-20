# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError
class AccidentTravailProlongation(models.Model):
    _name = "accident.travail.prolongation"
    _description = "Prolongation accident de travail"

    accident_id = fields.Many2one('accident.travail', string="Accident concerné", ondelete='cascade')
    date_debut = fields.Date(string="Date début prolongation", required=True)
    date_fin = fields.Date(string="Date fin prolongation", required=True)
    nb_jours = fields.Integer(string="Nombre de jours", compute="_compute_nb_jours", store=True)

    @api.depends('date_debut', 'date_fin')
    def _compute_nb_jours(self):
        for rec in self:
            if rec.date_debut and rec.date_fin:
                rec.nb_jours = (rec.date_fin - rec.date_debut).days + 1
            else:
                rec.nb_jours = 0
