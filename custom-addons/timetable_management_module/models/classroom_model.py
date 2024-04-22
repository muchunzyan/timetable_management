from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ClassroomModel(models.Model):
    _name = "classroom_model"
    _description = "Classroom Model"
    _rec_name = "number"

    number = fields.Char(string="Number")
    cluster_id = fields.Many2one("cluster_model", string="Cluster")
    building_id = fields.Many2one("building_model", string="Building")
    equipment_ids = fields.Many2many("equipment_model", string="Equipment")
    type_id = fields.Many2one("classroom_type_model", string="Type")
    capacity = fields.Integer(string="Capacity")

    _sql_constraints = [('unique_number', 'unique(number)', 'The classroom with this number already exists')]

    @api.constrains('capacity')
    def _check_capacity(self):
        for record in self:
            if record.capacity <= 0:
                raise ValidationError("The capacity should be greater than 0")
