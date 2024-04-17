import time

from odoo import models, fields


class ReservationModel(models.Model):
    _name = "reservation_model"
    _description = "Reservation Model"

    name = fields.Char()
    reservator = fields.Many2one('res.users')
    start_datetime = fields.Datetime()
    end_datetime = fields.Datetime()
    classroom_id = fields.Many2one('classroom_model')
    reservation_time = fields.Datetime(default=lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'))
