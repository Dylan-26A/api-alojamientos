from datetime import datetime
from app import db


class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    correo = db.Column(db.String(255), unique=True, nullable=False)
    contrasena = db.Column(db.String(255), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    rol = db.Column(db.String(50), default='usuario')

    # Relación uno a uno con perfil
    perfil = db.relationship(
        'PerfilUsuario',
        backref='usuario',
        uselist=False,
        cascade='all, delete-orphan'
    )


class PerfilUsuario(db.Model):
    __tablename__ = 'perfiles_usuario'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    apellido = db.Column(db.String(100))
    telefono = db.Column(db.String(20))

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey('usuarios.id'),
        nullable=False,
        unique=True
    )