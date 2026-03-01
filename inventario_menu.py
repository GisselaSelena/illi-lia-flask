from inventario.inventario import Inventario
from inventario.producto import Producto
from inventario.database import crear_tabla, insertar_producto, obtener_productos

inventario = Inventario()
crear_tabla()

while True:
    print("\n--- Inventario Illí Lía ---")
    print("1. Agregar producto")
    print("2. Mostrar productos")
    print("3. Buscar producto")
    print("4. Salir")

    opcion = input("Seleccione opción: ")

    if opcion == "1":
        id = int(input("ID: "))
        nombre = input("Nombre: ")
        cantidad = int(input("Cantidad: "))
        precio = float(input("Precio: "))

        producto = Producto(id, nombre, cantidad, precio)
        inventario.agregar_producto(producto)
        insertar_producto(id, nombre, cantidad, precio)

        print("Producto agregado correctamente.")

    elif opcion == "2":
        productos = obtener_productos()
        for p in productos:
            print(p)

    elif opcion == "3":
        nombre = input("Nombre a buscar: ")
        resultados = inventario.buscar_por_nombre(nombre)
        for p in resultados:
            print(p.get_nombre(), "-", p.get_precio())

    elif opcion == "4":
        print("Saliendo del sistema...")
        break