from odoo import models, fields


class EquipmentModel(models.Model):
    _name = "equipment_model"
    _description = "Equipment Model"

    name = fields.Char(string="Name")
