from odoo import models, fields


class EventTypeModel(models.Model):
    _name = "event_type_model"
    _description = "Event Type Model"

    name = fields.Char(string="Name")
