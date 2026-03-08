import sqlite3
import json
import csv
import os

BASE_DIR = os.path.dirname(__file__)

TXT_FILE = os.path.join(BASE_DIR, "data/datos.txt")
JSON_FILE = os.path.join(BASE_DIR, "data/datos.json")
CSV_FILE = os.path.join(BASE_DIR, "data/datos.csv")


# -------------------------
# SQLITE
# -------------------------

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


# -------------------------
# TXT
# -------------------------

def guardar_txt(nombre, cantidad, precio):
    with open(TXT_FILE, "a") as f:
        f.write(f"{nombre},{cantidad},{precio}\n")


def leer_txt():
    datos = []

    if not os.path.exists(TXT_FILE):
        return datos

    with open(TXT_FILE, "r") as f:
        for linea in f:

            if not linea.strip():
                continue

            partes = linea.strip().split(",")

            if len(partes) != 3:
                continue

            nombre, cantidad, precio = partes

            datos.append({
                "nombre": nombre,
                "cantidad": cantidad,
                "precio": precio
            })

    return datos


# -------------------------
# JSON
# -------------------------

def guardar_json(nombre, cantidad, precio):

    datos = []

    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as f:
            try:
                datos = json.load(f)
            except:
                datos = []

    datos.append({
        "nombre": nombre,
        "cantidad": cantidad,
        "precio": precio
    })

    with open(JSON_FILE, "w") as f:
        json.dump(datos, f, indent=4)


def leer_json():

    if not os.path.exists(JSON_FILE):
        return []

    with open(JSON_FILE, "r") as f:
        return json.load(f)


# -------------------------
# CSV
# -------------------------

def guardar_csv(nombre, cantidad, precio):

    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([nombre, cantidad, precio])


def leer_csv():

    datos = []

    if not os.path.exists(CSV_FILE):
        return datos

    with open(CSV_FILE, "r") as f:
        reader = csv.reader(f)

        for fila in reader:

            if len(fila) < 3:
                continue

            datos.append({
                "nombre": fila[0],
                "cantidad": fila[1],
                "precio": fila[2]
            })

    return datos