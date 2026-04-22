from functools import wraps
from flask import request, jsonify
import jwt

from app.config import Config


def requiere_token(f):
    @wraps(f)
    def decorador(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return {"message": "Token requerido"}, 401

        try:
            # Formato: Bearer <token>
            token = auth_header.split(" ")[1]

            payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])

            usuario_id = int(payload["sub"])

        except jwt.ExpiredSignatureError:
            return {"message": "Token expirado"}, 401

        except Exception:
            return {"message": "Token inválido"}, 401

        # Inyectamos usuario_id en la función
        return f(usuario_id=usuario_id, *args, **kwargs)

    return decorador