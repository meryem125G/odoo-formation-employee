# -*- coding: utf-8 -*-
from odoo import http

class FormationController(http.Controller):
    @http.route('/formation', auth='public', website=True)
    def formation_page(self, **kwargs):
        return http.request.render('FormationEmploye.formation_page')
