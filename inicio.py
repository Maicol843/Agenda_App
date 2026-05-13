import tkinter as tk
from tkinter import messagebox
import os
import sys

def abrir_archivo(nombre_archivo):
    """
    Función para cerrar la ventana actual y abrir un nuevo módulo.
    """
    try:
        # Cerramos la ventana actual de inicio
        root.destroy()
        # Ejecutamos el archivo solicitado
        os.system(f"python {nombre_archivo}")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir {nombre_archivo}: {e}")

# Configuración de la ventana principal
root = tk.Tk()
root.title("Sistema de Gestión Personal - Inicio")
root.geometry("1000x600")
root.configure(bg="#f8f9fa")

# --- FRAME LATERAL (NAVEGACIÓN) ---
frame_navegacion = tk.Frame(root, bg="#212529", width=200)
frame_navegacion.pack(side="left", fill="y")

# Título del menú
lbl_menu = tk.Label(frame_navegacion, text="MENÚ", font=("Arial", 14, "bold"), 
                    bg="#212529", fg="white", pady=20)
lbl_menu.pack()

# Lista de botones y sus archivos correspondientes
botones = [
    ("Inicio", "inicio.py"),
    ("Contactos", "contacto.py"),
    ("Contraseñas", "contrasena.py"),
    ("Calendario", "calendario.py"),
    ("Horarios", "horarios.py"),
    ("Citas", "citas.py"),
    ("Proyectos", "proyectos.py"),
    ("Hábitos", "habitos.py"),
    ("To Do List", "to_do_list.py"),
    ("Notas", "notas.py"),
    ("Entrenamiento", "entrenamiento.py"),
    ("Datos Físicos", "datos_fisicos.py"),
    ("Ingresos", "ingresos.py"),
    ("Egresos", "egresos.py"),
]

# Creación dinámica de botones
for nombre, archivo in botones:
    btn = tk.Button(frame_navegacion, text=nombre, font=("Arial", 11),
                    bg="#212529", fg="white", bd=0, padx=20, pady=10,
                    anchor="w", activebackground="#343a40", activeforeground="#20c997",
                    command=lambda a=archivo: abrir_archivo(a))
    btn.pack(fill="x")

# --- FRAME PRINCIPAL (CONTENIDO) ---
frame_contenido = tk.Frame(root, bg="white", padx=20, pady=20)
frame_contenido.pack(side="right", expand=True, fill="both")

lbl_bienvenida = tk.Label(frame_contenido, text="Panel de Inicio", 
                          font=("Arial", 24, "bold"), bg="white", fg="#333")
lbl_bienvenida.pack(pady=20)

lbl_instrucciones = tk.Label(frame_contenido, text="Selecciona una opción del menú lateral para comenzar.", 
                             font=("Arial", 12), bg="white", fg="#666")
lbl_instrucciones.pack()

root.mainloop()