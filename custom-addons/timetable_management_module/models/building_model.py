from odoo import models, fields


class BuildingModel(models.Model):
    _name = "building_model"
    _description = "Building Model"

    name = fields.Char()
    address = fields.Text()
