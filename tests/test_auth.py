"""Pruebas de la API con un DAO en memoria (no requiere MySQL)."""

import pytest

from app import crear_app
from config.configuracion import Config
from servicios.servicio_auth import ServicioAuth


class DAOFalso:
    """Simula UsuarioDAO guardando los usuarios en un diccionario."""

    def __init__(self):
        self.datos = {}

    def insertar(self, usuario, clave_hash):
        self.datos[usuario] = {
            "id_usuario": len(self.datos) + 1,
            "usuario": usuario,
            "clave_hash": clave_hash,
            "intentos_fallidos": 0,
            "estado": "ACTIVO"
        }
        return self.datos[usuario]["id_usuario"]

    def buscar_por_usuario(self, usuario):
        return self.datos.get(usuario)

    def registrar_fallo(self, id_usuario, max_intentos):
        for u in self.datos.values():
            if u["id_usuario"] == id_usuario:
                u["intentos_fallidos"] += 1

                if u["intentos_fallidos"] >= max_intentos:
                    u["estado"] = "BLOQUEADO"

    def registrar_acceso(self, id_usuario):
        for u in self.datos.values():
            if u["id_usuario"] == id_usuario:
                u["intentos_fallidos"] = 0


@pytest.fixture
def cliente():
    dao = DAOFalso()

    app = crear_app(
        ServicioAuth(dao)
    )

    c = app.test_client()
    c.dao = dao

    return c


def registrar(c, usuario="cesar01", clave="Clave1234"):
    return c.post(
        "/api/registro",
        json={
            "usuario": usuario,
            "clave": clave
        }
    )


def test_registro_exitoso_guarda_hash(cliente):
    r = registrar(cliente)

    assert r.status_code == 201
    assert r.get_json()["mensaje"] == "Registro exitoso."

    assert cliente.dao.datos["cesar01"]["clave_hash"] != "Clave1234"

    assert cliente.dao.datos["cesar01"]["clave_hash"].startswith("$2")


def test_registro_usuario_duplicado(cliente):
    registrar(cliente)

    assert registrar(cliente).status_code == 409


@pytest.mark.parametrize(
    "clave",
    [
        "corta1A",
        "sinnumeroA",
        "sinmayus123"
    ]
)
def test_registro_clave_invalida(cliente, clave):
    assert registrar(cliente, clave=clave).status_code == 400


def test_registro_sin_json(cliente):
    assert cliente.post(
        "/api/registro",
        data="no es json"
    ).status_code == 400


def test_login_correcto(cliente):
    registrar(cliente)

    r = cliente.post(
        "/api/login",
        json={
            "usuario": "cesar01",
            "clave": "Clave1234"
        }
    )

    assert r.status_code == 200
    assert r.get_json()["mensaje"] == "Autenticación satisfactoria."


def test_login_clave_incorrecta(cliente):
    registrar(cliente)

    r = cliente.post(
        "/api/login",
        json={
            "usuario": "cesar01",
            "clave": "Otra12345"
        }
    )

    assert r.status_code == 401
    assert r.get_json()["error"] == "Error en la autenticación."


def test_login_usuario_inexistente_mismo_mensaje(cliente):

    r = cliente.post(
        "/api/login",
        json={
            "usuario": "nadie99",
            "clave": "Clave1234"
        }
    )

    assert r.status_code == 401
    assert r.get_json()["error"] == "Error en la autenticación."


def test_login_campos_faltantes(cliente):
    assert cliente.post(
        "/api/login",
        json={}
    ).status_code == 401


def test_bloqueo_tras_intentos_fallidos(cliente):

    registrar(cliente)

    for _ in range(Config.MAX_INTENTOS):
        cliente.post(
            "/api/login",
            json={
                "usuario": "cesar01",
                "clave": "Mala12345"
            }
        )

    r = cliente.post(
        "/api/login",
        json={
            "usuario": "cesar01",
            "clave": "Clave1234"
        }
    )

    assert r.status_code == 423