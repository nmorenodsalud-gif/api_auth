"""Acceso a datos de la entidad usuario. Solo SQL, sin reglas de negocio."""

from database.conexion import Conexion


class UsuarioDAO:
    """Todas las consultas son parametrizadas (%s) para evitar inyección SQL."""

    def insertar(self, usuario: str, clave_hash: str) -> int:
        """Inserta un usuario nuevo y devuelve su id."""

        sql = (
            "INSERT INTO usuario (usuario, clave_hash) "
            "VALUES (%s, %s)"
        )

        with Conexion() as cn:
            cursor = cn.cursor()
            cursor.execute(sql, (usuario, clave_hash))
            return cursor.lastrowid

    def buscar_por_usuario(self, usuario: str):
        """Devuelve el usuario como diccionario, o None si no existe."""

        sql = (
            "SELECT id_usuario, usuario, clave_hash, "
            "intentos_fallidos, estado "
            "FROM usuario WHERE usuario = %s"
        )

        with Conexion() as cn:
            cursor = cn.cursor(dictionary=True)
            cursor.execute(sql, (usuario,))
            return cursor.fetchone()

    def registrar_fallo(self, id_usuario: int, max_intentos: int) -> None:
        """Suma un intento fallido y bloquea al usuario si llegó al máximo."""

        sql = (
            "UPDATE usuario SET intentos_fallidos = intentos_fallidos + 1, "
            "estado = IF(intentos_fallidos + 1 >= %s, 'BLOQUEADO', estado) "
            "WHERE id_usuario = %s"
        )

        with Conexion() as cn:
            cn.cursor().execute(sql, (max_intentos, id_usuario))

    def registrar_acceso(self, id_usuario: int) -> None:
        """Login correcto: reinicia los intentos y guarda la fecha de acceso."""

        sql = (
            "UPDATE usuario SET intentos_fallidos = 0, "
            "ultimo_acceso = NOW() "
            "WHERE id_usuario = %s"
        )

        with Conexion() as cn:
            cn.cursor().execute(sql, (id_usuario,))