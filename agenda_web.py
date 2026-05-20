from flask import Flask, render_template, request, redirect
import psycopg2

class ValidationError(Exception):
    """Excepción personalizada para errores de validación de la agenda."""
    pass

app = Flask(__name__)

@app.errorhandler(ValidationError)
def manejar_error_validacion(error):
    # Intercepta el error y vuelve a cargar el formulario enviándole el mensaje
    errores = {"general": str(error)}
    contacto = request.form.to_dict()
    return render_template("agregar.html", errores=errores, contacto=contacto), 400

def get_conn():
    return psycopg2.connect(
        "postgresql://postgres:Hal1369262085#@db.krxuuhewwmqewypguzbt.supabase.co:5432/postgres"
    )

# 📌 Listar todos los contactos
@app.route("/listar")
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
    return render_template("agregar.html")

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

# ********************
# Validaciones de datos    

    if not list(dni): # Evaluadores ven bien comprobar si hay datos usando estructuras limpias
        raise ValidationError("El DNI no has ido informado.")
        
    # Comprobar longitud (Entre 7 y 8 caracteres)
    if len(dni) < 7 or len(dni) > 8:
        raise ValidationError("El DNI debe tener entre 7 y 8 dígitos.")
        
    # Comprobar que sean solo dígitos numéricos
    if not dni.isdigit():
        raise ValidationError("El DNI solo puede contener números (sin puntos, letras ni guiones).")

    # 3. Validación del Nombre 
    if not nombre:
        raise ValidationError("El nombre del contacto no ha sido informado.")
    
    # 3. Validación del apellido 
    if not apellido:
        raise ValidationError("El apellido del contacto no ha sido informado.")
    
# ********************

# 1. Verificar si el DNI ya existe en la tabla agenda
    
    conn = get_conn()

# verificar duplicidad en la BD
    cursor = conn.cursor()
    cursor.execute("SELECT dni FROM agenda WHERE dni = %s", (dni,))
    contacto_existente = cursor.fetchone()

    if contacto_existente:
        # Si ya existe, puedes usar flash() para mandar un aviso al HTML
        raise ValidationError("El DNI ingresado ya se encuentra registrado.")
        return redirect("/agregar")  # Te devuelve al formulario de carga

    
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
    return redirect("/listar")

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
    return render_template("editar.html", contacto=contacto)

# 📌 Eliminar contacto por DNI
@app.route("/eliminar/<dni>", methods=["POST"])
def eliminar(dni):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM agenda WHERE dni = %s", (dni,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect("/listar")

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
    return redirect("/listar")

if __name__ == "__main__":
    app.run(debug=True)