from odoo import api, fields, models


class ScrRevenueForecast(models.Model):
    _name = 'scr.revenue.forecast'
    _description = 'AI Revenue Forecast'
    _order = 'period desc'
    _inherit = ['mail.thread']

    name = fields.Char(string='Reference', required=True, tracking=True)
    period = fields.Char(string='Period', tracking=True, help="e.g. 2025-Q1, 2025-01")
    forecast_amount = fields.Monetary(string='Forecast Amount', currency_field='currency_id', tracking=True)
    actual_amount = fields.Monetary(string='Actual Amount', currency_field='currency_id', tracking=True)
    variance = fields.Monetary(
        string='Variance',
        currency_field='currency_id',
        compute='_compute_variance',
        store=True,
        tracking=True,
    )
    ai_confidence = fields.Float(string='AI Confidence (%)', tracking=True, help="Confidence level 0-100")
    scenario = fields.Selection(
        [('conservative', 'Conservative'),
         ('base', 'Base'),
         ('optimistic', 'Optimistic')],
        string='Scenario',
        default='base',
        tracking=True,
    )
    product_category_id = fields.Many2one('product.category', string='Product Category', tracking=True)
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'The reference must be unique.'),
    ]

    @api.depends('forecast_amount', 'actual_amount')
    def _compute_variance(self):
        for record in self:
            record.variance = (record.actual_amount or 0.0) - (record.forecast_amount or 0.0)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('scr.revenue.forecast') or '/'
        return super().create(vals_list)
