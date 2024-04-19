from odoo import models, fields


class DisciplineModel(models.Model):
    _name = "discipline_model"
    _description = "Discipline Model"

    name = fields.Char(string="Name")
    professor_ids = fields.Many2many("res.users", string="Professors")
