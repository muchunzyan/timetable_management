from odoo import models, fields, api
from markupsafe import Markup


class ReservationRequestModel(models.Model):
    _name = "reservation_request_model"
    _description = "Reservation request Model"
    _rec_name = "classroom_id"

    is_discipline_related = fields.Boolean(string='Discipline-related reservation')

    name = fields.Char("Reservation name")
    discipline_id = fields.Many2one("discipline_model", string="Discipline")
    event_type_id = fields.Many2one("event_type_model", string="Event type")

    building_id = fields.Many2one("building_model", string="Building")
    hide_cluster_id = fields.Boolean(string='Hide Cluster field', compute='_compute_hide_cluster_id', store=False)
    cluster_id = fields.Many2one("cluster_model", string="Cluster")
    start_datetime = fields.Datetime(string="Event start")
    end_datetime = fields.Datetime(string="Event end")
    equipment_ids = fields.Many2many("equipment_model", string="Equipment")

    classroom_ids_to_display = fields.Many2many("classroom_model", string="Classroom IDs to display",
                                                compute='_compute_classroom_ids_to_display', store=False)
    classroom_id = fields.Many2one("classroom_model", "Classroom",
                                   domain="[('id', 'in', classroom_ids_to_display)]")
    classroom_can_be_reserved = fields.Boolean(string="Classroom can be reserved",
                                               compute="_compute_classroom_can_be_reserved", store=False)

    reservation_request_time = fields.Datetime(default=fields.datetime.now())
    reservator = fields.Many2one("res.users", string="Reservator")

    status = fields.Selection([
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ], string='Status', default='pending')

    # Methods for the buttons
    def action_accept(self):
        self.write({'status': 'accepted'})
        for record in self:
            _send_reservation_status_change_notification(self, record.start_datetime, record.end_datetime,
                                                         record.classroom_id.id, record.status, record.reservator)

            # Create reservation record
            self.env['reservation_model'].create({
                'name': record.name,
                'building_id': record.building_id.id,
                'cluster_id': record.cluster_id.id,
                'start_datetime': str(record.start_datetime),
                'end_datetime': str(record.end_datetime),
                'equipment_ids': record.equipment_ids,
                'classroom_id': record.classroom_id.id,
                'is_discipline_related': record.is_discipline_related,
                'discipline_id': record.discipline_id.id,
                'event_type_id': record.event_type_id.id,
                'reservation_time': fields.datetime.now(),
                'reservator': record.reservator.id,
            })

            _send_reservation_created_notification(self, record.discipline_id.id, record.event_type_id.id,
                                                   record.start_datetime, record.end_datetime, record.classroom_id.id)

    def action_decline(self):
        self.write({'status': 'declined'})
        for record in self:
            _send_reservation_status_change_notification(self, record.start_datetime, record.end_datetime,
                                                         record.classroom_id.id, record.status, record.reservator)

    @api.depends('building_id')
    def _compute_hide_cluster_id(self):
        for record in self:
            record.hide_cluster_id = '11, Pokrovsky Boulevard' not in (record.building_id.address or '')
            if record.hide_cluster_id:
                record.cluster_id = None

    @api.depends('start_datetime', 'end_datetime', 'equipment_ids', 'building_id', 'cluster_id')
    def _compute_classroom_ids_to_display(self):
        for record in self:
            # Define the domain to filter classrooms
            domain = []
            if record.building_id:
                domain.append(('building_id', '=', record.building_id.id))
            if record.cluster_id:
                domain.append(('cluster_id', '=', record.cluster_id.id))

            # Fetch classroom records based on the domain
            classroom_records = self.env['classroom_model'].search(domain)

            available_classroom_ids = []
            for classroom in classroom_records:
                overlapping_reservations = self.env['reservation_model'].search([
                    ('classroom_id', '=', classroom.id),
                    ('start_datetime', '<', record.end_datetime),
                    ('end_datetime', '>', record.start_datetime)
                ])
                if not overlapping_reservations:
                    available_classroom_ids.append(classroom.id)

            # Filter classrooms by equipment
            if record.equipment_ids:
                filtered_classroom_ids = []
                for classroom_id in available_classroom_ids:
                    classroom = self.env['classroom_model'].browse(classroom_id)

                    is_in_equipment = True

                    for record_equipment in record.equipment_ids:
                        if "_" in str(record_equipment.id):
                            record_equipment_id = str(record_equipment.id).split("_")[1]
                        else:
                            record_equipment_id = str(record_equipment.id)

                        classroom_equipment_ids = []
                        for classroom_equipment in classroom.equipment_ids:
                            classroom_equipment_ids.append(str(classroom_equipment.id))

                        if record_equipment_id not in classroom_equipment_ids:
                            is_in_equipment = False

                    if is_in_equipment:
                        filtered_classroom_ids.append(classroom_id)

                record.classroom_ids_to_display = [(6, 0, filtered_classroom_ids)]
            else:
                record.classroom_ids_to_display = [(6, 0, available_classroom_ids)]

            # Clear the chosen classroom if it's not suitable
            if record.status == 'pending' and (record.classroom_id not in record.classroom_ids_to_display):
                record.classroom_id = None

    @api.depends('classroom_id')
    def _compute_classroom_can_be_reserved(self):
        for record in self:
            record.classroom_can_be_reserved = record.classroom_id.id in record.classroom_ids_to_display.ids

    @api.model
    def create(self, vals):
        discipline = self.env["discipline_model"].search([("id", "=", vals["discipline_id"])]).name
        event_type = self.env["event_type_model"].search([("id", "=", vals["event_type_id"])]).name
        classroom = self.env["classroom_model"].search([("id", "=", vals["classroom_id"])]).number
        vals["reservator"] = self.env.user.id

        if vals["is_discipline_related"]:
            vals["name"] = None
        else:
            vals["discipline_id"] = None
            vals["event_type_id"] = None

        start_datetime = str(self.env['utils_model'].to_local_timezone(vals['start_datetime'])).split("+")[0]
        end_datetime = str(self.env['utils_model'].to_local_timezone(vals['end_datetime'])).split("+")[0]

        date = start_datetime.split(" ")[0]
        start_time = start_datetime.split(" ")[1]
        end_time = end_datetime.split(" ")[1]

        message_text = (f"<strong>New reservation request created:</strong><br>"
                        f"{discipline}, {event_type}<br>"
                        f"Date: {date}<br>"
                        f"Time: {start_time} - {end_time}<br>"
                        f"Classroom: {classroom}<br>"
                        f"Reservator: {self.env.user.name}")

        self.env['utils_model'].send_message("notify_managers", Markup(message_text), [])

        return super(ReservationRequestModel, self).create(vals)


