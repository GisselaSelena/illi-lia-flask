from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/producto/<nombre_producto>')
def producto(nombre_producto):
    nombre_formateado = nombre_producto.replace('-', ' ').title()
    return render_template("producto.html", nombre=nombre_formateado)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
