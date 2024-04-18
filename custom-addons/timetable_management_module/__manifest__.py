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
        'views/classrooms.xml',
        'views/reservations.xml',
        'views/timetable_management.xml'
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False
}