def _send_reservation_status_change_notification(self, start_datetime, end_datetime, classroom_id, status, reservator):
    classroom = self.env["classroom_model"].search([("id", "=", classroom_id)]).number
    start_datetime = str(self.env['utils_model'].to_local_timezone(str(start_datetime))).split("+")[0]
    end_datetime = str(self.env['utils_model'].to_local_timezone(str(end_datetime))).split("+")[0]

    date = start_datetime.split(" ")[0]
    start_time = start_datetime.split(" ")[1]
    end_time = end_datetime.split(" ")[1]

    message_text = (f"<strong>The status of your reservation request has changed:</strong><br>"
                    f"Date: {date}<br>"
                    f"Time: {start_time} - {end_time}<br>"
                    f"Classroom: {classroom}<br>"
                    f"New status: {status.capitalize()}<br>")

    self.env['utils_model'].send_message("notify_reservator", Markup(message_text), [reservator])


def _send_reservation_created_notification(self, discipline_id, event_type_id, start_datetime, end_datetime,
                                           classroom_id):
    discipline = self.env["discipline_model"].search([("id", "=", discipline_id)]).name
    event_type = self.env["event_type_model"].search([("id", "=", event_type_id)]).name
    classroom = self.env["classroom_model"].search([("id", "=", classroom_id)]).number
    start_datetime = str(self.env['utils_model'].to_local_timezone(str(start_datetime))).split("+")[0]
    end_datetime = str(self.env['utils_model'].to_local_timezone(str(end_datetime))).split("+")[0]

    date = start_datetime.split(" ")[0]
    start_time = start_datetime.split(" ")[1]
    end_time = end_datetime.split(" ")[1]

    message_text = (f"<strong>New reservation created:</strong><br>"
                    f"{discipline}, {event_type}<br>"
                    f"Date: {date}<br>"
                    f"Time: {start_time} - {end_time}<br>"
                    f"Classroom {classroom}")

    professors = self.env["discipline_model"].search([("id", "=", discipline_id)]).professor_ids

    self.env['utils_model'].send_message("notify_reservator", Markup(message_text), professors)
