from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class LeaveRequest(models.Model):
    _name = 'leave.request'
    _description = 'Leave Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    employee_id = fields.Many2one(
        'hr.employee',
        string='Employee',
        default=lambda self: self.env.user.employee_id,
        required=True,
        readonly=True,
        states={'draft': [('readonly', False)]}
    )
    leave_type = fields.Selection(
        selection=[
            ('annual', 'Annual Leave'),
            ('sick', 'Sick Leave'),
            ('unpaid', 'Unpaid Leave'),
            ('other', 'Other'),
        ],
        string='Leave Type',
        required=True,
        default='annual'
    )
    from_date = fields.Date(string='From Date', required=True)
    to_date = fields.Date(string='To Date', required=True)
    reason = fields.Text(string='Reason', required=True)
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('submitted', 'Submitted'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        string='Status',
        default='draft',
        tracking=True
    )
    manager_comments = fields.Text(string='Manager Comments')
    manager_id = fields.Many2one(
        'res.users',
        string='Manager',
        compute='_compute_manager',
        store=True
    )

    @api.depends('employee_id')
    def _compute_manager(self):
        for request in self:
            if request.employee_id.parent_id.user_id:
                request.manager_id = request.employee_id.parent_id.user_id
            else:
                request.manager_id = False

    def action_submit(self):
        self.write({'state': 'submitted'})
        # Notify manager via activity
        self.activity_schedule(
            'leave_approval_notify_hr.mail_activity_leave_approval',
            user_id=self.manager_id.id,
            note=f'Leave request from {self.employee_id.name} needs your approval'
        )

    def action_approve(self):
        self.write({'state': 'approved'})
        # Notify HR group
        hr_group = self.env.ref('hr.group_hr_user')
        self.message_post(
            body=_('Leave request has been approved by manager'),
            partner_ids=hr_group.users.partner_id.ids,
            message_type='notification',
            subtype_xmlid='mail.mt_comment'
        )

    def action_reject(self):
        self.write({'state': 'rejected'})

    def action_create_hr_leave(self):
        # Bonus: Create official hr.leave record
        hr_leave = self.env['hr.leave'].create({
            'employee_id': self.employee_id.id,
            'holiday_status_id': self.env.ref('hr_holidays.holiday_status_cl').id,  # Default to paid time off
            'request_date_from': self.from_date,
            'request_date_to': self.to_date,
            'name': self.reason,
        })
        self.message_post(body=f'HR Leave created: {hr_leave.name}')
        return {
            'name': _('HR Leave'),
            'view_mode': 'form',
            'res_model': 'hr.leave',
            'res_id': hr_leave.id,
            'type': 'ir.actions.act_window',
        }

    @api.constrains('from_date', 'to_date')
    def _check_dates(self):
        for request in self:
            if request.from_date > request.to_date:
                raise ValidationError(_('End date must be after start date'))