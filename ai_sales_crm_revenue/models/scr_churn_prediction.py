from odoo import api, fields, models


class ScrChurnPrediction(models.Model):
    _name = 'scr.churn.prediction'
    _description = 'AI Churn Prediction'
    _order = 'churn_probability desc'
    _inherit = ['mail.thread']

    name = fields.Char(string='Reference', required=True, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Customer', tracking=True)
    churn_probability = fields.Float(string='Churn Probability (%)', tracking=True, help="Probability 0-100")
    risk_factors = fields.Text(string='Risk Factors', help="Factors contributing to churn risk")
    last_activity = fields.Datetime(string='Last Activity', tracking=True)
    days_inactive = fields.Integer(string='Days Inactive', tracking=True)
    ai_confidence = fields.Float(string='AI Confidence (%)', tracking=True, help="Confidence level 0-100")
    state = fields.Selection(
        [('active', 'Active'),
         ('at_risk', 'At Risk'),
         ('churned', 'Churned'),
         ('saved', 'Saved')],
        string='Status',
        default='active',
        tracking=True,
    )
    retention_action = fields.Text(string='Retention Action', help="Recommended retention action")
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'The reference must be unique.'),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('scr.churn.prediction') or '/'
        return super().create(vals_list)

    def action_mark_saved(self):
        """Mark a churned/at-risk customer as saved after retention action."""
        self.write({'state': 'saved'})
        return True
