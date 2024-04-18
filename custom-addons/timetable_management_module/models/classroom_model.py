from odoo import models, fields


class ClassroomModel(models.Model):
    _name = "classroom_model"
    _description = "Classroom Model"

    number = fields.Char()
    building_id = fields.Many2one("building_model", string="Building")
    equipment_ids = fields.Many2many("equipment_model", string="Equipment")
    type_id = fields.Many2one("classroom_type_model", string="Type")
    capacity = fields.Integer()
    occupied = fields.Boolean()

    _sql_constraints = [('unique_number', 'unique(number)', 'The classroom with this number already exists')]
