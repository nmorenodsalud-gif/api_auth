"""Punto de entrada de la API. Ejecutar con: python app.py"""

from flask import Flask, jsonify

from rutas.auth_rutas import crear_blueprint


def crear_app(servicio=None) -> Flask:
    """Fábrica de la aplicación."""

    app = Flask(__name__)

    app.register_blueprint(
        crear_blueprint(servicio)
    )

    @app.get("/")
    def salud():
        return jsonify(
            estado="API de autenticación en línea"
        )

    @app.errorhandler(ConnectionError)
    def error_bd(e):
        return jsonify(
            error="Servicio de base de datos no disponible."
        ), 503

    return app


if __name__ == "__main__":
    crear_app().run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )