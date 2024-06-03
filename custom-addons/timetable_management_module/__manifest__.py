{
    'name': 'Timetable management',
    'version': '1.0',
    'category': 'Human Resources/Student',
    'description': "Description",
    'author': "Uchunzhyan Mikhail",
    'depends': ['base', 'mail', 'student'],
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