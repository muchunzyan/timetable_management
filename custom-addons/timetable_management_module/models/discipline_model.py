from odoo import models, fields, api


class DisciplineModel(models.Model):
    _name = "discipline_model"
    _description = "Discipline Model"
    _rec_name = "name"

    name = fields.Char("Discipline Name", required=True)
    professor_ids = fields.Many2many('res.users', string="Professors", domain=lambda self: self._get_professor_domain())

    @api.model
    def _get_professor_domain(self):
        professor_group = self.env.ref('student.group_professor')
        return [('groups_id', 'in', professor_group.id)]
