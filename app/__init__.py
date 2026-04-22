from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate

from app.config import Config

# Version de la API
API_VERSION = "v1"

# Instancia de SQLAlchemy
db = SQLAlchemy()

# Instancia de Flask-Migrate
migrate = Migrate()


def crear_app():
    """App factory: crea y configura la instancia de Flask."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app, origins=app.config["CORS_ALLOWED_ORIGINS"])

    # Importar modelos
    from app.dominios.usuarios import modelos

    # Importar blueprint y errores
    from app.dominios.usuarios.controladores import usuarios_bp
    from app.dominios.usuarios.servicios import (
        CorreoYaRegistradoError,
        CredencialesInvalidasError,
        UsuarioNoEncontradoError,
    )

    # Registrar blueprint
    app.register_blueprint(usuarios_bp, url_prefix="/api/v1/usuarios")

    # Endpoint de salud
    @app.route("/health", methods=["GET"])
    def health():
        return {
            "status": "ok",
            "service": "alojamientos-api",
            "version": API_VERSION
        }, 200

    # Manejadores de error de dominio
    @app.errorhandler(CorreoYaRegistradoError)
    def manejar_correo_duplicado(error):
        return {"message": str(error)}, 400

    @app.errorhandler(CredencialesInvalidasError)
    def manejar_credenciales_invalidas(error):
        return {"message": str(error)}, 401

    @app.errorhandler(UsuarioNoEncontradoError)
    def manejar_usuario_no_encontrado(error):
        return {"message": str(error)}, 404

    # Manejadores globales
    @app.errorhandler(404)
    def recurso_no_encontrado(error):
        return {"success": False, "error": {"message": "Recurso no encontrado"}}, 404

    @app.errorhandler(500)
    def error_interno(error):
        return {"success": False, "error": {"message": "Error interno del servidor"}}, 500

    return app