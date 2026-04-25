from flask import Blueprint, request
from marshmallow import ValidationError

from app.seguridad import requiere_token, requiere_admin
from app.dominios.usuarios.dtos import RegistroUsuarioDTO, ActualizarPerfilDTO
from app.dominios.usuarios.servicios import UsuarioServicio


usuarios_bp = Blueprint("usuarios", __name__)
admin_bp = Blueprint("admin", __name__)

registro_dto = RegistroUsuarioDTO()
actualizar_perfil_dto = ActualizarPerfilDTO()


# -----------------------------
# USUARIOS
# -----------------------------

@usuarios_bp.route("/registro", methods=["POST"])
def registro():
    try:
        data = registro_dto.load(request.get_json())

        usuario = UsuarioServicio.registrar_usuario(
            correo=data["correo"],
            contrasena=data["contrasena"]
        )

        return {
            "message": "Usuario registrado correctamente",
            "usuario": {
                "id": usuario.id,
                "correo": usuario.correo
            }
        }, 201

    except ValidationError as e:
        return {"errors": e.messages}, 400


@usuarios_bp.route("/login", methods=["POST"])
def login():
    try:
        data = registro_dto.load(request.get_json())

        token = UsuarioServicio.iniciar_sesion(
            correo=data["correo"],
            contrasena=data["contrasena"]
        )

        return {
            "message": "Login exitoso",
            "token": token
        }, 200

    except ValidationError as e:
        return {"errors": e.messages}, 400


@usuarios_bp.route("/perfil", methods=["GET"])
@requiere_token
def obtener_perfil(usuario_id):
    perfil = UsuarioServicio.obtener_perfil(usuario_id)

    return {
        "perfil": {
            "nombre": perfil.nombre,
            "apellido": perfil.apellido,
            "telefono": perfil.telefono,
            "usuario_id": perfil.usuario_id
        }
    }, 200


@usuarios_bp.route("/perfil", methods=["PATCH"])
@requiere_token
def actualizar_perfil(usuario_id):
    try:
        data = actualizar_perfil_dto.load(request.get_json())

        perfil = UsuarioServicio.actualizar_perfil(usuario_id, data)

        return {
            "message": "Perfil actualizado correctamente",
            "perfil": {
                "nombre": perfil.nombre,
                "apellido": perfil.apellido,
                "telefono": perfil.telefono,
                "usuario_id": perfil.usuario_id
            }
        }, 200

    except ValidationError as e:
        return {"errors": e.messages}, 400


# -----------------------------
# ADMIN
# -----------------------------

@admin_bp.route("/usuarios", methods=["GET"])
@requiere_admin
def listar_usuarios(usuario_id):
    usuarios = UsuarioServicio.listar_todos_los_usuarios()

    return {
        "success": True,
        "message": "Lista de usuarios.",
        "data": usuarios,
    }, 200