# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime

class AlternativeHolidayRequest(models.Model):
    _name = 'alternative.holiday.request'
    _description = 'Alternative Holiday Request'
    _order = 'worked_date desc'

    # Many2one to hr.employee (auto set to current user’s employee)
    employee_id = fields.Many2one(
        'hr.employee', string='Employee',
        default=lambda self: self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1),
        required=True
    )

    worked_date = fields.Date(string='Worked Date', required=True)

    day_type = fields.Selection([
        ('weekend', 'Weekend'),
        ('public_holiday', 'Public Holiday'),
    ], string='Day Type', required=True)

    reason = fields.Text(string='Reason', required=True)

    requested_leave_date = fields.Date(string='Requested Leave Date', required=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string='Status', default='draft', tracking=True)

    manager_comments = fields.Text(string='Manager Comments')

    # Auto fill worked_date must be weekend/holiday is done later with constraint
    @api.constrains('worked_date')
    def _check_worked_date(self):
        for record in self:
            if record.worked_date and record.worked_date > fields.Date.today():
                raise ValidationError("Worked Date cannot be in the future.")
    def action_submit(self):
        for record in self:
            if record.state != 'draft':
                continue
            record.state = 'submitted'

    def action_approve(self):
        for record in self:
            if record.state != 'submitted':
                continue
            record.state = 'approved'

    def action_reject(self):
        for record in self:
            if record.state != 'submitted':
                continue
            record.state = 'rejected'
