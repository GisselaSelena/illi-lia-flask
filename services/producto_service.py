from conexion.conexion import obtener_conexion

def obtener_productos():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos")
    datos = cursor.fetchall()
    conexion.close()
    return datos

def obtener_producto_por_id(id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos WHERE id_producto = %s", (id,))
    dato = cursor.fetchone()
    conexion.close()
    return dato

def obtener_productos_por_categoria(categoria):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos WHERE categoria = %s", (categoria,))
    datos = cursor.fetchall()
    conexion.close()
    return datos

def agregar_producto(nombre, precio, cantidad, descripcion=''):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO productos (nombre, precio, cantidad, descripcion) VALUES (%s, %s, %s, %s)",
        (nombre, precio, cantidad, descripcion)
    )
    conexion.commit()
    conexion.close()

def editar_producto(id, nombre, precio, cantidad):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        "UPDATE productos SET nombre=%s, precio=%s, cantidad=%s WHERE id_producto=%s",
        (nombre, precio, cantidad, id)
    )
    conexion.commit()
    conexion.close()

def eliminar_producto(id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM productos WHERE id_producto = %s", (id,))
    conexion.commit()
    conexion.close()