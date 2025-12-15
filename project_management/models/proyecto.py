# models/proyecto.py
from odoo import models, fields, api
from odoo.exceptions import UserError
from pkg_resources import require


class Proyecto(models.Model):
    _name = 'project.proyecto'
    _description = 'Gestión de Proyectos'

    name = fields.Char(string='Nombre del proyecto', required=True)
    description = fields.Text(string='Descripción general del proyecto')

    start_date = fields.Date(string='Fecha de inicio', required=True)
    end_date = fields.Date(string='Fecha de fin')

    responsible_id = fields.Many2one('res.users', string='Responsable del proyecto')


    trabajo_ids = fields.One2many('project.trabajo', 'proyecto_id', string='Trabajos')


    state = fields.Selection([
        ('borrador', 'Borrador'),
        ('planificacion', 'En planificación'),
        ('ejecucion', 'En ejecución'),
        ('finalizado', 'Finalizado'),
        ('cancelado', 'Cancelado')
    ], string='Estado', default='borrador')


    progress = fields.Float(string='Avance (%)', compute='_compute_progress', store=True)


    individual_progress = fields.Float(string='Avance Manual (%)')

    @api.depends('trabajo_ids.progress')
    def _compute_progress(self):
        for record in self:
            if record.trabajo_ids:
                total_progress = sum(t.progress for t in record.trabajo_ids)
                record.progress = total_progress / len(record.trabajo_ids)
            else:
                record.progress = 0.0


    @api.ondelete(at_uninstall=False)
    def _check_unlink(self):
        for record in self:
            if record.trabajo_ids and record.state != 'borrador':
                raise UserError("No se puede eliminar un proyecto con trabajos asociados salvo en estado borrador.")

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for record in self:
            if record.start_date and record.end_date and record.start_date > record.end_date:
                raise UserError("Error: La fecha de finalización no puede ser anterior a la fecha de inicio.")