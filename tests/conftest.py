import os
import pytest

from app import crear_app, db


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
    # Registrar usuario
    client.post(
        "/api/v1/usuarios/registro",
        json={
            "correo": "test@example.com",
            "contrasena": "123456"
        }
    )

    # Login
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