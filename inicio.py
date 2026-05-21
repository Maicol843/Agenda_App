import customtkinter as ctk
from contacto import ContactosFrame
from ver_contacto import VerContactoFrame  # Importamos la vista detallada

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AppAgenda(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Agenda Personal Pro")
        self.geometry("1100x700")
        self.configure(fg_color="#1a1a1a")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkScrollableFrame(self, width=220, corner_radius=0, 
                                              fg_color="#212121", 
                                              scrollbar_button_color="#454545",
                                              scrollbar_button_hover_color="#5a5a5a")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar, text="MI AGENDA", 
                                       font=ctk.CTkFont(size=22, weight="bold"),
                                       text_color="white")
        self.logo_label.pack(pady=(20, 20))

        self.contenedor_principal = ctk.CTkFrame(self, corner_radius=0, fg_color="#1a1a1a")
        self.contenedor_principal.grid(row=0, column=1, sticky="nsew")

        self.crear_botones_menu()
        self.mostrar_bienvenida()

    def crear_botones_menu(self):
        opciones = [
            ("Inicio", "#0d6efd"), ("Contactos", "#454545"), 
            ("Contraseñas", "#454545"), ("Calendario", "#454545"),
            ("Horarios", "#454545"), ("Citas", "#454545"), 
            ("Proyectos", "#454545"), ("Hábitos", "#454545"),
            ("To Do List", "#454545"), ("Notas", "#454545"), 
            ("Entrenamiento", "#454545"), ("Datos Físicos", "#454545"),
            ("Ingresos", "#198754"), ("Egresos", "#dc3545")
        ]

        for texto, color in opciones:
            btn = ctk.CTkButton(self.sidebar, text=texto, 
                                fg_color=color,
                                hover_color="#5a5a5a",
                                height=40,
                                font=ctk.CTkFont(size=13),
                                command=lambda t=texto: self.cambiar_seccion(t))
            btn.pack(fill="x", padx=10, pady=5)

    def limpiar_contenedor(self):
        for widget in self.contenedor_principal.winfo_children():
            widget.destroy()

    def mostrar_bienvenida(self):
        self.limpiar_contenedor()
        label_bienvenida = ctk.CTkLabel(self.contenedor_principal, 
                                        text="Bienvenido a tu agenda app", 
                                        font=ctk.CTkFont(size=32, weight="bold"),
                                        text_color="#ffffff")
        label_bienvenida.place(relx=0.5, rely=0.5, anchor="center")

    def cambiar_seccion(self, nombre):
        self.limpiar_contenedor()
        if nombre == "Inicio":
            self.mostrar_bienvenida()
        elif nombre == "Contactos":
            # Pasamos una función lambda como callback para cambiar a la vista de detalle
            frame_contactos = ContactosFrame(
                self.contenedor_principal, 
                callback_ver=lambda id_c: self.ir_a_ver_contacto(id_c)
            )
            frame_contactos.pack(expand=True, fill="both")
        else:
            lbl = ctk.CTkLabel(self.contenedor_principal, text=f"Sección {nombre} en desarrollo")
            lbl.place(relx=0.5, rely=0.5, anchor="center")

    def ir_a_ver_contacto(self, id_contacto):
        from ver_contacto import VerContactoFrame
        self.limpiar_contenedor()
        frame_detalle = VerContactoFrame(
            self.contenedor_principal,
            id_contacto=id_contacto,
            callback_volver=lambda: self.cambiar_seccion("Contactos")
        )
        frame_detalle.pack(expand=True, fill="both")

if __name__ == "__main__":
    app = AppAgenda()
    app.mainloop()