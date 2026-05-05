import os
import pytest

from app import crear_app, db
from app.dominios.usuarios.servicios import UsuarioServicio


@pytest.fixture
def app():
    os.environ["FLASK_TESTING"] = "true"

    app = crear_app()
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:"
    )

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

    os.environ.pop("FLASK_TESTING", None)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def usuario_autenticado(client):
    client.post(
        "/api/v1/usuarios/registro",
        json={
            "correo": "test@example.com",
            "contrasena": "123456"
        }
    )

    response = client.post(
        "/api/v1/usuarios/login",
        json={
            "correo": "test@example.com",
            "contrasena": "123456"
        }
    )

    token = response.get_json()["token"]

    return {
        "token": token,
        "headers": {
            "Authorization": f"Bearer {token}"
        }
    }


@pytest.fixture
def usuario_auth2(client):
    """Crea un segundo usuario unico y devuelve token + headers."""
    import uuid

    email = f"user2-{uuid.uuid4().hex[:8]}@ejemplo.com"

    client.post(
        "/api/v1/usuarios/registro",
        json={
            "correo": email,
            "contrasena": "123456"
        }
    )

    response = client.post(
        "/api/v1/usuarios/login",
        json={
            "correo": email,
            "contrasena": "123456"
        }
    )

    token = response.get_json()["token"]

    return {
        "token": token,
        "headers": {
            "Authorization": f"Bearer {token}"
        }
    }


@pytest.fixture
def admin_autenticado(client):
    client.post(
        "/api/v1/usuarios/registro",
        json={
            "correo": "admin@example.com",
            "contrasena": "123456"
        }
    )

    UsuarioServicio.promover_a_admin("admin@example.com")

    response = client.post(
        "/api/v1/usuarios/login",
        json={
            "correo": "admin@example.com",
            "contrasena": "123456"
        }
    )

    token = response.get_json()["token"]

    return {
        "token": token,
        "headers": {
            "Authorization": f"Bearer {token}"
        }
    }