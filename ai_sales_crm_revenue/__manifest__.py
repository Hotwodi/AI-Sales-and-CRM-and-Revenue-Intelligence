{
    'name': 'AI Sales, CRM & Revenue Intelligence',
    'version': '18.0.1.0.0',
    'images': ['static/description/cover.png'],
    'category': 'Productivity/AI',
    'summary': 'AI-powered lead scoring, revenue forecasting, customer insights, pipeline analytics, and churn prediction',
    'description': """
AI Sales, CRM & Revenue Intelligence
=====================================

Transform your sales process with AI-driven insights:
- AI Lead Scoring with conversion probability and recommendations
- Revenue Forecasting with confidence levels and scenario planning
- Customer Insights with LTV, churn risk, and AI segmentation
- Pipeline Analytics with weighted pipeline and win-rate analysis
- Churn Prediction with risk factors and retention actions
""",
    'author': 'SoftaiDev',
    'website': 'https://softaidev.pages.dev',
    'license': 'LGPL-3',
    'price': 599.99,
    'currency': 'USD',
    'application': True,
    'installable': True,
    'depends': ['base', 'web', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/lead_score_views.xml',
        'views/revenue_forecast_views.xml',
        'views/customer_insight_views.xml',
        'views/pipeline_analytics_views.xml',
        'views/churn_prediction_views.xml',
        'views/menu.xml',
    ],
}
