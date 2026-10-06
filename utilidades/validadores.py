"""Validadores de entrada. Devuelven un mensaje de error o None si todo está bien."""

import re


def validar_usuario(usuario) -> str | None:
    """Usuario: texto de 4 a 30 caracteres (letras, números, punto o guion bajo)."""

    if not isinstance(usuario, str) or not re.fullmatch(
        r"[A-Za-z0-9._]{4,30}",
        usuario
    ):
        return (
            "El usuario debe tener entre 4 y 30 caracteres "
            "(letras, números, . o _)."
        )

    return None


def validar_clave(clave) -> str | None:
    """Regla RN-02 del SGC: mínimo 8 caracteres, una mayúscula y un número."""

    if (
        not isinstance(clave, str)
        or len(clave) < 8
        or not re.search(r"[A-Z]", clave)
        or not re.search(r"\d", clave)
    ):
        return (
            "La contraseña debe tener mínimo 8 caracteres, "
            "una mayúscula y un número."
        )

    return None