import mysql.connector

def obtener_conexion():
    return mysql.connector.connect(
        host="sql10.freesqldatabase.com",
        user="sql10821670",
        password="5DzjQcFwnG",
        database="sql10821670",
        port=3306
    )