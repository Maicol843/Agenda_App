import sqlite3

def conectar():
    return sqlite3.connect("agenda_datos.db")

def crear_tabla():
    conexion = conectar()
    cursor = conexion.cursor()
    # Agregamos el campo relacion a la creación inicial
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contactos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            direccion TEXT,
            empresa TEXT,
            telefono TEXT,
            facebook TEXT,
            instagram TEXT,
            relacion TEXT
        )
    ''')
    
    # Intenta agregar la columna si la tabla ya existe sin ella
    try:
        cursor.execute('ALTER TABLE contactos ADD COLUMN relacion TEXT')
    except sqlite3.OperationalError:
        pass # La columna ya existe
        
    conexion.commit()
    conexion.close()

def insertar_contacto(datos):
    conexion = conectar()
    cursor = conexion.cursor()
    # Actualizamos la query para incluir el 8vo valor (relacion)
    query = '''INSERT INTO contactos (nombre, apellido, direccion, empresa, telefono, facebook, instagram, relacion) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
    cursor.execute(query, datos)
    conexion.commit()
    conexion.close()

def obtener_contactos(busqueda=""):
    conexion = conectar()
    cursor = conexion.cursor()
    # Seleccionamos también el campo relacion para la tabla
    if busqueda:
        query = "SELECT id, nombre, apellido, direccion, relacion FROM contactos WHERE nombre LIKE ? OR apellido LIKE ?"
        cursor.execute(query, (f'%{busqueda}%', f'%{busqueda}%'))
    else:
        query = "SELECT id, nombre, apellido, direccion, relacion FROM contactos"
        cursor.execute(query)
    rows = cursor.fetchall()
    conexion.close()
    return rows

crear_tabla()


def eliminar_contacto(id_contacto):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM contactos WHERE id = ?", (id_contacto,))
    conexion.commit()
    conexion.close()

def restablecer_base_datos():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM contactos")
    # Opcional: Reiniciar el contador de IDs
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='contactos'")
    conexion.commit()
    conexion.close()