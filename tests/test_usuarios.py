def test_registro_exitoso(client):
    response = client.post(
        "/api/v1/usuarios/registro",
        json={
            "correo": "nuevo@example.com",
            "contrasena": "123456"
        }
    )

    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "Usuario registrado correctamente"
    assert data["usuario"]["correo"] == "nuevo@example.com"


def test_registro_email_duplicado(client):
    client.post(
        "/api/v1/usuarios/registro",
        json={
            "correo": "duplicado@example.com",
            "contrasena": "123456"
        }
    )

    response = client.post(
        "/api/v1/usuarios/registro",
        json={
            "correo": "duplicado@example.com",
            "contrasena": "123456"
        }
    )

    assert response.status_code == 400
    data = response.get_json()
    assert "ya está registrado" in data["message"]


def test_registro_contrasena_corta(client):
    response = client.post(
        "/api/v1/usuarios/registro",
        json={
            "correo": "short@example.com",
            "contrasena": "123"
        }
    )

    assert response.status_code == 400
    data = response.get_json()
    assert "contrasena" in data["errors"]


def test_registro_email_invalido(client):
    response = client.post(
        "/api/v1/usuarios/registro",
        json={
            "correo": "correo-invalido",
            "contrasena": "123456"
        }
    )

    assert response.status_code == 400
    data = response.get_json()
    assert "correo" in data["errors"]


def test_login_exitoso(client):
    client.post(
        "/api/v1/usuarios/registro",
        json={
            "correo": "login@example.com",
            "contrasena": "123456"
        }
    )

    response = client.post(
        "/api/v1/usuarios/login",
        json={
            "correo": "login@example.com",
            "contrasena": "123456"
        }
    )

    assert response.status_code == 200
    data = response.get_json()
    assert "token" in data


def test_login_credenciales_invalidas(client):
    client.post(
        "/api/v1/usuarios/registro",
        json={
            "correo": "wrongpass@example.com",
            "contrasena": "123456"
        }
    )

    response = client.post(
        "/api/v1/usuarios/login",
        json={
            "correo": "wrongpass@example.com",
            "contrasena": "999999"
        }
    )

    assert response.status_code == 401
    data = response.get_json()
    assert "Credenciales inválidas" in data["message"]


def test_login_usuario_no_existente(client):
    response = client.post(
        "/api/v1/usuarios/login",
        json={
            "correo": "noexiste@example.com",
            "contrasena": "123456"
        }
    )

    assert response.status_code == 401
    data = response.get_json()
    assert "Credenciales inválidas" in data["message"]


def test_perfil_sin_token(client):
    response = client.get("/api/v1/usuarios/perfil")

    assert response.status_code == 401
    data = response.get_json()
    assert "Token requerido" in data["message"]


def test_perfil_con_token(usuario_autenticado, client):
    response = client.get(
        "/api/v1/usuarios/perfil",
        headers=usuario_autenticado["headers"]
    )

    assert response.status_code == 200
    data = response.get_json()
    assert "perfil" in data
    assert data["perfil"]["usuario_id"] == 1


def test_actualizacion_perfil(usuario_autenticado, client):
    response = client.patch(
        "/api/v1/usuarios/perfil",
        headers=usuario_autenticado["headers"],
        json={
            "nombre": "Dylan",
            "apellido": "Lopez",
            "telefono": "3001234567"
        }
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["perfil"]["nombre"] == "Dylan"
    assert data["perfil"]["apellido"] == "Lopez"
    assert data["perfil"]["telefono"] == "3001234567"


def test_actualizacion_parcial_perfil(usuario_autenticado, client):
    response = client.patch(
        "/api/v1/usuarios/perfil",
        headers=usuario_autenticado["headers"],
        json={
            "nombre": "SoloNombre"
        }
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["perfil"]["nombre"] == "SoloNombre"