from datetime import datetime

import pytz
from odoo import api, models
from markupsafe import Markup


class UtilsModel(models.AbstractModel):
    _name = 'utils_model'
    _description = 'Utility Methods'

    @api.model
    def send_message(self, message_text, recipients, author):
        for recipient in recipients:
            channel_name = f"{recipient.name} reservations"

            channel = self.env['discuss.channel'].sudo().search([('name', '=', channel_name)], limit=1)

            if not channel:
                channel = self.env['discuss.channel'].with_context(mail_create_nosubscribe=True).sudo().create({
                    'channel_partner_ids': [(6, 0, recipient.partner_id.id)],
                    'channel_type': 'channel',
                    'name': channel_name,
                    'display_name': channel_name
                })

            channel.sudo().message_post(
                body=Markup(message_text),
                author_id=author.id,
                message_type="comment",
                subtype_xmlid='mail.mt_comment'
            )

    def to_local_timezone(self, date):
        datetime_format = "%Y-%m-%d %H:%M:%S"
        tz = pytz.timezone(self.env.user.partner_id.tz) or pytz.utc
        local_date = pytz.utc.localize(datetime.strptime(date, datetime_format)).astimezone(tz)
        return local_date
