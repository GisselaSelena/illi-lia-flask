def obtener_datos_producto(request):
    return {
        "nombre": request.form["nombre"],
        "precio": request.form["precio"],
        "stock": request.form["stock"]
    }