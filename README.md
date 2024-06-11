# Timetable management Odoo module

## Description
This module for Odoo 17 offers a solution to solve complex scheduling and resource management challenges faced by educational institutions. Utilizing the capabilities of the Odoo platform, this project aims to create a dynamic and user-friendly system that can meet the diverse needs of students, teachers and management staff. Key features include the management of classrooms as basic structural units, with attributes such as capacity, address, equipment and type. User roles are defined for administrators, managers, supervisors, professors, students and guests, each with individual access to information and functionality. The system allows managers to schedule classes and book classrooms on demand for faculty members, facilitating communication between them. 

## Installation
To run the project:
- Clone the repository
```commandline
git clone https://github.com/muchunzyan/timetable_management.git
```
- Set up the odoo.conf file
- Run your postgres database
- Run the odoo module

Example:
```commandline
path_to_python_env path_to_odoo-bin -c path_to_timetable_management/odoo.conf
```

> For the module to work correctly, it is also necessary to install the PaLMS module of [the next version](https://github.com/sefasenlik/PaLMS/commit/ad86212f54d75207cb923ec55b4899f937663f76) in addition to the libraries used by odoo.
