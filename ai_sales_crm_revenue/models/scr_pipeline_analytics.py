from odoo import api, fields, models


class ScrPipelineAnalytics(models.Model):
    _name = 'scr.pipeline.analytics'
    _description = 'AI Pipeline Analytics'
    _order = 'period desc'
    _inherit = ['mail.thread']

    name = fields.Char(string='Reference', required=True, tracking=True)
    period = fields.Char(string='Period', tracking=True, help="e.g. 2025-Q1, 2025-01")
    total_pipeline = fields.Monetary(string='Total Pipeline', currency_field='currency_id', tracking=True)
    weighted_pipeline = fields.Monetary(
        string='Weighted Pipeline',
        currency_field='currency_id',
        tracking=True,
        help="Pipeline weighted by probability",
    )
    avg_deal_size = fields.Monetary(string='Average Deal Size', currency_field='currency_id', tracking=True)
    win_rate = fields.Float(string='Win Rate (%)', tracking=True, help="Win rate 0-100")
    sales_cycle_days = fields.Integer(string='Sales Cycle (Days)', tracking=True)
    ai_forecast = fields.Monetary(string='AI Forecast', currency_field='currency_id', tracking=True)
    team_id = fields.Many2one('res.users', string='Sales Team / Owner', tracking=True)
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'The reference must be unique.'),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('scr.pipeline.analytics') or '/'
        return super().create(vals_list)
