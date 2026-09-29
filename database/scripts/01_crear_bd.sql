DROP DATABASE IF EXISTS api_auth_db;

CREATE DATABASE api_auth_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_spanish_ci;

USE api_auth_db;

CREATE TABLE usuario (

    id_usuario INT AUTO_INCREMENT PRIMARY KEY,

    usuario VARCHAR(30)
        NOT NULL UNIQUE,

    clave_hash VARCHAR(255)
        NOT NULL,

    intentos_fallidos TINYINT
        NOT NULL DEFAULT 0,

    estado ENUM('ACTIVO','BLOQUEADO')
        NOT NULL DEFAULT 'ACTIVO',

    fecha_creacion DATETIME
        NOT NULL DEFAULT CURRENT_TIMESTAMP,

    ultimo_acceso DATETIME
        NULL

) ENGINE=InnoDB;