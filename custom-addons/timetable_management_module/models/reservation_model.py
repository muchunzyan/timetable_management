from odoo import models, fields


class ReservationModel(models.Model):
    _name = "reservation_model"
    _description = "Reservation Model"

    name = fields.Char(string="Event name")
    reservator_id = fields.Many2one("res.users", "Reservator")
    start_datetime = fields.Datetime(string="Event start")
    end_datetime = fields.Datetime(string="Event end")
    classroom_id = fields.Many2one("classroom_model", "Classroom")
    reservation_time = fields.Datetime(default=fields.datetime.now())
