from flask import Flask, render_template, request, redirect, session, make_response, send_file
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from fpdf import FPDF
import os
import uuid
import tempfile

from models import Usuario
from conexion.conexion import obtener_conexion

from inventario.database import guardar_txt, guardar_json, guardar_csv
from inventario.database import leer_txt, leer_json, leer_csv

from services.producto_service import obtener_productos, obtener_producto_por_id
from services.pedido_service import (
    crear_pedido,
    obtener_pedidos_usuario,
    obtener_todos_pedidos,
    actualizar_estado_pedido,
    contar_pedidos_pendientes
)

app = Flask(__name__)
app.secret_key = "secret123"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (user_id,))
    user = cursor.fetchone()
    conexion.close()
    if user:
        return Usuario(user[0], user[1], user[2], user[3], user[4])
    return None

@app.context_processor
def inject_pedidos_pendientes():
    try:
        if current_user.is_authenticated and current_user.rol == 'admin':
            return dict(pedidos_pendientes=contar_pedidos_pendientes())
    except:
        pass
    return dict(pedidos_pendientes=0)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/catalogo")
def catalogo():
    productos = obtener_productos()
    return render_template("catalogo.html", productos=productos, categoria=None)

@app.route("/catalogo/<categoria>")
def catalogo_categoria(categoria):
    from services.producto_service import obtener_productos_por_categoria
    productos = obtener_productos_por_categoria(categoria)
    return render_template("catalogo.html", productos=productos, categoria=categoria)

@app.route("/producto/<nombre_producto>")
def producto(nombre_producto):
    nombre_formateado = nombre_producto.replace('-', ' ').title()
    return render_template("producto.html", nombre=nombre_formateado)

@app.route("/datos")
def ver_datos():
    datos_txt = leer_txt()
    datos_json = leer_json()
    datos_csv = leer_csv()
    return render_template("datos.html", txt=datos_txt, json=datos_json, csv=datos_csv)

@app.route("/agregar-carrito/<int:id_producto>", methods=["POST"])
def agregar_carrito(id_producto):
    cantidad = int(request.form.get("cantidad", 1))
    if "carrito" not in session:
        session["carrito"] = {}
    carrito = session["carrito"]
    clave = str(id_producto)
    if clave in carrito:
        carrito[clave]["cantidad"] += cantidad
    else:
        p = obtener_producto_por_id(id_producto)
        if p:
            carrito[clave] = {
                "id": id_producto,
                "nombre": p[1],
                "precio": float(p[2]),
                "cantidad": cantidad
            }
    session["carrito"] = carrito
    session.modified = True
    return redirect("/carrito")

@app.route("/carrito")
def ver_carrito():
    carrito = session.get("carrito", {})
    total = sum(item["precio"] * item["cantidad"] for item in carrito.values())
    return render_template("carrito.html", carrito=carrito, total=total)

@app.route("/eliminar-carrito/<int:id_producto>")
def eliminar_carrito(id_producto):
    carrito = session.get("carrito", {})
    carrito.pop(str(id_producto), None)
    session["carrito"] = carrito
    session.modified = True
    return redirect("/carrito")

@app.route("/checkout")
@login_required
def checkout():
    carrito = session.get("carrito", {})
    if not carrito:
        return redirect("/carrito")
    total = sum(item["precio"] * item["cantidad"] for item in carrito.values())
    return render_template("checkout.html", carrito=carrito, total=total)

@app.route("/confirmar-pedido", methods=["POST"])
@login_required
def confirmar_pedido():
    carrito = session.get("carrito", {})
    if not carrito:
        return redirect("/carrito")

    metodo = request.form.get("metodo_pago", "contra entrega")
    comprobante_nombre = None

    if "comprobante" in request.files:
        archivo = request.files["comprobante"]
        if archivo.filename != "":
            ext = archivo.filename.rsplit(".", 1)[-1]
            comprobante_nombre = f"{uuid.uuid4().hex}.{ext}"
            os.makedirs("static/comprobantes", exist_ok=True)
            archivo.save(f"static/comprobantes/{comprobante_nombre}")

    errores = []
    for clave, item in carrito.items():
        ok, msg = crear_pedido(
            id_usuario=current_user.id,
            id_producto=item["id"],
            cantidad=item["cantidad"],
            metodo_pago=metodo,
            comprobante=comprobante_nombre
        )
        if not ok:
            errores.append(f"{item['nombre']}: {msg}")

    session["carrito"] = {}
    session.modified = True

    if errores:
        return render_template("pedido_resultado.html", exito=False, errores=errores)
    return render_template("pedido_resultado.html", exito=True)

