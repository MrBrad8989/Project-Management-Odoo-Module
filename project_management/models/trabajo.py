# models/trabajo.py
from odoo import models, fields, api
from odoo.exceptions import UserError


class Trabajo(models.Model):
    _name = 'project.trabajo'
    _description = 'Trabajo del Proyecto'

    name = fields.Char(string='Descripción del trabajo', required=True)

    actividad_ids = fields.One2many('project.actividad', 'trabajo_id', string='Actividades')
    proyecto_id = fields.Many2one('project.proyecto', string='Proyecto', required=True, ondelete='cascade')

    responsible_id = fields.Many2one('res.users', string='Responsable/Técnico')
    start_date = fields.Date(string='Fecha de inicio')
    end_date = fields.Date(string='Fecha de finalización')



    priority = fields.Selection([
        ('0', 'Baja'),
        ('1', 'Media'),
        ('2', 'Alta'),
        ('3', 'Urgente')
    ], string='Importancia de las actividades')


    state = fields.Selection([
        ('pendiente', 'Pendiente'),
        ('progreso', 'En progreso'),
        ('revision', 'En revisión'),
        ('finalizado', 'Finalizado')
    ], string='Estado', default='pendiente')


    progress = fields.Float(string='Avance Promedio (%)', compute='_compute_progress', store=True)
    individual_progress = fields.Float(string='Avance Individual (%)')

    @api.model
    def create(self, vals):
        # 1. Bloqueo por Proyecto Finalizado
        if vals.get('proyecto_id'):
            proyecto = self.env['project.proyecto'].browse(vals['proyecto_id'])
            if proyecto.state == 'finalizado':
                raise UserError("No se pueden crear nuevos trabajos en un Proyecto finalizado.")

        return super(Trabajo, self).create(vals)


    @api.depends('actividad_ids.progress')
    def _compute_progress(self):
        for record in self:
            if record.actividad_ids:
                total_progress = sum(a.progress for a in record.actividad_ids)
                record.progress = total_progress / len(record.actividad_ids)
            else:
                record.progress = 0.0


    def check_all_activities_done(self):
        for record in self:
            if record.actividad_ids and all(a.state == 'finalizada' for a in record.actividad_ids):
                record.state = 'finalizado'

    def write(self, vals):
        for record in self:
            # 2. Bloqueo por Proyecto Finalizado
            if record.proyecto_id.state == 'finalizado':
                raise UserError("No se puede modificar este trabajo porque el Proyecto está finalizado.")

            # 3. Bloqueo por Estado del Trabajo (Revisión/Finalizado)
            # Permitimos escribir SOLO si se está cambiando el 'state' (ej. reabrir el trabajo)
            if record.state in ['revision', 'finalizado'] and 'state' not in vals:
                raise UserError("No puedes editar un Trabajo que está en revisión o finalizado. Debes cambiar su estado a 'Progreso' primero.")


        if 'state' in vals:
            nuevo_estado = vals['state']
            if nuevo_estado == 'finalizado':
                actividades_abiertas = self.actividad_ids.filtered(
                    lambda a: a.state not in ['finalizada', 'cancelada']
                )
                if actividades_abiertas:
                    actividades_abiertas.write({'state': 'finalizada'})

        return super(Trabajo, self).write(vals)