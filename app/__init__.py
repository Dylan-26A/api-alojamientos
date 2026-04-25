from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate

from app.config import Config

API_VERSION = "v1"

db = SQLAlchemy()
migrate = Migrate()


def crear_app():
    """App factory: crea y configura la instancia de Flask."""
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app, origins=app.config["CORS_ALLOWED_ORIGINS"])

    from app.dominios.usuarios import modelos
    from app.dominios.usuarios.controladores import usuarios_bp, admin_bp
    from app.dominios.usuarios.servicios import (
        CorreoYaRegistradoError,
        CredencialesInvalidasError,
        UsuarioNoEncontradoError,
        PermisoDenegadoError,
    )

    app.register_blueprint(usuarios_bp, url_prefix="/api/v1/usuarios")
    app.register_blueprint(admin_bp, url_prefix="/api/v1/admin")

    @app.route("/health", methods=["GET"])
    def health():
        return {
            "status": "ok",
            "service": "alojamientos-api",
            "version": API_VERSION
        }, 200

    @app.errorhandler(CorreoYaRegistradoError)
    def manejar_correo_duplicado(error):
        return {"message": str(error)}, 400

    @app.errorhandler(CredencialesInvalidasError)
    def manejar_credenciales_invalidas(error):
        return {"message": str(error)}, 401

    @app.errorhandler(UsuarioNoEncontradoError)
    def manejar_usuario_no_encontrado(error):
        return {"message": str(error)}, 404

    @app.errorhandler(PermisoDenegadoError)
    def manejar_permiso_denegado(error):
        return {"message": str(error)}, 403

    @app.errorhandler(404)
    def recurso_no_encontrado(error):
        return {"success": False, "error": {"message": "Recurso no encontrado"}}, 404

    @app.errorhandler(500)
    def error_interno(error):
        return {"success": False, "error": {"message": "Error interno del servidor"}}, 500

    return app