/* SE CREAN LAS TABLAS */

CREATE TABLE IF NOT EXISTS usuarios(
    username VARCHAR(30) UNIQUE NOT NULL,
    password VARCHAR(20) NOT NULL,
    PRIMARY KEY(username)
    );
    
CREATE TABLE IF NOT EXISTS recetas(
    nombre VARCHAR(80),
    ingredientes JSON,
    duenio VARCHAR(30) NOT NULL,
    descripcion TEXT,
    fecha_creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(nombre),
    FOREIGN KEY (duenio) REFERENCES usuarios(username)
    );
