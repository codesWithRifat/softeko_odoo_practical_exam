{
    'name': 'Product Price History',
    'version': '18.0.1.0.0',
    'category': 'Sales',
    'summary': 'Customer-specific Product Price History on Quotation',
    'description': """
        This module adds functionality to display customer-specific product price history 
        within the sales order form, without modifying the standard Sales app.
        
        Features:
        - View price history for specific product and customer combinations
        - Multiple UI options: smart button, inline button, and collapsible section
        - Advanced filtering by date range
        - "Use Last Price" functionality
        - Integration with existing sale.report model
    """,
    'author': 'Your Company',
    'depends': [
        'base',
        'sale',
        'sale_management',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}