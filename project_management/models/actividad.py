from odoo import models, fields, api
from odoo.exceptions import UserError  # <--- IMPORTANTE: Importar esto


class Actividad(models.Model):
    _name = 'project.actividad'
    _description = 'Actividad del Trabajo'

    name = fields.Char(string='Nombre de la actividad', required=True)
    detail = fields.Text(string='Detalle de la tarea')

    trabajo_id = fields.Many2one('project.trabajo', string='Trabajo', required=True, ondelete='cascade')

    user_id = fields.Many2one('res.users', string='Persona que la realiza')
    date_planned_start = fields.Date(string='Inicio planificado')
    date_planned_end = fields.Date(string='Fin planificado')

    progress = fields.Float(string='Avance individual (0-100%)')

    state = fields.Selection([
        ('pendiente', 'Pendiente'),
        ('curso', 'En curso'),
        ('revision', 'En revisión'),
        ('finalizada', 'Finalizada'),
        ('cancelada', 'Cancelada')
    ], string='Estado', default='pendiente')

    @api.model
    def create(self, vals):
        if vals.get('trabajo_id'):
            trabajo = self.env['project.trabajo'].browse(vals['trabajo_id'])

            if trabajo.state in ['revision', 'finalizado']:
                raise UserError('No puedes crear nuevas actividades cuando el Trabajo está en revisión o finalizado.')

            if trabajo.proyecto_id.state == 'finalizado':
                raise UserError('No se pueden añadir actividades: El Proyecto principal está finalizado.')

        return super(Actividad, self).create(vals)


    def write(self, vals):
        for record in self:
            if record.trabajo_id.state in ['revision', 'finalizado']:

                raise UserError('No puedes modificar actividades de un Trabajo que está en revisión o finalizado.')


        res = super(Actividad, self).write(vals)


        if 'state' in vals:
            self.trabajo_id.check_all_activities_done()

        return res