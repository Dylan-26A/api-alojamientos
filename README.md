\# API Alojamientos



API REST desarrollada con Flask para la gestión de usuarios y alojamientos.



\## Tecnologías utilizadas



\- Python

\- Flask

\- Flask-SQLAlchemy

\- Flask-Migrate

\- MySQL

\- PyJWT

\- Marshmallow

\- Pytest



\## Funcionalidades principales



\- Registro de usuarios

\- Inicio de sesión con token

\- Consulta y actualización de perfil

\- Autorización por roles

\- Endpoints administrativos

\- CRUD de alojamientos

\- Relación entre usuario propietario y alojamiento

\- Pruebas automatizadas



\## Estructura general





app/

├── dominios/

│   ├── usuarios/

│   └── alojamientos/

├── seguridad.py

├── config.py

└── \_\_init\_\_.py



tests/

migrations/

scripts/

\# Endpoints principales

\## Usuarios

POST /api/v1/usuarios/registro

POST /api/v1/usuarios/login

GET /api/v1/usuarios/perfil

PATCH /api/v1/usuarios/perfil



\## Administración

GET /api/v1/admin/usuarios



\## Alojamientos

POST /api/v1/alojamientos

GET /api/v1/alojamientos

GET /api/v1/alojamientos/<id>

PATCH /api/v1/alojamientos/<id>

DELETE /api/v1/alojamientos/<id>

