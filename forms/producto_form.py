def obtener_datos_producto(request):
    return {
        "nombre": request.form["nombre"],
        "precio": request.form["precio"],
        "cantidad": request.form["cantidad"],
        "descripcion": request.form.get("descripcion", "")
    }