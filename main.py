import customtkinter as ctk
from tkinter import messagebox
from inventario import GestorInventario

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class AplicacionLogiStock:
    def __init__(self, root):
        self.root = root
        self.root.title("LogiStock Pro - Búsqueda y Filtros")
        self.root.geometry("1200x750") # Aumenté un poco el ancho para que entre el ID
        
        self.gestor = GestorInventario()
        self.cambios_pendientes = {} 

        # --- ENCABEZADO ---
        self.header = ctk.CTkFrame(self.root, height=60, fg_color="transparent")
        self.header.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(self.header, text="📦 Control de Stock", font=("Roboto", 24, "bold")).pack(side="left")
        ctk.CTkButton(self.header, text="+ Nuevo Producto", fg_color="#2CC985", 
                      command=self.abrir_ventana_agregar).pack(side="right")

        # --- MARCO DE FILTROS ---
        self.frame_filtros = ctk.CTkFrame(self.root, fg_color="#2b2b2b", corner_radius=10)
        self.frame_filtros.pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(self.frame_filtros, text="🔍 Buscar:").pack(side="left", padx=(15, 5))
        self.entry_busqueda = ctk.CTkEntry(self.frame_filtros, placeholder_text="Nombre o ID...", width=200)
        self.entry_busqueda.pack(side="left", padx=5, pady=10)
        self.entry_busqueda.bind("<KeyRelease>", self.filtrar_automaticamente)

        ctk.CTkLabel(self.frame_filtros, text="Categoría:").pack(side="left", padx=(15, 5))
        self.combo_categoria = ctk.CTkComboBox(self.frame_filtros, values=["Todas"], width=150, command=self.filtrar_automaticamente)
        self.combo_categoria.pack(side="left", padx=5)

        ctk.CTkLabel(self.frame_filtros, text="Orden:").pack(side="left", padx=(15, 5))
        self.combo_orden = ctk.CTkComboBox(self.frame_filtros, 
                                           values=["Normal (ID)", "Menor Precio", "Mayor Precio"], 
                                           width=150, command=self.filtrar_automaticamente)
        self.combo_orden.pack(side="left", padx=5)

        # --- TÍTULOS DE COLUMNAS (AHORA CON ID) ---
        self.frame_titulos = ctk.CTkFrame(self.root, fg_color="#1f538d", height=30, corner_radius=5)
        self.frame_titulos.pack(fill="x", padx=20, pady=(10,0))
        
        # COLUMNA NUEVA: ID
        ctk.CTkLabel(self.frame_titulos, text="ID", width=40, anchor="center").pack(side="left", padx=5)
        
        ctk.CTkLabel(self.frame_titulos, text="Producto", width=220, anchor="w").pack(side="left", padx=5)
        ctk.CTkLabel(self.frame_titulos, text="Categoría", width=120, anchor="w").pack(side="left", padx=5)
        ctk.CTkLabel(self.frame_titulos, text="Precio", width=80, anchor="w").pack(side="left", padx=5)
        ctk.CTkLabel(self.frame_titulos, text="Mínimo", width=60, anchor="center").pack(side="left", padx=5)
        ctk.CTkLabel(self.frame_titulos, text="Stock Real / Editado", width=120, anchor="center").pack(side="left", padx=5)
        ctk.CTkLabel(self.frame_titulos, text="Acciones", width=280, anchor="center").pack(side="left", padx=5)

        # --- LISTA ---
        self.scroll_lista = ctk.CTkScrollableFrame(self.root, fg_color="transparent")
        self.scroll_lista.pack(fill="both", expand=True, padx=20, pady=5)

        self.cargar_datos_iniciales()

    def cargar_datos_iniciales(self):
        self.productos_todos = self.gestor.obtener_productos()
        self.actualizar_combo_categorias()
        self.renderizar_lista()

    def actualizar_combo_categorias(self):
        categorias = set()
        for p in self.productos_todos:
            if p[2]: categorias.add(p[2])
        lista_cat = ["Todas"] + sorted(list(categorias))
        self.combo_categoria.configure(values=lista_cat)
        self.combo_categoria.set("Todas")

    def filtrar_automaticamente(self, event=None):
        self.renderizar_lista()

    def renderizar_lista(self):
        for widget in self.scroll_lista.winfo_children():
            widget.destroy()

        if not hasattr(self, 'productos_todos'):
            self.productos_todos = self.gestor.obtener_productos()

        busqueda = self.entry_busqueda.get().lower()
        cat_seleccionada = self.combo_categoria.get()
        orden = self.combo_orden.get()

        productos_filtrados = []

        for p in self.productos_todos:
            id_prod, nombre, categoria, cantidad, precio, minimo = p
            
            coincide_texto = (busqueda in nombre.lower()) or (busqueda in str(id_prod))
            coincide_cat = (cat_seleccionada == "Todas") or (cat_seleccionada == categoria)

            if coincide_texto and coincide_cat:
                productos_filtrados.append(p)

        if orden == "Menor Precio":
            productos_filtrados.sort(key=lambda x: x[4]) 
        elif orden == "Mayor Precio":
            productos_filtrados.sort(key=lambda x: x[4], reverse=True) 
        
        for p in productos_filtrados:
            self.crear_fila_producto(p)

    def crear_fila_producto(self, p):
        id_prod, nombre, categoria, cantidad_real, precio, minimo = p
        
        en_edicion = False
        cantidad_mostrar = cantidad_real
        
        if id_prod in self.cambios_pendientes:
            en_edicion = True
            cantidad_mostrar = self.cambios_pendientes[id_prod]

        color_fondo = "#2b2b2b"
        color_texto_stock = "white"

        if en_edicion:
            color_texto_stock = "#FFD700" 
        elif cantidad_mostrar < minimo:
            color_fondo = "#550000" 
            color_texto_stock = "#FF5555"

        fila = ctk.CTkFrame(self.scroll_lista, fg_color=color_fondo, height=50)
        fila.pack(fill="x", pady=2)

        # --- AQUÍ AGREGAMOS EL ID VISUALMENTE ---
        ctk.CTkLabel(fila, text=str(id_prod), width=40, anchor="center", text_color="gray").pack(side="left", padx=5)

        ctk.CTkLabel(fila, text=nombre, width=220, anchor="w", font=("Arial", 14, "bold")).pack(side="left", padx=5)
        ctk.CTkLabel(fila, text=categoria, width=120, anchor="w").pack(side="left", padx=5)
        ctk.CTkLabel(fila, text=f"${precio}", width=80, anchor="w", text_color="#4cd137").pack(side="left", padx=5)
        ctk.CTkLabel(fila, text=f"Min: {minimo}", width=60, text_color="gray").pack(side="left", padx=5)
        ctk.CTkLabel(fila, text=str(cantidad_mostrar), width=120, 
                        font=("Arial", 16, "bold"), text_color=color_texto_stock).pack(side="left", padx=5)

        acciones = ctk.CTkFrame(fila, fg_color="transparent")
        acciones.pack(side="left", padx=10)

        ctk.CTkButton(acciones, text="-", width=30, height=30, fg_color="#e74c3c",
                        command=lambda i=id_prod, c=cantidad_real: self.ajustar_temporalmente(i, c, -1)).pack(side="left", padx=2)
        ctk.CTkButton(acciones, text="+", width=30, height=30, fg_color="#2ecc71",
                        command=lambda i=id_prod, c=cantidad_real: self.ajustar_temporalmente(i, c, 1)).pack(side="left", padx=2)
        
        if en_edicion:
            ctk.CTkButton(acciones, text="✓", width=30, height=30, fg_color="#2CC985", hover_color="#229965",
                            command=lambda i=id_prod, r=cantidad_real: self.confirmar_cambio(i, r)).pack(side="left", padx=5)
            ctk.CTkButton(acciones, text="✕", width=30, height=30, fg_color="#666", hover_color="#888",
                            command=lambda i=id_prod: self.cancelar_cambio(i)).pack(side="left", padx=2)
        else:
            ctk.CTkButton(acciones, text="⚙️ Editar", width=90, height=30, fg_color="#0056b3", hover_color="#003d80",
                            command=lambda prod=p: self.abrir_ventana_editar(prod)).pack(side="left", padx=5)
            ctk.CTkButton(acciones, text="🗑️ Borrar", width=90, height=30, fg_color="#444", hover_color="#222",
                            command=lambda i=id_prod: self.eliminar_item(i)).pack(side="left", padx=2)

    def ajustar_temporalmente(self, id_prod, stock_real, delta):
        if id_prod in self.cambios_pendientes: valor_actual = self.cambios_pendientes[id_prod]
        else: valor_actual = stock_real
        nuevo_valor = valor_actual + delta
        if nuevo_valor < 0: return
        self.cambios_pendientes[id_prod] = nuevo_valor
        self.renderizar_lista()

    def confirmar_cambio(self, id_prod, stock_real_inicial):
        nuevo_stock = self.cambios_pendientes[id_prod]
        diferencia = nuevo_stock - stock_real_inicial
        mensaje = self.gestor.actualizar_stock(id_prod, diferencia)
        if "Error" in mensaje: messagebox.showerror("Error", mensaje)
        else:
            del self.cambios_pendientes[id_prod]
            self.cargar_datos_iniciales()

    def cancelar_cambio(self, id_prod):
        if id_prod in self.cambios_pendientes: del self.cambios_pendientes[id_prod]
        self.renderizar_lista()

    def eliminar_item(self, id_prod):
        if messagebox.askyesno("Confirmar", "¿Borrar producto definitivamente?"):
            self.gestor.eliminar_producto(id_prod)
            self.cargar_datos_iniciales()

    def cerrar_modal(self):
        if hasattr(self, 'frame_modal'): self.frame_modal.destroy()
        if hasattr(self, 'fondo_bloqueo'): self.fondo_bloqueo.destroy()

    def abrir_ventana_editar(self, producto_datos):
        id_prod, nombre, categoria, cantidad, precio, minimo = producto_datos
        self.fondo_bloqueo = ctk.CTkFrame(self.root, fg_color="black")
        self.fondo_bloqueo.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.frame_modal = ctk.CTkFrame(self.root, width=400, height=450, corner_radius=15, fg_color="#333333", border_width=2, border_color="#555")
        self.frame_modal.place(relx=0.5, rely=0.5, anchor="center")

        header = ctk.CTkFrame(self.frame_modal, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=10)
        ctk.CTkLabel(header, text=f"Editar: {nombre}", font=("Arial", 16, "bold")).pack(side="left")
        ctk.CTkButton(header, text="✕", width=30, fg_color="transparent", text_color="gray", hover_color="#444", command=self.cerrar_modal).pack(side="right")

        ctk.CTkLabel(self.frame_modal, text="Categoría:").pack(pady=(5,0))
        entry_cat = ctk.CTkEntry(self.frame_modal, width=200); entry_cat.insert(0, categoria); entry_cat.pack(pady=5)
        ctk.CTkLabel(self.frame_modal, text="Precio ($):").pack(pady=(5,0))
        entry_precio = ctk.CTkEntry(self.frame_modal, width=200); entry_precio.insert(0, str(precio)); entry_precio.pack(pady=5)
        ctk.CTkLabel(self.frame_modal, text="Stock Mínimo (Alerta):").pack(pady=(5,0))
        entry_min = ctk.CTkEntry(self.frame_modal, width=200); entry_min.insert(0, str(minimo)); entry_min.pack(pady=5)
        ctk.CTkLabel(self.frame_modal, text="(El stock actual se modifica con + y -)", text_color="gray", font=("Arial", 10)).pack(pady=10)

        def guardar_cambios():
            try:
                mensaje = self.gestor.modificar_producto(id_prod, entry_cat.get(), float(entry_precio.get()), int(entry_min.get()))
                messagebox.showinfo("Gestión", mensaje)
                self.cerrar_modal()
                self.cargar_datos_iniciales()
            except ValueError: messagebox.showerror("Error", "Datos numéricos inválidos")

        ctk.CTkButton(self.frame_modal, text="💾 Guardar Cambios", command=guardar_cambios, fg_color="#0056b3", hover_color="#003d80", width=200).pack(pady=20)

    def abrir_ventana_agregar(self):
        self.fondo_bloqueo = ctk.CTkFrame(self.root, fg_color="black")
        self.fondo_bloqueo.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.frame_modal = ctk.CTkFrame(self.root, width=400, height=500, corner_radius=15, fg_color="#333333", border_width=2, border_color="#555")
        self.frame_modal.place(relx=0.5, rely=0.5, anchor="center")

        header = ctk.CTkFrame(self.frame_modal, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=10)
        ctk.CTkLabel(header, text="Nuevo Producto", font=("Arial", 18, "bold")).pack(side="left")
        ctk.CTkButton(header, text="✕", width=30, fg_color="transparent", text_color="gray", hover_color="#444", command=self.cerrar_modal).pack(side="right")

        ctk.CTkLabel(self.frame_modal, text="Nombre:").pack(pady=(5,0)); entry_nom = ctk.CTkEntry(self.frame_modal, width=250); entry_nom.pack(pady=5)
        ctk.CTkLabel(self.frame_modal, text="Categoría:").pack(pady=(5,0)); entry_cat = ctk.CTkEntry(self.frame_modal, width=250); entry_cat.pack(pady=5)
        
        frame_doble = ctk.CTkFrame(self.frame_modal, fg_color="transparent"); frame_doble.pack(pady=5)
        fr_izq = ctk.CTkFrame(frame_doble, fg_color="transparent"); fr_izq.pack(side="left", padx=5)
        ctk.CTkLabel(fr_izq, text="Cantidad:").pack(); entry_cant = ctk.CTkEntry(fr_izq, width=100); entry_cant.pack()
        fr_der = ctk.CTkFrame(frame_doble, fg_color="transparent"); fr_der.pack(side="left", padx=5)
        ctk.CTkLabel(fr_der, text="Precio:").pack(); entry_precio = ctk.CTkEntry(fr_der, width=100); entry_precio.pack()
        
        ctk.CTkLabel(self.frame_modal, text="Stock Mínimo:").pack(pady=(5,0)); entry_min = ctk.CTkEntry(self.frame_modal, width=100); entry_min.insert(0,"5"); entry_min.pack(pady=5)

        def guardar_interno():
            try:
                self.gestor.agregar_producto(entry_nom.get(), entry_cat.get(), int(entry_cant.get()), float(entry_precio.get()), int(entry_min.get()))
                self.cerrar_modal()
                self.cargar_datos_iniciales()
            except ValueError: messagebox.showerror("Error", "Datos inválidos")

        ctk.CTkButton(self.frame_modal, text="Guardar", command=guardar_interno, fg_color="#2CC985").pack(pady=20)

if __name__ == "__main__":
    root = ctk.CTk()
    app = AplicacionLogiStock(root)
    root.mainloop()