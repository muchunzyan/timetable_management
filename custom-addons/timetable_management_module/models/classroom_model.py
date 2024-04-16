from odoo import models, fields


class ClassroomModel(models.Model):
    _name = "classroom_model"
    _description = "Classroom Model"

    number = fields.Char()
    building = fields.Many2one('building_model')
    equipment = fields.Many2many('equipment_model')
    type = fields.Many2one('classroom_type_model')
    capacity = fields.Integer()
    occupied = fields.Boolean()
