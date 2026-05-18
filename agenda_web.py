from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

def get_conn():
    return psycopg2.connect(
        "postgresql://postgres:Hal1369262085#@db.krxuuhewwmqewypguzbt.supabase.co:5432/postgres"
    )

# 📌 Listar todos los contactos
@app.route("/")
def listar():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM agenda ORDER BY dni")
    contactos = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("listar.html", contactos=contactos)

# 📌 Mostrar formulario de nuevo contacto
@app.route("/nuevo")
def nuevo():
    return render_template("index.html")

# 📌 Agregar un nuevo contacto
@app.route("/agregar", methods=["POST"])
def agregar():
    dni = request.form["dni"]
    nombre = request.form["nombre"]
    apellido = request.form["apellido"]
    calle = request.form["calle"]
    numero = request.form["numero"]
    codigo_postal = request.form["codigo_postal"]
    email = request.form["email"]
    telefono = request.form["telefono"]
    fecha_nacimiento = request.form["fecha_nacimiento"]
    gastos_mensuales = request.form["gastos_mensuales"]

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO agenda (
            dni, nombre, apellido, calle, numero, codigo_postal,
            email, telefono, fecha_nacimiento, gastos_mensuales
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (
            dni, nombre, apellido, calle, numero, codigo_postal,
            email, telefono, fecha_nacimiento, gastos_mensuales
    ))
    conn.commit()
    cur.close()
    conn.close()
    return redirect("/")

# 📌 Buscar contacto por DNI
@app.route("/buscar", methods=["POST"])
def buscar():
    dni = request.form["dni"]
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM agenda WHERE dni = %s", (dni,))
    contacto = cur.fetchone()
    cur.close()
    conn.close()
    return render_template("index.html", contacto=contacto)

# 📌 Eliminar contacto por DNI
@app.route("/eliminar/<dni>", methods=["POST"])
def eliminar(dni):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM agenda WHERE dni = %s", (dni,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect("/")

# 📌 Editar contacto existente
@app.route("/editar/<dni>", methods=["POST"])
def editar(dni):
    nombre = request.form["nombre"]
    apellido = request.form["apellido"]
    calle = request.form["calle"]
    numero = request.form["numero"]
    codigo_postal = request.form["codigo_postal"]
    email = request.form["email"]
    telefono = request.form["telefono"]
    fecha_nacimiento = request.form["fecha_nacimiento"]
    gastos_mensuales = request.form["gastos_mensuales"]

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        UPDATE agenda
        SET nombre=%s, apellido=%s, calle=%s, numero=%s, codigo_postal=%s,
            email=%s, telefono=%s, fecha_nacimiento=%s, gastos_mensuales=%s
        WHERE dni=%s
    """, (
        nombre, apellido, calle, numero, codigo_postal,
        email, telefono, fecha_nacimiento, gastos_mensuales, dni
    ))
    conn.commit()
    cur.close()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)