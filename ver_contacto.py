import customtkinter as ctk
from tkinter import messagebox, filedialog
from PIL import Image
import database
import os
import shutil

class VerContactoFrame(ctk.CTkFrame):
    def __init__(self, master, id_contacto, callback_volver):
        super().__init__(master, fg_color="transparent")
        
        self.id_contacto = id_contacto
        self.callback_volver = callback_volver
        
        # Color azul de acento para la consistencia visual
        self.color_acento = "#3a86ff"

        # Crear la carpeta de imágenes en el proyecto si no existe
        self.carpeta_imagenes = os.path.join(os.path.dirname(__file__), "contactos_imagenes")
        if not os.path.exists(self.carpeta_imagenes):
            os.makedirs(self.carpeta_imagenes)

        # Cargar los datos completos desde la base de datos
        self.cargar_datos()

        # --- TOOLBAR DE ACCIONES ---
        self.toolbar = ctk.CTkFrame(self, fg_color="#212121", height=50, corner_radius=0)
        self.toolbar.pack(fill="x", side="top")
        
        self.btn_volver = ctk.CTkButton(self.toolbar, text="← Volver a la lista", width=120,
                                         fg_color="#454545", hover_color="#5a5a5a",
                                         command=self.callback_volver, corner_radius=8)
        self.btn_volver.pack(side="left", padx=15, pady=10)

        # --- TÍTULO PRINCIPAL CENTRADO ---
        nombre_completo = f"{self.datos[1]} {self.datos[2]}".upper()
        self.lbl_titulo = ctk.CTkLabel(self, text=nombre_completo, font=ctk.CTkFont(size=28, weight="bold"))
        self.lbl_titulo.pack(pady=(25, 15), side="top")

        # --- CONTENEDOR DE LA ESTRUCTURA ---
        self.contenido_bloque = ctk.CTkFrame(self, fg_color="transparent")
        self.contenido_bloque.pack(expand=True, fill="both", padx=50, pady=10)

        # Le damos mucho más peso/ancho a la columna izquierda (3 frente a 1)
        self.contenido_bloque.grid_columnconfigure(0, weight=3) # Izquierda (Datos personales más ancho)
        self.contenido_bloque.grid_columnconfigure(1, weight=1) # Derecha (Imagen y Botones de acción)
        self.contenido_bloque.grid_rowconfigure(0, weight=1)

        # =====================================================================
        # PARTE IZQUIERDA: TARJETA DE DATOS PERSONALES
        # =====================================================================
        self.col_izquierda_datos = ctk.CTkFrame(self.contenido_bloque, fg_color="#262626", corner_radius=12)
        self.col_izquierda_datos.grid(row=0, column=0, sticky="nsew", padx=(0, 20), pady=10)
        
        self.col_derecha_interna = ctk.CTkFrame(self.col_izquierda_datos, fg_color="transparent")
        self.col_derecha_interna.pack(expand=True, fill="both", padx=25, pady=25)

        self.dibujar_bloque_datos()

        # =====================================================================
        # PARTE DERECHA: IMAGEN Y BOTONES CENTRADOS ABAJO
        # =====================================================================
        self.col_derecha_media = ctk.CTkFrame(self.contenido_bloque, fg_color="transparent")
        self.col_derecha_media.grid(row=0, column=1, sticky="nsew", padx=(20, 0), pady=10)
        
        # Estructura interna de la derecha en filas fijas
        self.col_derecha_media.grid_columnconfigure(0, weight=1)
        self.col_derecha_media.grid_rowconfigure(0, weight=0) # Fila Imagen
        self.col_derecha_media.grid_rowconfigure(1, weight=0) # Fila Botón Cargar Imagen
        self.col_derecha_media.grid_rowconfigure(2, weight=0) # Fila Botón Editar Contacto

        # Contenedor visual para enmarcar la imagen de perfil
        self.frame_marco_img = ctk.CTkFrame(self.col_derecha_media, fg_color="#262626", width=240, height=240, corner_radius=10)
        self.frame_marco_img.grid(row=0, column=0, pady=(0, 15))
        self.frame_marco_img.grid_propagate(False)

        self.lbl_avatar = ctk.CTkLabel(self.frame_marco_img, text="")
        self.lbl_avatar.place(relx=0.5, rely=0.5, anchor="center")
        
        # Carga y muestra la foto
        self.mostrar_imagen_contacto()

        # Botón 1: Cargar Imagen (Centrado debajo de la foto)
        self.btn_cargar_img = ctk.CTkButton(self.col_derecha_media, text="Cargar imagen", 
                                            fg_color="#454545", hover_color="#5a5a5a",
                                            command=self.seleccionar_y_guardar_imagen, 
                                            corner_radius=8, width=200, height=38)
        self.btn_cargar_img.grid(row=1, column=0, pady=8)

        # Botón 2: Editar Contacto (Centrado debajo de Cargar Imagen)
        self.btn_editar = ctk.CTkButton(self.col_derecha_media, text="Editar contacto", 
                                        fg_color="#0d6efd", hover_color="#0b5ed7", 
                                        command=self.abrir_formulario_edicion, 
                                        corner_radius=8, width=200, height=38)
        self.btn_editar.grid(row=2, column=0, pady=8)

    def cargar_datos(self):
        self.datos = database.obtener_contacto_por_id(self.id_contacto)

    def mostrar_imagen_contacto(self):
        ruta_guardada = self.datos[9] if len(self.datos) > 9 else None
        size = (220, 220)

        if ruta_guardada and os.path.exists(ruta_guardada):
            try:
                img_pil = Image.open(ruta_guardada)
                ctk_img = ctk.CTkImage(light_image=img_pil, dark_image=img_pil, size=size)
                self.lbl_avatar.configure(image=ctk_img, text="")
                return
            except Exception as e:
                print(f"Error al cargar la imagen guardada: {e}")

        try:
            img_placeholder = ctk.CTkImage(light_image=Image.new("RGB", size, "#3d3d3d"),
                                           dark_image=Image.new("RGB", size, "#3d3d3d"),
                                           size=size)
            self.lbl_avatar.configure(image=img_placeholder, text="")
        except Exception:
            self.lbl_avatar.configure(text="[ Imagen ]")

    def seleccionar_y_guardar_imagen(self):
        ruta_origen = filedialog.askopenfilename(filetypes=[("Archivos de Imagen", "*.png *.jpg *.jpeg *.bmp")])
        if not ruta_origen:
            return

        try:
            _, extension = os.path.splitext(ruta_origen)
            nombre_archivo = f"contacto_{self.id_contacto}{extension.lower()}"
            ruta_destino = os.path.join(self.carpeta_imagenes, nombre_archivo)

            shutil.copy2(ruta_origen, ruta_destino)
            database.actualizar_imagen_contacto(self.id_contacto, ruta_destino)

            self.cargar_datos()
            self.mostrar_imagen_contacto()
            messagebox.showinfo("Éxito", "Imagen guardada y actualizada correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la imagen de perfil: {e}")

    def dibujar_bloque_datos(self):
        for w in self.col_derecha_interna.winfo_children():
            w.destroy()

        fuente_lbl = ctk.CTkFont(size=14, weight="normal")
        fuente_val = ctk.CTkFont(size=15, weight="normal")

        campos = [
            ("Relación:", self.datos[8]),
            ("Dirección:", self.datos[3]),
            ("Teléfono:", self.datos[5]),
            ("Empresa:", self.datos[4])
        ]

        for lbl_txt, val_txt in campos:
            f = ctk.CTkFrame(self.col_derecha_interna, fg_color="transparent")
            f.pack(fill="x", pady=8, anchor="nw") 
            
            lbl = ctk.CTkLabel(f, text=lbl_txt, font=fuente_lbl, width=100, anchor="nw", text_color="#aaaaaa")
            lbl.pack(side="left", anchor="nw")
            
            # Aumentamos wraplength a 450 para aprovechar el espacio extra a lo ancho
            val = ctk.CTkLabel(f, text=str(val_txt) if val_txt else "No especificado", font=fuente_val, anchor="nw", text_color="#ffffff")
            val.configure(wraplength=450)
            val.pack(side="left", padx=10, expand=True, fill="x", anchor="nw")

        # Subtítulo Redes Sociales
        ctk.CTkLabel(self.col_derecha_interna, text="REDES SOCIALES", font=ctk.CTkFont(size=12, weight="bold"), text_color=self.color_acento).pack(pady=(30, 10), anchor="nw")

        redes = [
            ("Facebook:", self.datos[6]),
            ("Instagram:", self.datos[7])
        ]

        for lbl_txt, val_txt in redes:
            f = ctk.CTkFrame(self.col_derecha_interna, fg_color="transparent")
            f.pack(fill="x", pady=6, anchor="nw")
            
            lbl = ctk.CTkLabel(f, text=lbl_txt, font=fuente_lbl, width=100, anchor="nw", text_color="#aaaaaa")
            lbl.pack(side="left", anchor="nw")
            
            val = ctk.CTkLabel(f, text=str(val_txt) if val_txt else "No especificado", font=fuente_val, anchor="nw", text_color="#ffffff")
            val.configure(wraplength=450)
            val.pack(side="left", padx=10, expand=True, fill="x", anchor="nw")

    def abrir_formulario_edicion(self):
        ventana_edit = ctk.CTkToplevel(self)
        ventana_edit.title("Editar Contacto")
        ventana_edit.geometry("600x540")
        ventana_edit.attributes("-topmost", True)
        ventana_edit.grid_columnconfigure((1, 3), weight=1)

        campos_config = [
            ("Nombre", "nombre", self.datos[1]),
            ("Apellido", "apellido", self.datos[2]),
            ("Dirección", "direccion", self.datos[3]),
            ("Empresa", "empresa", self.datos[4]),
            ("Teléfono", "telefono", self.datos[5]),
            ("Facebook", "facebook", self.datos[6])
        ]
        
        entries = {}
        for i, (label_text, var_name, valor_previo) in enumerate(campos_config):
            row, col = i // 2, (i % 2) * 2
            ctk.CTkLabel(ventana_edit, text=label_text).grid(row=row, column=col, padx=10, pady=15, sticky="e")
            entry = ctk.CTkEntry(ventana_edit, corner_radius=8)
            entry.insert(0, valor_previo if valor_previo else "")
            entry.grid(row=row, column=col+1, padx=10, pady=15, sticky="ew")
            entries[var_name] = entry

        ctk.CTkLabel(ventana_edit, text="Instagram").grid(row=3, column=0, padx=10, pady=15, sticky="e")
        entries["instagram"] = ctk.CTkEntry(ventana_edit, corner_radius=8)
        entries["instagram"].insert(0, self.datos[7] if self.datos[7] else "")
        entries["instagram"].grid(row=3, column=1, padx=10, pady=15, sticky="ew")

        ctk.CTkLabel(ventana_edit, text="Relación").grid(row=3, column=2, padx=10, pady=15, sticky="e")
        opciones = ["Padre", "Madre", "Hermano/a", "Primo/a", "Tio/a", "Abuelo/a", "Amigo/a", "Otro"]
        
        select_relacion = ctk.CTkOptionMenu(ventana_edit, values=opciones, corner_radius=8, command=lambda sel: verificar_otro_edicion(sel))
        
        lbl_otro = ctk.CTkLabel(ventana_edit, text="¿Cuál es?")
        entry_otro = ctk.CTkEntry(ventana_edit, placeholder_text="Especificar...", corner_radius=8)

        if self.datos[8] in opciones:
            select_relacion.set(self.datos[8])
        else:
            select_relacion.set("Otro")
            entry_otro.insert(0, self.datos[8] if self.datos[8] else "")
            lbl_otro.grid(row=4, column=2, padx=10, pady=10, sticky="e")
            entry_otro.grid(row=4, column=3, padx=10, pady=10, sticky="ew")

        select_relacion.grid(row=3, column=3, padx=10, pady=15, sticky="ew")

        def verificar_otro_edicion(seleccion):
            if seleccion == "Otro":
                lbl_otro.grid(row=4, column=2, padx=10, pady=10, sticky="e")
                entry_otro.grid(row=4, column=3, padx=10, pady=10, sticky="ew")
            else:
                lbl_otro.grid_forget()
                entry_otro.grid_forget()

        def guardar_cambios():
            rel_sel = select_relacion.get()
            relacion_final = entry_otro.get() if rel_sel == "Otro" else rel_sel

            nuevos_datos = (
                entries["nombre"].get(), entries["apellido"].get(), entries["direccion"].get(),
                entries["empresa"].get(), entries["telefono"].get(), entries["facebook"].get(),
                entries["instagram"].get(), relacion_final
            )
            database.actualizar_contacto(self.id_contacto, nuevos_datos)
            ventana_edit.destroy()
            
            self.cargar_datos()
            nombre_completo = f"{self.datos[1]} {self.datos[2]}".upper()
            self.lbl_titulo.configure(text=nombre_completo)
            self.dibujar_bloque_datos()

        btn_guardar = ctk.CTkButton(ventana_edit, text="Guardar Cambios", command=guardar_cambios, 
                                     fg_color="#198754", hover_color="#146C43", corner_radius=8, height=35)
        btn_guardar.grid(row=5, column=0, columnspan=4, pady=30)