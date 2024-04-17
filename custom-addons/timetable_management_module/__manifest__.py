{
    'name': 'Timetable management',
    'version': '1.0',
    'category': 'Education',
    'description': "Description",
    'author': "Uchunzhyan Mikhail",
    'depends': [
        'base',
    ],
    'data': [
        'data/data.xml',
        'security/ir.model.access.csv',
        'views/timetable_management.xml',
        'views/classrooms.xml',
        'views/reservations.xml'
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False
}