"""
Script para promover un usuario existente a rol admin.
Uso:
    python scripts/promover_admin.py correo@ejemplo.com
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import crear_app
from app.dominios.usuarios.servicios import UsuarioServicio, UsuarioNoEncontradoError


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python scripts/promover_admin.py <correo>")
        sys.exit(1)

    correo = sys.argv[1]

    app = crear_app()

    with app.app_context():
        try:
            UsuarioServicio.promover_a_admin(correo)
            print(f"Exito: el usuario '{correo}' ahora tiene rol de administrador.")
        except UsuarioNoEncontradoError as e:
            print(f"Error: {e}")
            sys.exit(1)