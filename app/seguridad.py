from functools import wraps

import jwt
from flask import request, current_app

from app.dominios.usuarios.repositorios import UsuarioRepositorio
from app.dominios.usuarios.servicios import PermisoDenegadoError


def _extraer_y_validar_token():
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return None, {"message": "Token requerido"}, 401

    partes = auth_header.split()

    if len(partes) != 2 or partes[0].lower() != "bearer":
        return None, {"message": "Formato de token inválido"}, 401

    token = partes[1]

    try:
        payload = jwt.decode(
            token,
            current_app.config["SECRET_KEY"],
            algorithms=["HS256"]
        )
        usuario_id = int(payload["sub"])
        return usuario_id, None, None

    except jwt.ExpiredSignatureError:
        return None, {"message": "Token expirado"}, 401

    except jwt.InvalidTokenError:
        return None, {"message": "Token inválido"}, 401


def requiere_token(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        usuario_id, error, status = _extraer_y_validar_token()

        if error:
            return error, status

        return f(usuario_id=usuario_id, *args, **kwargs)

    return wrapper


def requiere_admin(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        usuario_id, error, status = _extraer_y_validar_token()

        if error:
            return error, status

        usuario = UsuarioRepositorio.obtener_por_id(usuario_id)

        if not usuario or usuario.rol != "admin":
            raise PermisoDenegadoError(
                "Permiso denegado. Se requiere rol de administrador."
            )

        return f(usuario_id=usuario_id, *args, **kwargs)

    return wrapper