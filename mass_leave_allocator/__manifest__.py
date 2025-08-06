# -*- coding: utf-8 -*-
{
    'name': 'Mass Leave Allocator',
    'version': '1.0',
    'summary': 'Allocate leave to multiple employees at once',
    'category': 'Human Resources',
    'depends': ['hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/mass_leave_allocation_menu.xml',
        'views/mass_leave_allocation_wizard_view.xml',
    ],
    'installable': True,
    'application': True,
}
