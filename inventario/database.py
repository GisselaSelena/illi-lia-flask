import sqlite3

def conectar():
    return sqlite3.connect("database.db")

def crear_tabla():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY,
            nombre TEXT,
            cantidad INTEGER,
            precio REAL
        )
    """)
    conn.commit()
    conn.close()

def insertar_producto(id, nombre, cantidad, precio):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO productos VALUES (?, ?, ?, ?)",
        (id, nombre, cantidad, precio)
    )
    conn.commit()
    conn.close()

def obtener_productos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    datos = cursor.fetchall()
    conn.close()
    return datos