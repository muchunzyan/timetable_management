from odoo import models, fields


class ClassroomModel(models.Model):
    _name = "classroom_model"
    _description = "Classroom Model"

    number = fields.Char()
    address = fields.Text()
    equipment = fields.Text()
    # TODO сделать выбираемые значения (selection) для equipment. Проблема в том, что должна быть возможность выбрать
    #  несколько значений
    type = fields.Selection(
        string='Type',
        selection=[('linguistic', 'Linguistic room (12-20 persons)'),
                   ('seminar', 'Seminar room (~25 persons)'),
                   ('seminar', 'Lecture room (>25 persons)'),
                   ('computer_class', 'Computer class')],
        help="The type is used to specify the purpose and capacity of the classroom")
    capacity = fields.Integer()
    occupied = fields.Boolean()
