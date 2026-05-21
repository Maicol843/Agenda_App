import sqlite3

def conectar():
    return sqlite3.connect("agenda_datos.db")

def crear_tabla():
    conexion = conectar()
    cursor = conexion.cursor()
    # Creamos la tabla incluyendo 'relacion' y 'ruta_imagen' desde el inicio
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
            relacion TEXT,
            ruta_imagen TEXT
        )
    ''')
    
    # Migraciones por si la base de datos ya existía sin estas columnas
    try:
        cursor.execute('ALTER TABLE contactos ADD COLUMN relacion TEXT')
    except sqlite3.OperationalError:
        pass # La columna ya existe
        
    try:
        cursor.execute('ALTER TABLE contactos ADD COLUMN ruta_imagen TEXT')
    except sqlite3.OperationalError:
        pass # La columna ya existe
        
    conexion.commit()
    conexion.close()

def insertar_contacto(datos):
    conexion = conectar()
    cursor = conexion.cursor()
    query = '''INSERT INTO contactos (nombre, apellido, direccion, empresa, telefono, facebook, instagram, relacion) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
    cursor.execute(query, datos)
    conexion.commit()
    conexion.close()

def obtener_contactos(busqueda=""):
    conexion = conectar()
    cursor = conexion.cursor()
    if busqueda:
        query = "SELECT id, nombre, apellido, direccion, relacion FROM contactos WHERE nombre LIKE ? OR apellido LIKE ?"
        cursor.execute(query, (f'%{busqueda}%', f'%{busqueda}%'))
    else:
        query = "SELECT id, nombre, apellido, direccion, relacion FROM contactos"
        cursor.execute(query)
    rows = cursor.fetchall()
    conexion.close()
    return rows

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
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='contactos'")
    conexion.commit()
    conexion.close()

def obtener_contacto_por_id(id_contacto):
    conexion = conectar()
    cursor = conexion.cursor()
    # Añadimos 'ruta_imagen' al SELECT (será el índice 9 en la tupla resultante)
    cursor.execute("""
        SELECT id, nombre, apellido, direccion, empresa, telefono, facebook, instagram, relacion, ruta_imagen 
        FROM contactos 
        WHERE id = ?
    """, (id_contacto,))
    row = cursor.fetchone()
    conexion.close()
    return row

def actualizar_contacto(id_contacto, datos):
    conexion = conectar()
    cursor = conexion.cursor()
    query = '''UPDATE contactos 
               SET nombre=?, apellido=?, direccion=?, empresa=?, telefono=?, facebook=?, instagram=?, relacion=? 
               WHERE id=?'''
    cursor.execute(query, datos + (id_contacto,))
    conexion.commit()
    conexion.close()

def actualizar_imagen_contacto(id_contacto, ruta_imagen):
    """Guarda o actualiza la ruta de la imagen local del contacto en la base de datos."""
    conexion = conectar()
    cursor = conexion.cursor()
    query = "UPDATE contactos SET ruta_imagen = ? WHERE id = ?"
    cursor.execute(query, (ruta_imagen, id_contacto))
    conexion.commit()
    conexion.close()

# Ejecutar la creación de tablas al importar el módulo
crear_tabla()