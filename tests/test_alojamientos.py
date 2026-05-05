import json


class TestAlojamientos:
    def test_crear_alojamiento_con_auth(self, client, usuario_autenticado):
        resp = client.post("/api/v1/alojamientos", headers=usuario_autenticado["headers"], json={
            "titulo": "Cabaña Andina",
            "descripcion": "Vista al volcan",
            "precio_noche": 85.50,
            "ciudad": "Quito",
        })
        datos = json.loads(resp.data)

        assert resp.status_code == 201
        assert datos["success"] is True
        assert datos["data"]["titulo"] == "Cabaña Andina"
        assert datos["data"]["ciudad"] == "Quito"

    def test_crear_alojamiento_sin_token(self, client):
        resp = client.post("/api/v1/alojamientos", json={
            "titulo": "Cabaña Andina",
            "descripcion": "Vista al volcan",
            "precio_noche": 85.50,
            "ciudad": "Quito",
        })

        assert resp.status_code == 401

    def test_listar_alojamientos_sin_auth(self, client):
        resp = client.get("/api/v1/alojamientos")
        datos = json.loads(resp.data)

        assert resp.status_code == 200
        assert datos["success"] is True
        assert isinstance(datos["data"], list)

    def test_detalle_alojamiento_sin_auth(self, client, usuario_autenticado):
        r1 = client.post("/api/v1/alojamientos", headers=usuario_autenticado["headers"], json={
            "titulo": "Detalle Test",
            "descripcion": "Para prueba",
            "precio_noche": 50.0,
            "ciudad": "Lima",
        })
        d1 = json.loads(r1.data)
        alojamiento_id = d1["data"]["id"]

        resp = client.get(f"/api/v1/alojamientos/{alojamiento_id}")
        datos = json.loads(resp.data)

        assert resp.status_code == 200
        assert datos["success"] is True
        assert datos["data"]["titulo"] == "Detalle Test"

    def test_detalle_inexistente(self, client):
        resp = client.get("/api/v1/alojamientos/99999")
        datos = json.loads(resp.data)

        assert resp.status_code == 404
        assert datos["success"] is False

    def test_actualizar_ajeno_usuario_normal(self, client, usuario_autenticado, usuario_auth2):
        r1 = client.post("/api/v1/alojamientos", headers=usuario_autenticado["headers"], json={
            "titulo": "Propiedad Ajena",
            "descripcion": "No tocar",
            "precio_noche": 100.0,
            "ciudad": "Bogota",
        })
        d1 = json.loads(r1.data)
        alojamiento_id = d1["data"]["id"]

        resp = client.patch(
            f"/api/v1/alojamientos/{alojamiento_id}",
            headers=usuario_auth2["headers"],
            json={"titulo": "Hackeado"},
        )

        assert resp.status_code == 403

    def test_eliminar_ajeno_usuario_normal(self, client, usuario_autenticado, usuario_auth2):
        r1 = client.post("/api/v1/alojamientos", headers=usuario_autenticado["headers"], json={
            "titulo": "Propiedad Ajena 2",
            "descripcion": "No eliminar",
            "precio_noche": 75.0,
            "ciudad": "Medellin",
        })
        d1 = json.loads(r1.data)
        alojamiento_id = d1["data"]["id"]

        resp = client.delete(
            f"/api/v1/alojamientos/{alojamiento_id}",
            headers=usuario_auth2["headers"],
        )

        assert resp.status_code == 403

    def test_actualizar_propio(self, client, usuario_autenticado):
        r1 = client.post("/api/v1/alojamientos", headers=usuario_autenticado["headers"], json={
            "titulo": "Mi Alojamiento",
            "descripcion": "Original",
            "precio_noche": 60.0,
            "ciudad": "Santiago",
        })
        d1 = json.loads(r1.data)
        alojamiento_id = d1["data"]["id"]

        resp = client.patch(
            f"/api/v1/alojamientos/{alojamiento_id}",
            headers=usuario_autenticado["headers"],
            json={"titulo": "Mi Alojamiento Editado"},
        )
        datos = json.loads(resp.data)

        assert resp.status_code == 200
        assert datos["data"]["titulo"] == "Mi Alojamiento Editado"
        assert datos["data"]["descripcion"] == "Original"

    def test_eliminar_propio(self, client, usuario_autenticado):
        r1 = client.post("/api/v1/alojamientos", headers=usuario_autenticado["headers"], json={
            "titulo": "Para Eliminar",
            "descripcion": "Temporal",
            "precio_noche": 40.0,
            "ciudad": "Buenos Aires",
        })
        d1 = json.loads(r1.data)
        alojamiento_id = d1["data"]["id"]

        resp = client.delete(
            f"/api/v1/alojamientos/{alojamiento_id}",
            headers=usuario_autenticado["headers"],
        )
        assert resp.status_code == 204

        resp2 = client.get(f"/api/v1/alojamientos/{alojamiento_id}")
        assert resp2.status_code == 404

    def test_admin_actualiza_ajeno(self, client, admin_autenticado, usuario_autenticado):
        r1 = client.post("/api/v1/alojamientos", headers=usuario_autenticado["headers"], json={
            "titulo": "Propiedad de Usuario",
            "descripcion": "Admin va a editar",
            "precio_noche": 90.0,
            "ciudad": "Caracas",
        })
        d1 = json.loads(r1.data)
        alojamiento_id = d1["data"]["id"]

        resp = client.patch(
            f"/api/v1/alojamientos/{alojamiento_id}",
            headers=admin_autenticado["headers"],
            json={"titulo": "Editado por Admin"},
        )
        datos = json.loads(resp.data)

        assert resp.status_code == 200
        assert datos["data"]["titulo"] == "Editado por Admin"

    def test_admin_elimina_ajeno(self, client, admin_autenticado, usuario_autenticado):
        r1 = client.post("/api/v1/alojamientos", headers=usuario_autenticado["headers"], json={
            "titulo": "Propiedad para Eliminar",
            "descripcion": "Admin va a eliminar",
            "precio_noche": 120.0,
            "ciudad": "Panama",
        })
        d1 = json.loads(r1.data)
        alojamiento_id = d1["data"]["id"]

        resp = client.delete(
            f"/api/v1/alojamientos/{alojamiento_id}",
            headers=admin_autenticado["headers"],
        )
        assert resp.status_code == 204

        resp2 = client.get(f"/api/v1/alojamientos/{alojamiento_id}")
        assert resp2.status_code == 404