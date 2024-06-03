from odoo import models, fields, api
from odoo.exceptions import ValidationError
from markupsafe import Markup


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

    @api.model
    def create(self, vals):
        message_text = "new reservation created"
        professor_ids = [1]
        self.env['utils_model'].send_message('event', Markup(message_text), professor_ids,
                                             self.env.user.partner_id.id, (str(1), str("name")))
        return super(ReservationModel, self).create(vals)

    @api.constrains('classroom_id')
    def _check_classroom_id_is_free(self):

        for record in self:
            overlapping_class_reservations_interval_1 = (self.env["reservation_model"].search([
                ("id", "!=", record.id),
                ("classroom_id", "=", record.classroom_id.id),
                ("start_datetime", ">", record.start_datetime),
                ("start_datetime", "<", record.end_datetime)
            ]))
            overlapping_class_reservations_interval_2 = (self.env["reservation_model"].search([
                ("id", "!=", record.id),
                ("classroom_id", "=", record.classroom_id.id),
                ("end_datetime", "<", record.start_datetime),
                ("end_datetime", ">", record.end_datetime)
            ]))
            overlapping_class_reservations_interval_3 = (self.env["reservation_model"].search([
                ("id", "!=", record.id),
                ("classroom_id", "=", record.classroom_id.id),
                ("start_datetime", "<", record.start_datetime),
                ("end_datetime", ">", record.end_datetime)
            ]))
            overlapping_class_reservations_interval_4 = (self.env["reservation_model"].search([
                ("id", "!=", record.id),
                ("classroom_id", "=", record.classroom_id.id),
                ("end_datetime", ">", record.start_datetime),
                ("end_datetime", "<", record.end_datetime)
            ]))

            overlapping_class_reservations = (overlapping_class_reservations_interval_1 +
                                              overlapping_class_reservations_interval_2 +
                                              overlapping_class_reservations_interval_3 +
                                              overlapping_class_reservations_interval_4)

            for overlapping_class_reservation in overlapping_class_reservations:
                print(overlapping_class_reservation.classroom_id.id, ":",
                      overlapping_class_reservation.start_datetime, "-",
                      overlapping_class_reservation.end_datetime)

            if len(overlapping_class_reservations) > 0:
                raise ValidationError("The selected classroom is occupied at this time")