@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nombre   = request.form["nombre"]
        mail     = request.form["mail"]
        password = generate_password_hash(request.form["password"], method='pbkdf2:sha256')
        conexion = obtener_conexion()
        cursor   = conexion.cursor()
        cursor.execute("INSERT INTO usuarios (nombre, mail, password) VALUES (%s,%s,%s)", (nombre, mail, password))
        conexion.commit()
        conexion.close()
        return redirect("/login")
    return render_template("registro.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    mensaje = None
    if request.method == "POST":
        mail     = request.form["mail"]
        password = request.form["password"]
        conexion = obtener_conexion()
        cursor   = conexion.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE mail=%s", (mail,))
        user = cursor.fetchone()
        conexion.close()
        if user and check_password_hash(user[3], password):
            usuario = Usuario(user[0], user[1], user[2], user[3], user[4])
            login_user(usuario)
            if usuario.rol == 'admin':
                return redirect("/productos")
            else:
                return redirect("/catalogo")
        else:
            mensaje = "Correo o contrasena incorrectos"
    return render_template("login.html", mensaje=mensaje)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")

@app.route("/usuarios")
@login_required
def usuarios():
    conexion = obtener_conexion()
    cursor   = conexion.cursor()
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    conexion.close()
    return render_template("usuarios.html", usuarios=usuarios)

@app.route("/agregar_usuario", methods=["GET", "POST"])
@login_required
def agregar_usuario():
    if request.method == "POST":
        nombre   = request.form["nombre"]
        mail     = request.form["mail"]
        password = generate_password_hash(request.form["password"], method='pbkdf2:sha256')
        conexion = obtener_conexion()
        cursor   = conexion.cursor()
        cursor.execute("INSERT INTO usuarios (nombre, mail, password) VALUES (%s,%s,%s)", (nombre, mail, password))
        conexion.commit()
        conexion.close()
        return redirect("/usuarios")
    return render_template("agregar_usuario.html")

@app.route("/eliminar_usuario/<int:id>")
@login_required
def eliminar_usuario(id):
    conexion = obtener_conexion()
    cursor   = conexion.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id,))
    conexion.commit()
    conexion.close()
    return redirect("/usuarios")

@app.route("/editar_usuario/<int:id>", methods=["GET", "POST"])
@login_required
def editar_usuario(id):
    conexion = obtener_conexion()
    cursor   = conexion.cursor()
    if request.method == "POST":
        nombre   = request.form["nombre"]
        mail     = request.form["mail"]
        password = generate_password_hash(request.form["password"], method='pbkdf2:sha256')
        cursor.execute("UPDATE usuarios SET nombre=%s, mail=%s, password=%s WHERE id_usuario=%s", (nombre, mail, password, id))
        conexion.commit()
        conexion.close()
        return redirect("/usuarios")
    cursor.execute("SELECT * FROM usuarios WHERE id_usuario=%s", (id,))
    usuario = cursor.fetchone()
    conexion.close()
    return render_template("editar_usuario.html", usuario=usuario)

@app.route("/productos")
@login_required
def productos():
    lista = obtener_productos()
    return render_template("productos/productos.html", productos=lista)

@app.route("/productos/agregar", methods=["GET", "POST"])
@login_required
def agregar_producto():
    if request.method == "POST":
        from services.producto_service import agregar_producto as add
        add(request.form["nombre"], request.form["precio"], request.form["cantidad"], request.form.get("descripcion", ""))
        return redirect("/productos")
    return render_template("productos/agregar_producto.html")

@app.route("/productos/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_producto_ruta(id):
    from services.producto_service import editar_producto, obtener_producto_por_id
    if request.method == "POST":
        editar_producto(id, request.form["nombre"], request.form["precio"], request.form["cantidad"])
        return redirect("/productos")
    p = obtener_producto_por_id(id)
    return render_template("productos/editar_producto.html", producto=p)

@app.route("/productos/eliminar/<int:id>")
@login_required
def eliminar_producto_ruta(id):
    from services.producto_service import eliminar_producto
    eliminar_producto(id)
    return redirect("/productos")

@app.route("/mis-pedidos")
@login_required
def mis_pedidos():
    pedidos = obtener_pedidos_usuario(current_user.id)
    return render_template("mis_pedidos.html", pedidos=pedidos)

@app.route("/admin/pedidos")
@login_required
def admin_pedidos():
    if current_user.rol != 'admin':
        return redirect("/")
    pedidos = obtener_todos_pedidos()
    return render_template("admin_pedidos.html", pedidos=pedidos)

@app.route("/admin/pedido/<int:id>/estado", methods=["POST"])
@login_required
def cambiar_estado_pedido(id):
    if current_user.rol != 'admin':
        return redirect("/")
    nuevo_estado = request.form.get("estado")
    actualizar_estado_pedido(id, nuevo_estado)
    return redirect("/admin/pedidos")

@app.route("/reporte-pdf")
@login_required
def reporte_pdf():
    productos = obtener_productos()
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(28, 58, 42)
    pdf.cell(0, 14, "ILLI LIA", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "I", 10)
    pdf.set_text_color(100, 120, 100)
    pdf.cell(0, 8, "Jabones Decorativos Artesanales", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, "Reporte de Productos", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    pdf.set_draw_color(201, 168, 76)
    pdf.set_line_width(0.8)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(6)
    pdf.set_fill_color(28, 58, 42)
    pdf.set_text_color(201, 168, 76)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(15, 10, "ID",       border=1, fill=True)
    pdf.cell(85, 10, "Nombre",   border=1, fill=True)
    pdf.cell(45, 10, "Precio",   border=1, fill=True)
    pdf.cell(45, 10, "Cantidad", border=1, fill=True, new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(28, 58, 42)
    pdf.set_font("Helvetica", "", 10)
    fill = False
    for p in productos:
        pdf.set_fill_color(245, 242, 235) if fill else pdf.set_fill_color(255, 255, 255)
        pdf.cell(15, 9, str(p[0]),               border=1, fill=True)
        pdf.cell(85, 9, str(p[1]),               border=1, fill=True)
        pdf.cell(45, 9, f"$ {float(p[2]):.2f}",  border=1, fill=True)
        pdf.cell(45, 9, str(p[3]),               border=1, fill=True, new_x="LMARGIN", new_y="NEXT")
        fill = not fill
    pdf.ln(8)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(120, 120, 100)
    pdf.cell(0, 8, "Generado por el sistema Illi Lia - 2026", align="C")
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
        pdf.output(tmp.name)
        tmp_path = tmp.name
    return send_file(
        tmp_path,
        mimetype='application/pdf',
        as_attachment=True,
        download_name='reporte_productos.pdf'
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)