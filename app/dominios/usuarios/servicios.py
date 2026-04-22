from datetime import datetime, timedelta
import jwt

from werkzeug.security import generate_password_hash, check_password_hash

from app.config import Config
from app.dominios.usuarios.modelos import Usuario, PerfilUsuario
from app.dominios.usuarios.repositorios import UsuarioRepositorio


class CorreoYaRegistradoError(Exception):
    pass


class CredencialesInvalidasError(Exception):
    pass


class UsuarioNoEncontradoError(Exception):
    pass


class UsuarioServicio:

    @staticmethod
    def registrar_usuario(correo, contrasena):
        # Verificar duplicado
        existente = UsuarioRepositorio.obtener_por_correo(correo)
        if existente:
            raise CorreoYaRegistradoError("El correo ya está registrado")

        # Hashear contraseña
        hash_contrasena = generate_password_hash(contrasena)

        usuario = Usuario(
            correo=correo,
            contrasena=hash_contrasena
        )

        usuario = UsuarioRepositorio.guardar_usuario(usuario)

        # Crear perfil vacío
        perfil = PerfilUsuario(usuario_id=usuario.id)
        UsuarioRepositorio.guardar_perfil(perfil)

        return usuario

    @staticmethod
    def iniciar_sesion(correo, contrasena):
        usuario = UsuarioRepositorio.obtener_por_correo(correo)

        if not usuario:
            raise CredencialesInvalidasError("Credenciales inválidas")

        if not check_password_hash(usuario.contrasena, contrasena):
            raise CredencialesInvalidasError("Credenciales inválidas")

        token = UsuarioServicio._generar_token(usuario)

        return token

    @staticmethod
    def _generar_token(usuario):
        payload = {
            "sub": str(usuario.id),  # IMPORTANTE: string
            "exp": datetime.utcnow() + timedelta(minutes=Config.JWT_EXP_MINUTES)
        }

        token = jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")

        return token

    @staticmethod
    def obtener_perfil(usuario_id):
        perfil = UsuarioRepositorio.obtener_perfil_por_usuario_id(usuario_id)

        if not perfil:
            raise UsuarioNoEncontradoError("Perfil no encontrado")

        return perfil

    @staticmethod
    def actualizar_perfil(usuario_id, datos):
        perfil = UsuarioRepositorio.obtener_perfil_por_usuario_id(usuario_id)

        if not perfil:
            raise UsuarioNoEncontradoError("Perfil no encontrado")

        if "nombre" in datos:
            perfil.nombre = datos["nombre"]

        if "apellido" in datos:
            perfil.apellido = datos["apellido"]

        if "telefono" in datos:
            perfil.telefono = datos["telefono"]

        UsuarioRepositorio.guardar_perfil(perfil)

        return perfil