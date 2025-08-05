{
    "name": "Mass Leave Allocator",
    "version": "1.0",
    "summary": "Allocate leave to multiple employees at once",
    "category": "Human Resources",
    "depends": ["hr_holidays"],
    "data": [
        "security/ir.model.access.csv",
        'views/action.xml',
         "views/menu.xml"
        "wizard/mass_leave_allocation_wizard_view.xml",
       
    ],
    "installable": True,
    "application": True,
    "auto_install": False
}
