CREATE DATABASE illi_lia;

USE illi_lia;

CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    mail VARCHAR(100),
    password VARCHAR(100)
);