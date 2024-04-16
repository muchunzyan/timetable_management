from odoo import models, fields


class ClassroomTypeModel(models.Model):
    _name = "classroom_type_model"
    _description = "Classroom Type Model"

    name = fields.Char()
    description = fields.Char()
