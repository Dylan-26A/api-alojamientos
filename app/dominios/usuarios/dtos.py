from marshmallow import Schema, fields, validate


class RegistroUsuarioDTO(Schema):
    correo = fields.Email(required=True)
    contrasena = fields.String(required=True, validate=validate.Length(min=6))


class ActualizarPerfilDTO(Schema):
    nombre = fields.String(required=False)
    apellido = fields.String(required=False)
    telefono = fields.String(required=False)