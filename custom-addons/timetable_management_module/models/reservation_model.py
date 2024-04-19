from odoo import models, fields


class ReservationModel(models.Model):
    _name = "reservation_model"
    _description = "Reservation Model"
    _rec_name = "discipline_id"

    discipline_id = fields.Many2one("discipline_model", string="Discipline")
    event_type_id = fields.Many2one("event_type_model", string="Event type")
    start_datetime = fields.Datetime(string="Event start")
    end_datetime = fields.Datetime(string="Event end")
    classroom_id = fields.Many2one("classroom_model", "Classroom")
    reservation_time = fields.Datetime(default=fields.datetime.now())
