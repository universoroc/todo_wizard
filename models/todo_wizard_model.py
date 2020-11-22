# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError, Warning


import logging
_logger = logging.getLogger(__name__)


class TodoWizard(models.TransientModel):
    _name = 'todo.wizard'
    task_ids = fields.Many2many('todoroc_app.todoroc_app', string='Tasks')
    new_user_id = fields.Many2one('res.users', string='Set Responsible')
    new_deadline = fields.Date('Set Deadline')

    #@api.model_create_multi
    def todo_app_do_mass_update(self):
        self.ensure_one()
        if not (self.new_deadline or self.new_user_id):
            raise ValidationError('No data to update!')
        # else:
        _logger.debug('Mass update on Todo Tasks %s',
                      self.task_ids.ids)
        if self.new_deadline:
            self.task_ids.write({'date_deadline': self.new_deadline})
        if self.new_user_id:
            self.task_ids.write({'user_id': self.new_user_id.id})
        return True

    #@api.model_create_multi
    def todo_app_do_count_tasks(self):
        Task = self.env['todoroc_app.todoroc_app']
        count = Task.search_count([])
        #self.app_dialog()
        raise Warning('There are %d active tasks. ' % count)

    #@api.model_create_multi
    def todo_app_do_reopen_form(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,  # this model
            'res_id': self.id,  # the current wizard record
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new'}

    #@api.model_create_multi
    def todo_app_do_populate_tasks(self):
        self.ensure_one()
        Task = self.env['todoroc_app.todoroc_app']
        all_tasks = Task.search([])
        self.task_ids = all_tasks
        # reopen wizard form on same wizard record
        return self.todo_app_do_reopen_form()

    def app_dialog(self):

        return self.env['todo.wizard'].open_dialog(
            message='The product will be hided, <b>you cannot use again</b> '
                    'but remain in sale order where yet present, <br/>'
                    'confirm?',
            action='',
            title='Confirm request:',
            mode='cancel_confirm',
         )
