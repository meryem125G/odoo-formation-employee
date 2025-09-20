from odoo import models, fields, api

class FormationEmployeModuleLine(models.Model):
    _name = 'formation.employe.module.line'
    _description = 'Formateur et module d’une formation'

    formation_id = fields.Many2one(
        'formation.employe',
        string="Formation",
        required=True,
        ondelete='cascade'
    )
    theme_id = fields.Many2one('formation.theme', string="Thème")
    module_id = fields.Many2one('formation.module', string="Module")
    
    # tarifs
    tarif_modules = fields.Float(string="Tarif selon Modules", compute="_compute_tarifs", store=True)
    tarif_formateurs = fields.Float(string="Tarif selon Formateurs", compute="_compute_tarifs", store=True)
    

     # autres champs
    autres_frais = fields.Float(string="Autres frais")
    cout = fields.Float(string="Coût réel de la formation")
    budget_alloue = fields.Float(string="Budget alloué")
     # champs booléens pour comparer
    budget_modules_ok = fields.Boolean(string="Modules dans budget alloué", compute="_compute_budget_reel", store=True)
    budget_formateurs_ok = fields.Boolean(string="Formateurs dans budget alloué", compute="_compute_budget_reel", store=True)
    
    # budgets réels calculés
    budget_reel_modules = fields.Float(string="Budget réel Modules", compute="_compute_budget_reel", store=True)
    budget_reel_formateurs = fields.Float(string="Budget réel Formateurs", compute="_compute_budget_reel", store=True)
    
    # Multiple formateurs pour le module
    formateur_ids = fields.Many2many(
        'formation.formateur',
        'module_line_formateur_rel',
        'module_line_id',
        'formateur_id',
        string="Formateurs"
    )

    duree = fields.Float(string="Durée (heures)")
    
      # Domaines dynamiques pour la vue
    module_domain_ids = fields.Many2many('formation.module', compute='_compute_module_domain')
    formateur_domain_ids = fields.Many2many('formation.formateur', compute='_compute_formateur_domain')
    marge_modules = fields.Float(string="Marge Modules", compute="_compute_budget_reel", store=True)
    marge_formateurs = fields.Float(string="Marge Formateurs", compute="_compute_budget_reel", store=True)
    marge_totale = fields.Float(string="Marge Totale", compute="_compute_budget_reel", store=True)
    
    @api.depends('tarif_modules', 'tarif_formateurs', 'autres_frais')
    def _compute_budget_reel(self):
       for line in self:
        # Budget réel incluant autres frais
        line.budget_reel_modules = (line.tarif_modules or 0.0) + (line.autres_frais or 0.0)
        line.budget_reel_formateurs = (line.tarif_formateurs or 0.0) + (line.autres_frais or 0.0)
        line.cout = line.budget_reel_modules + line.budget_reel_formateurs

        # Comparaison avec budget alloué (ligne spécifique)
        if line.budget_alloue:
            line.budget_modules_ok = line.budget_alloue >= line.budget_reel_modules
            line.budget_formateurs_ok = line.budget_alloue >= line.budget_reel_formateurs

        # Calcul de la marge pour la ligne
        line.marge_modules = (line.budget_alloue - line.budget_reel_modules) if line.budget_alloue else 0.0
        line.marge_formateurs = (line.budget_alloue - line.budget_reel_formateurs) if line.budget_alloue else 0.0
        line.marge_totale = (line.budget_alloue - line.cout) if line.budget_alloue else 0.0
            

   

    @api.depends('module_id', 'duree', 'formateur_ids', 'formateur_ids.tarif_horaire')
    def _compute_tarifs(self):
        for line in self:
            # Tarif selon modules
            if line.module_id and line.duree:
                line.tarif_modules = (line.module_id.cout_par_heure or 0.0) * (line.duree or 0.0)
            else:
                line.tarif_modules = 0.0

            # Tarif selon formateurs
            total_formateur = 0.0
            for formateur in line.formateur_ids:
                total_formateur += (formateur.tarif_horaire or 0.0) * (line.duree or 0.0)
            line.tarif_formateurs = total_formateur


    @api.onchange('formation_id')
    def _onchange_formation_id(self):
        if self.formation_id and self.formation_id.theme_id:
            self.theme_id = self.formation_id.theme_id

    @api.depends('formation_id', 'theme_id')
    def _compute_module_domain(self):
        for line in self:
            if line.formation_id:
                # Modules déjà choisis dans d'autres lignes
                selected_modules = line.formation_id.module_line_ids.filtered(lambda l: l.id != line.id).mapped('module_id')
                domain_modules = line.env['formation.module'].search([('id', 'not in', selected_modules.ids)])
                if line.theme_id:
                    domain_modules = domain_modules.filtered(lambda m: m.theme_id.id == line.theme_id.id)
                line.module_domain_ids = domain_modules
            else:
                line.module_domain_ids = line.env['formation.module'].browse([])

    @api.depends('module_id')
    def _compute_formateur_domain(self):
        for line in self:
            if line.module_id:
                formateurs = line.env['formation.formateur'].search([('module_ids', 'in', line.module_id.id)])
                line.formateur_domain_ids = formateurs
            else:
                line.formateur_domain_ids = line.env['formation.formateur'].browse([])

    @api.onchange('theme_id', 'module_id')
    def _onchange_theme_module(self):
        """Filtrer les modules par thème, les formateurs par module et éviter les doublons"""
        res = {'domain': {}}

        # Modules déjà choisis
        if self.formation_id:
            selected_modules = self.formation_id.module_line_ids.filtered(lambda l: l.id != self.id).mapped('module_id')
            domain_module = [('id', 'not in', selected_modules.ids)]
            if self.theme_id:
                domain_module.append(('theme_id', '=', self.theme_id.id))
            res['domain']['module_id'] = domain_module

        # Filtrer les formateurs selon le module choisi
        if self.module_id:
            res['domain']['formateur_ids'] = [('module_ids', 'in', self.module_id.id)]
        else:
            res['domain']['formateur_ids'] = []

        return res