from odoo import models, fields


class BuildingModel(models.Model):
    _name = "building_model"
    _description = "Building Model"
    _rec_name = "address"

    address = fields.Text()
