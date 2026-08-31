from odoo import api, fields, models


class ScrLeadScore(models.Model):
    _name = 'scr.lead.score'
    _description = 'AI Lead Scoring'
    _order = 'score desc, last_scored desc'
    _inherit = ['mail.thread']

    name = fields.Char(string='Reference', required=True, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Customer/Prospect', tracking=True)
    lead_source = fields.Char(string='Lead Source', tracking=True)
    score = fields.Float(string='AI Score', tracking=True, help="AI-computed score from 0 to 100")
    score_factors = fields.Text(string='Score Factors', help="Breakdown of factors contributing to the score")
    ai_recommendation = fields.Selection(
        [('pursue', 'Pursue'),
         ('nurture', 'Nurture'),
         ('disqualify', 'Disqualify')],
        string='AI Recommendation',
        tracking=True,
    )
    last_scored = fields.Datetime(string='Last Scored', tracking=True)
    conversion_probability = fields.Float(
        string='Conversion Probability (%)',
        tracking=True,
        help="Estimated probability of conversion (0-100)",
    )
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'The reference must be unique.'),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('scr.lead.score') or '/'
        return super().create(vals_list)

    def action_rescore(self):
        """Re-run AI scoring for selected records."""
        for record in self:
            record.last_scored = fields.Datetime.now()
        return True
