CREATE DATABASE usuariosdb;

USE usuariosdb;

CREATE TABLE IF NOT EXISTS usuarios (
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    edad VARCHAR(100) NOT NULL
);