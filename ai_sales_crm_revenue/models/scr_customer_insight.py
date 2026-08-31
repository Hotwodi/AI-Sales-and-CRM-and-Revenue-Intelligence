from odoo import api, fields, models


class ScrCustomerInsight(models.Model):
    _name = 'scr.customer.insight'
    _description = 'AI Customer Insight'
    _order = 'ltv desc'
    _inherit = ['mail.thread']

    name = fields.Char(string='Reference', required=True, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Customer', tracking=True)
    ltv = fields.Monetary(string='Lifetime Value (LTV)', currency_field='currency_id', tracking=True)
    churn_risk = fields.Float(string='Churn Risk (%)', tracking=True, help="Risk of churn 0-100")
    engagement_score = fields.Float(string='Engagement Score', tracking=True, help="Engagement score 0-100")
    ai_segment = fields.Selection(
        [('vip', 'VIP'),
         ('growth', 'Growth'),
         ('stable', 'Stable'),
         ('at_risk', 'At Risk')],
        string='AI Segment',
        tracking=True,
    )
    last_purchase = fields.Date(string='Last Purchase', tracking=True)
    recommended_actions = fields.Text(string='Recommended Actions', help="AI-suggested actions for this customer")
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'The reference must be unique.'),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('scr.customer.insight') or '/'
        return super().create(vals_list)
