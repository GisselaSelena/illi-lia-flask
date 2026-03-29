from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import Usuario
from flask import Flask, render_template, request, redirect
from conexion.conexion import obtener_conexion
import os

# importar funciones de persistencia
from inventario.database import guardar_txt, guardar_json, guardar_csv
from inventario.database import leer_txt, leer_json, leer_csv

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
        return Usuario(user[0], user[1], user[2], user[3])

    return None

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/producto/<nombre_producto>")
def producto(nombre_producto):
    nombre_formateado = nombre_producto.replace('-', ' ').title()
    return render_template("producto.html", nombre=nombre_formateado)


# Mostrar datos TXT JSON CSV
@app.route("/datos")
def ver_datos():

    datos_txt = leer_txt()
    datos_json = leer_json()
    datos_csv = leer_csv()

    return render_template(
        "datos.html",
        txt=datos_txt,
        json=datos_json,
        csv=datos_csv
    )


# VER USUARIOS DESDE MYSQL
@app.route("/usuarios")
@login_required
def usuarios():

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM usuarios")

    usuarios = cursor.fetchall()

    conexion.close()

    return render_template("usuarios.html", usuarios=usuarios)


# AGREGAR USUARIO MYSQL
@app.route("/agregar_usuario", methods=["GET", "POST"])
@login_required
def agregar_usuario():

    if request.method == "POST":

        nombre = request.form["nombre"]
        mail = request.form["mail"]
        password = request.form["password"]

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            "INSERT INTO usuarios (nombre, mail, password) VALUES (%s,%s,%s)",
            (nombre, mail, password)
        )

        conexion.commit()
        conexion.close()

        return redirect("/usuarios")

    return render_template("agregar_usuario.html")

@app.route("/eliminar_usuario/<int:id>")
@login_required
def eliminar_usuario(id):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id,))

    conexion.commit()
    conexion.close()

    return redirect("/usuarios")

@app.route("/editar_usuario/<int:id>", methods=["GET", "POST"])
@login_required
def editar_usuario(id):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    if request.method == "POST":

        nombre = request.form["nombre"]
        mail = request.form["mail"]
        password = request.form["password"]

        cursor.execute(
            "UPDATE usuarios SET nombre=%s, mail=%s, password=%s WHERE id_usuario=%s",
            (nombre, mail, password, id)
        )

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

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()

    conexion.close()

    return render_template("productos/productos.html", productos=productos)

@app.route("/registro", methods=["GET", "POST"])
def registro():

    if request.method == "POST":

        nombre = request.form["nombre"]
        mail = request.form["mail"]
        password = request.form["password"]

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            "INSERT INTO usuarios (nombre, mail, password) VALUES (%s,%s,%s)",
            (nombre, mail, password)
        )

        conexion.commit()
        conexion.close()

        return redirect("/login")

    return render_template("registro.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    mensaje = None  

    if request.method == "POST":

        mail = request.form["mail"]
        password = request.form["password"]

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            "SELECT * FROM usuarios WHERE mail=%s AND password=%s",
            (mail, password)
        )

        user = cursor.fetchone()
        conexion.close()

        if user:
            usuario = Usuario(user[0], user[1], user[2], user[3])
            login_user(usuario)
            return redirect("/productos")
        else:
            mensaje = "Usuario o contraseña incorrecta"

    return render_template("login.html", mensaje=mensaje)
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)

