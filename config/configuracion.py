"""Configuración de la API. Lee los parámetros desde variables de entorno (.env).

Regla de oro: las credenciales NUNCA se escriben en el código ni se suben a Git.
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Parámetros de conexión a MySQL y de la aplicación."""

    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", "3306"))
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "api_auth_db")

    MAX_INTENTOS = int(os.getenv("MAX_INTENTOS", "3"))