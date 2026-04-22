from app import db
from app.dominios.usuarios.modelos import Usuario, PerfilUsuario


class UsuarioRepositorio:
    @staticmethod
    def guardar_usuario(usuario):
        db.session.add(usuario)
        db.session.commit()
        return usuario

    @staticmethod
    def obtener_por_correo(correo):
        return Usuario.query.filter_by(correo=correo).first()

    @staticmethod
    def obtener_por_id(usuario_id):
        return Usuario.query.get(usuario_id)

    @staticmethod
    def obtener_perfil_por_usuario_id(usuario_id):
        return PerfilUsuario.query.filter_by(usuario_id=usuario_id).first()

    @staticmethod
    def guardar_perfil(perfil):
        db.session.add(perfil)
        db.session.commit()
        return perfil