from odoo import models, fields, api

class MassLeaveAllocationWizard(models.TransientModel):
    _name = "mass.leave.allocation.wizard"
    _description = "Mass Leave Allocation Wizard"

    leave_type_id = fields.Many2one('hr.leave.type', required=True)
    number_of_days = fields.Float(string="Number of Days", required=True)
    allocation_mode = fields.Selection([
        ('all', 'All Employees'),
        ('by_department', 'By Department'),
        ('by_job', 'By Job Title')
    ], required=True)
    department_id = fields.Many2one('hr.department')
    job_id = fields.Many2one('hr.job')
    allocation_reason = fields.Text(string="Reason")

    def action_allocate(self):
        domain = []
        if self.allocation_mode == 'by_department' and self.department_id:
            domain.append(('department_id', '=', self.department_id.id))
        elif self.allocation_mode == 'by_job' and self.job_id:
            domain.append(('job_id', '=', self.job_id.id))

        employees = self.env['hr.employee'].search(domain)

        for emp in employees:
            self.env['hr.leave'].create({
                'employee_id': emp.id,
                'holiday_status_id': self.leave_type_id.id,
                'number_of_days': self.number_of_days,
                'holiday_type': 'employee',
                'request_date_from': fields.Date.today(),
                'request_date_to': fields.Date.today(),
                'state': 'validate',
                'name': self.allocation_reason or "Mass Leave Allocation"
            })
