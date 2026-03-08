from flask import Flask, render_template
import os

# importar funciones de persistencia
from inventario.database import guardar_txt, guardar_json, guardar_csv
from inventario.database import leer_txt, leer_json, leer_csv

app = Flask(__name__)


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


# NUEVA RUTA para mostrar los datos guardados
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


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)