{
    'name': 'Leave Approval Notifier',
    'version': '18.0.0.0',
    'summary': 'Multi-level leave approval with HR notification',
    'description': """
        Allows employees to apply for leave, managers to approve,
        and automatically notifies HR after approval.
    """,
    'author': 'Humayra,Rifat, Lamia',
    'depends': ['hr', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/security_rules.xml',
        'views/leave_request_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}