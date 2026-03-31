from conexion.conexion import obtener_conexion

def crear_pedido(id_usuario, id_producto, cantidad, metodo_pago='contra entrega', comprobante=None, telefono_envio=None):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT precio, cantidad FROM productos WHERE id_producto = %s", (id_producto,))
    producto = cursor.fetchone()

    if not producto:
        conexion.close()
        return False, "Producto no encontrado"

    precio, cantidad_disponible = producto

    if cantidad_disponible < cantidad:
        conexion.close()
        return False, "Stock insuficiente"

    total = float(precio) * cantidad

    cursor.execute(
        """INSERT INTO pedidos (id_usuario, telefono_envio, id_producto, cantidad, total, estado, metodo_pago, comprobante)
           VALUES (%s, %s, %s, %s, %s, 'pendiente', %s, %s)""",
        (id_usuario, telefono_envio, id_producto, cantidad, total, metodo_pago, comprobante)
    )

    cursor.execute(
        "UPDATE productos SET cantidad = cantidad - %s WHERE id_producto = %s",
        (cantidad, id_producto)
    )

    conexion.commit()
    conexion.close()
    return True, "Pedido creado exitosamente"


def obtener_pedidos_usuario(id_usuario):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT p.id_pedido, pr.nombre, p.cantidad, p.total, p.estado, p.fecha
        FROM pedidos p
        JOIN productos pr ON p.id_producto = pr.id_producto
        WHERE p.id_usuario = %s
        ORDER BY p.fecha DESC
    """, (id_usuario,))
    datos = cursor.fetchall()
    conexion.close()
    return datos


def obtener_todos_pedidos():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT p.id_pedido, u.nombre, pr.nombre, p.cantidad, p.total, p.estado, p.metodo_pago, p.comprobante, p.fecha, p.telefono_envio
        FROM pedidos p
        JOIN usuarios u   ON p.id_usuario  = u.id_usuario
        JOIN productos pr ON p.id_producto = pr.id_producto
        ORDER BY p.fecha DESC
    """)
    datos = cursor.fetchall()
    conexion.close()
    return datos


def actualizar_estado_pedido(id_pedido, estado):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        "UPDATE pedidos SET estado = %s WHERE id_pedido = %s",
        (estado, id_pedido)
    )
    conexion.commit()
    conexion.close()


def contar_pedidos_pendientes():
    conexion = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT COUNT(*) FROM pedidos WHERE estado = 'pendiente'")
        total = cursor.fetchone()[0]
        return total
    except:
        return 0
    finally:
        if conexion:
            conexion.close()