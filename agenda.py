import psycopg2
from psycopg2 import sql

# ⚠️ Cambiá estos valores por los de tu conexión Supabase/PostgreSQL
DB_URL = "postgresql://postgres:Hal1369262085#@db.krxuuhewwmqewypguzbt.supabase.co:5432/postgres"

# Conexión a la base
conn = psycopg2.connect(DB_URL)
cursor = conn.cursor()

# Crear tabla si no existe
cursor.execute("""
CREATE TABLE IF NOT EXISTS agenda (
    dni VARCHAR(10) PRIMARY KEY,
    nombre VARCHAR(50),
    apellido VARCHAR(50),
    calle VARCHAR(100),
    numero VARCHAR(10),
    codigo_postal VARCHAR(10),
    email VARCHAR(100),
    telefono VARCHAR(20),
    fecha_nacimiento DATE,
    gastos_mensuales NUMERIC(10,2)
);
""")
conn.commit()

def agregar_contacto():
    dni = input("DNI: ")
    nombre = input("Nombre: ")
    apellido = input("Apellido: ")
    calle = input("Calle: ")
    numero = input("Número: ")
    codigo_postal = input("Código Postal: ")
    email = input("Email: ")
    telefono = input("Teléfono: ")
    fecha_nacimiento = input("Fecha de nacimiento (YYYY-MM-DD): ")
    gastos_mensuales = input("Gastos mensuales: ")

    cursor.execute("""
        INSERT INTO agenda (dni, nombre, apellido, calle, numero, codigo_postal, email, telefono, fecha_nacimiento, gastos_mensuales)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (dni) DO UPDATE SET
            nombre = EXCLUDED.nombre,
            apellido = EXCLUDED.apellido,
            calle = EXCLUDED.calle,
            numero = EXCLUDED.numero,
            codigo_postal = EXCLUDED.codigo_postal,
            email = EXCLUDED.email,
            telefono = EXCLUDED.telefono,
            fecha_nacimiento = EXCLUDED.fecha_nacimiento,
            gastos_mensuales = EXCLUDED.gastos_mensuales;
    """, (dni, nombre, apellido, calle, numero, codigo_postal, email, telefono, fecha_nacimiento, gastos_mensuales))
    conn.commit()
    print("✅ Contacto guardado correctamente.")

def listar_contactos():
    cursor.execute("SELECT * FROM agenda")
    rows = cursor.fetchall()
    print("\n📋 Agenda completa:")
    for r in rows:
        print(r)

def menu():
    while True:
        print("\n--- Menú ---")
        print("1. Agregar contacto")
        print("2. Listar contactos")
        print("3. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            agregar_contacto()
        elif opcion == "2":
            listar_contactos()
        elif opcion == "3":
            break
        else:
            print("❌ Opción inválida.")

menu()

# Cerrar conexión
cursor.close()
conn.close()