import customtkinter as ctk
from tkinter import messagebox
import database

class ContactosFrame(ctk.CTkFrame):
    # Agregamos callback_ver como parámetro obligatorio
    def __init__(self, master, callback_ver):
        super().__init__(master, fg_color="transparent")
        
        self.callback_ver = callback_ver
        self.pagina_actual = 0
        self.contactos_por_pagina = 8
        self.contacto_seleccionado = None 
        self.widgets_seleccionados = [] 

        # Título
        self.label_titulo = ctk.CTkLabel(self, text="MIS CONTACTOS", font=ctk.CTkFont(size=24, weight="bold"))
        self.label_titulo.pack(pady=(20, 10))

        # --- TOOLBAR DE ACCIONES ---
        self.frame_acciones = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_acciones.pack(pady=10)

        self.btn_agregar = ctk.CTkButton(self.frame_acciones, text="Agregar contacto", 
                                         fg_color="#198754", hover_color="#146C43",
                                         command=self.abrir_formulario)
        self.btn_agregar.pack(side="left", padx=5)

        self.btn_eliminar = ctk.CTkButton(self.frame_acciones, text="Eliminar", 
                                          fg_color="#dc3545", hover_color="#B02A37",
                                          command=self.confirmar_eliminacion)
        self.btn_eliminar.pack(side="left", padx=5)

        self.btn_restablecer = ctk.CTkButton(self.frame_acciones, text="Restablecer", 
                                             fg_color="#6c757d", hover_color="#5a6268",
                                             command=self.confirmar_restablecer)
        self.btn_restablecer.pack(side="left", padx=5)

        # Botón Ver contacto
        self.btn_ver = ctk.CTkButton(self.frame_acciones, text="Ver contacto", 
                                     fg_color="#0d6efd", hover_color="#0b5ed7",
                                     command=self.ejecutar_ver_contacto)
        self.btn_ver.pack(side="left", padx=5)

        # Buscador
        self.entry_busqueda = ctk.CTkEntry(self, placeholder_text="Buscar por nombre o apellido...", width=400)
        self.entry_busqueda.pack(pady=10)
        self.entry_busqueda.bind("<KeyRelease>", lambda event: self.actualizar_tabla())

        # --- CONTENEDOR DE TABLA ---
        self.marco_borde = ctk.CTkFrame(self, fg_color="#333333", corner_radius=10)
        self.marco_borde.pack(expand=True, fill="both", padx=40, pady=(10, 5))

        self.scroll_tabla = ctk.CTkScrollableFrame(self.marco_borde, fg_color="#1a1a1a", corner_radius=8)
        self.scroll_tabla.pack(expand=True, fill="both", padx=2, pady=2)
        
        for i in range(5):
            self.scroll_tabla.grid_columnconfigure(i, weight=1)

        self.pag_container = ctk.CTkFrame(self, fg_color="transparent")
        self.pag_container.pack(pady=10)

        self.actualizar_tabla()

    def seleccionar_contacto(self, id_contacto, fila_widgets):
        # Limpiar selección anterior
        for w in self.widgets_seleccionados:
            if w.winfo_exists():
                w.configure(fg_color="transparent")
        
        self.contacto_seleccionado = id_contacto
        self.widgets_seleccionados = fila_widgets
        
        # Aplicar color de selección
        for w in self.widgets_seleccionados:
            w.configure(fg_color="#052C65")
            
    def ejecutar_ver_contacto(self):
        if self.contacto_seleccionado is None:
            messagebox.showwarning("Atención", "Por favor, selecciona un contacto de la tabla primero.")
            return
            
        # Ejecuta de forma correcta el cambio de pantalla
        self.callback_ver(self.contacto_seleccionado)

    def confirmar_eliminacion(self):
        if self.contacto_seleccionado is None:
            messagebox.showwarning("Atención", "Por favor, selecciona un contacto de la tabla primero.")
            return

        respuesta = messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar este contacto?")
        if respuesta:
            database.eliminar_contacto(self.contacto_seleccionado)
            self.contacto_seleccionado = None
            self.widgets_seleccionados = []
            self.actualizar_tabla()

    def confirmar_restablecer(self):
        respuesta = messagebox.askyesno("ADVERTENCIA", "¿Estás seguro de eliminar TODOS los datos?")
        if respuesta:
            database.restablecer_base_datos()
            self.pagina_actual = 0
            self.actualizar_tabla()

    def abrir_formulario(self):
        ventana_form = ctk.CTkToplevel(self)
        ventana_form.title("Nuevo Contacto")
        ventana_form.geometry("600x500") 
        ventana_form.attributes("-topmost", True)
        ventana_form.grid_columnconfigure((1, 3), weight=1)

        campos = [("Nombre", "nombre"), ("Apellido", "apellido"), ("Dirección", "direccion"), 
                  ("Empresa", "empresa"), ("Teléfono", "telefono"), ("Facebook", "facebook")]
        
        self.entries = {}
        for i, (label_text, var_name) in enumerate(campos):
            row, col = i // 2, (i % 2) * 2
            ctk.CTkLabel(ventana_form, text=label_text).grid(row=row, column=col, padx=10, pady=15, sticky="e")
            entry = ctk.CTkEntry(ventana_form)
            entry.grid(row=row, column=col+1, padx=10, pady=15, sticky="ew")
            self.entries[var_name] = entry

        ctk.CTkLabel(ventana_form, text="Instagram").grid(row=3, column=0, padx=10, pady=15, sticky="e")
        self.entries["instagram"] = ctk.CTkEntry(ventana_form)
        self.entries["instagram"].grid(row=3, column=1, padx=10, pady=15, sticky="ew")

        ctk.CTkLabel(ventana_form, text="Relación").grid(row=3, column=2, padx=10, pady=15, sticky="e")
        opciones = ["Padre", "Madre", "Hermano/a", "Primo/a", "Tio/a", "Abuelo/a", "Amigo/a", "Otro"]
        self.select_relacion = ctk.CTkOptionMenu(ventana_form, values=opciones, command=self.verificar_otro)
        self.select_relacion.grid(row=3, column=3, padx=10, pady=15, sticky="ew")

        self.lbl_otro = ctk.CTkLabel(ventana_form, text="¿Cuál es?")
        self.entry_otro = ctk.CTkEntry(ventana_form, placeholder_text="Especificar...")

        def guardar():
            rel_sel = self.select_relacion.get()
            relacion_final = self.entry_otro.get() if rel_sel == "Otro" else rel_sel
            datos = (self.entries["nombre"].get(), self.entries["apellido"].get(), self.entries["direccion"].get(),
                     self.entries["empresa"].get(), self.entries["telefono"].get(), self.entries["facebook"].get(),
                     self.entries["instagram"].get(), relacion_final)
            database.insertar_contacto(datos)
            ventana_form.destroy()
            self.actualizar_tabla()

        btn_guardar = ctk.CTkButton(ventana_form, text="Guardar", command=guardar)
        btn_guardar.grid(row=5, column=0, columnspan=4, pady=30)

    def verificar_otro(self, seleccion):
        if seleccion == "Otro":
            self.lbl_otro.grid(row=4, column=2, padx=10, pady=10, sticky="e")
            self.entry_otro.grid(row=4, column=3, padx=10, pady=10, sticky="ew")
        else:
            self.lbl_otro.grid_forget()
            self.entry_otro.grid_forget()

    def actualizar_tabla(self):
        for widget in self.scroll_tabla.winfo_children():
            widget.destroy()

        headers = ["#", "Nombre", "Apellido", "Dirección", "Relación"]
        for col, text in enumerate(headers):
            lbl = ctk.CTkLabel(self.scroll_tabla, text=text, font=ctk.CTkFont(weight="bold", size=14), text_color="#0d6efd")
            lbl.grid(row=0, column=col, padx=0, pady=15, sticky="nsew")

        busqueda = self.entry_busqueda.get()
        todos_los_datos = database.obtener_contactos(busqueda)
        
        inicio = self.pagina_actual * self.contactos_por_pagina
        fin = inicio + self.contactos_por_pagina
        datos_paginados = todos_los_datos[inicio:fin]

        for row_idx, row_data in enumerate(datos_paginados):
            fila_widgets = []
            id_db = row_data[0]
            for col_idx, value in enumerate(row_data):
                lbl = ctk.CTkLabel(self.scroll_tabla, text=str(value), font=ctk.CTkFont(size=13))
                lbl.grid(row=row_idx+1, column=col_idx, padx=0, pady=1, sticky="nsew")
                
                lbl.bind("<Button-1>", lambda e, idx=id_db, fw=fila_widgets: self.seleccionar_contacto(idx, fw))
                fila_widgets.append(lbl)
        
        self.dibujar_paginacion(len(todos_los_datos), fin)

    def dibujar_paginacion(self, total_items, fin):
        for widget in self.pag_container.winfo_children():
            widget.destroy()

        btn_prev = ctk.CTkButton(self.pag_container, text="< Anterior", width=100, 
                                 fg_color="#454545", hover_color="#5a5a5a", 
                                 command=self.prev_pag,
                                 state="normal" if self.pagina_actual > 0 else "disabled")
        btn_prev.pack(side="left", padx=10)

        total_pag = (total_items - 1) // self.contactos_por_pagina + 1
        ctk.CTkLabel(self.pag_container, text=f"Página {self.pagina_actual + 1} de {max(1, total_pag)}").pack(side="left", padx=20)

        btn_next = ctk.CTkButton(self.pag_container, text="Siguiente >", width=100, 
                                 fg_color="#454545", hover_color="#5a5a5a",
                                 command=self.next_pag,
                                 state="normal" if fin < total_items else "disabled")
        btn_next.pack(side="left", padx=10)

    def next_pag(self):
        self.pagina_actual += 1
        self.actualizar_tabla()

    def prev_pag(self):
        self.pagina_actual -= 1
        self.actualizar_tabla()