# gestor_escolar.py
import customtkinter as ctk
from tkinter import ttk, messagebox
from database import crear_conexion  # Usa la función de database.py
from mysql.connector import Error
from exportar_pdf import exportar_estudiantes_pdf

class GestorEscolar:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión Escolar - Colegio XYZ")
        self.root.geometry("1100x650")
        self.root.minsize(900, 600)
        
        # Configuración de tema
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("dark-blue")
        
        # Título principal
        title_frame = ctk.CTkFrame(root, fg_color="#232946")
        title_frame.pack(fill="x")
        ctk.CTkLabel(
            title_frame,
            text="Sistema de Gestión Escolar",
            font=("Segoe UI", 28, "bold"),
            text_color="#fffffe",
            bg_color="#232946"
        ).pack(pady=(18, 0))
        ctk.CTkLabel(
            title_frame,
            text="Colegio XYZ",
            font=("Segoe UI", 16, "italic"),
            text_color="#b8c1ec",
            bg_color="#232946"
        ).pack(pady=(0, 12))

        # Tabview principal
        self.tabview = ctk.CTkTabview(root, fg_color="#333", segmented_button_fg_color="#232946")
        self.tabview.pack(fill="both", expand=True, padx=30, pady=20)

        # Crear pestañas
        self.tabs = {
            "Estudiantes": self._tab_estudiantes,
            "Cursos": self._tab_cursos,
            "Profesores": self._tab_profesores,
            "Reportes": self._tab_reportes
        }
        
        for tab_name in self.tabs:
            self.tabview.add(tab_name)
            self.tabs[tab_name]()

        # Pie de página
        footer = ctk.CTkLabel(
            root,
            text="Desarrollado por TuNombre - 2025",
            font=("Segoe UI", 10),
            text_color="#232946"
        )
        footer.pack(side="bottom", pady=6)
    
    # -------------------------
    # Pestaña de Estudiantes
    # -------------------------
    def _tab_estudiantes(self):
        frame = self.tabview.tab("Estudiantes")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(3, weight=1)

        # Formulario de registro
        form_frame = ctk.CTkFrame(frame, fg_color="#fffffe", corner_radius=12)
        form_frame.grid(row=0, column=0, columnspan=2, padx=30, pady=(25, 10), sticky="ew")

        ctk.CTkLabel(form_frame, text="Registro de Estudiantes", font=("Segoe UI", 18, "bold"), text_color="#232946").grid(row=0, column=0, columnspan=2, pady=(10, 15))
        ctk.CTkLabel(form_frame, text="Nombre:", font=("Segoe UI", 13), text_color="#232946").grid(row=1, column=0, padx=10, pady=8, sticky="e")
        self.nombre_entry = ctk.CTkEntry(form_frame, width=260, font=("Segoe UI", 12))
        self.nombre_entry.grid(row=1, column=1, padx=10, pady=8, sticky="w")
        ctk.CTkLabel(form_frame, text="Edad:", font=("Segoe UI", 13), text_color="#232946").grid(row=2, column=0, padx=10, pady=8, sticky="e")
        self.edad_entry = ctk.CTkEntry(form_frame, width=100, font=("Segoe UI", 12))
        self.edad_entry.grid(row=2, column=1, padx=10, pady=8, sticky="w")
        btn_agregar = ctk.CTkButton(
            form_frame,
            text="Agregar Estudiante",
            fg_color="#232946",
            hover_color="#393e6c",
            font=("Segoe UI", 12, "bold"),
            command=self.agregar_estudiante
        )
        btn_agregar.grid(row=3, column=0, columnspan=2, pady=(18, 10))

        # Separador visual
        sep = ctk.CTkLabel(frame, text="", height=2, fg_color="#b8c1ec")
        sep.grid(row=1, column=0, columnspan=2, sticky="ew", padx=30, pady=(5, 10))

        # Tabla de estudiantes y botones
        table_frame = ctk.CTkFrame(frame, fg_color="#f5f5f5", corner_radius=12)
        table_frame.grid(row=2, column=0, columnspan=2, padx=30, pady=(0, 10), sticky="nsew")
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(table_frame, text="Listado de Estudiantes", font=("Segoe UI", 15, "bold"), text_color="#232946").grid(row=0, column=0, columnspan=4, pady=(10, 0))

        self.tree_estudiantes = ttk.Treeview(table_frame, columns=("ID", "Nombre", "Edad"), show="headings", height=12)
        self.tree_estudiantes.heading("ID", text="ID")
        self.tree_estudiantes.heading("Nombre", text="Nombre")
        self.tree_estudiantes.heading("Edad", text="Edad")
        self.tree_estudiantes.column("ID", width=60, anchor="center")
        self.tree_estudiantes.column("Nombre", width=220, anchor="center")
        self.tree_estudiantes.column("Edad", width=80, anchor="center")
        self.tree_estudiantes.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree_estudiantes.yview)
        self.tree_estudiantes.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=1, column=4, sticky="ns")

        # Botones debajo de la tabla
        btn_modificar = ctk.CTkButton(
            table_frame, text="Modificar", fg_color="#ffb703", hover_color="#fb8500",
            command=self.modificar_estudiante
        )
        btn_modificar.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        btn_guardar = ctk.CTkButton(
            table_frame, text="Guardar", fg_color="#219ebc", hover_color="#126782",
            command=self.guardar_estudiante
        )
        btn_guardar.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        btn_eliminar = ctk.CTkButton(
            table_frame, text="Eliminar", fg_color="#e63946", hover_color="#b5171e",
            command=self.eliminar_estudiante
        )
        btn_eliminar.grid(row=2, column=2, padx=5, pady=5, sticky="ew")

        # Botón Exportar PDF debajo de todo
        btn_exportar_pdf = ctk.CTkButton(
            frame, text="Exportar en PDF", fg_color="#232946", hover_color="#393e6c",
            font=("Segoe UI", 13, "bold"),
            command=self.exportar_pdf
        )
        btn_exportar_pdf.grid(row=4, column=0, columnspan=2, pady=(10, 20))

        # Cargar datos iniciales
        self.cargar_estudiantes()
    
    def agregar_estudiante(self):
        nombre = self.nombre_entry.get().strip()
        edad = self.edad_entry.get().strip()
        if not nombre or not edad.isdigit():
            messagebox.showerror("Error", "Datos inválidos. Ingrese un nombre y una edad válida.")
            return
        try:
            conexion = crear_conexion()
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO estudiantes (nombre, edad) VALUES (%s, %s)", (nombre, int(edad)))
            conexion.commit()
            messagebox.showinfo("Éxito", "Estudiante agregado correctamente.")
            self.cargar_estudiantes()
            self.nombre_entry.delete(0, "end")
            self.edad_entry.delete(0, "end")
        except Error as e:
            messagebox.showerror("Error", f"No se pudo agregar: {e}")
        finally:
            if conexion:
                conexion.close()
    
    def cargar_estudiantes(self):
        # Limpiar tabla
        for item in self.tree_estudiantes.get_children():
            self.tree_estudiantes.delete(item)
        
        # Obtener datos
        try:
            conexion = crear_conexion()
            cursor = conexion.cursor()
            cursor.execute("SELECT id, nombre, edad FROM estudiantes")
            for row in cursor.fetchall():
                self.tree_estudiantes.insert("", "end", values=row)
        except Error as e:
            messagebox.showerror("Error", f"No se pudieron cargar los datos: {e}")
        finally:
            if conexion:
                conexion.close()
    
    def eliminar_estudiante(self):
        seleccionado = self.tree_estudiantes.selection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Seleccione un estudiante para eliminar.")
            return
        id_estudiante = self.tree_estudiantes.item(seleccionado[0])["values"][0]
        if messagebox.askyesno("Confirmar", "¿Seguro que desea eliminar este estudiante?"):
            try:
                conexion = crear_conexion()
                cursor = conexion.cursor()
                cursor.execute("DELETE FROM estudiantes WHERE id=%s", (id_estudiante,))
                conexion.commit()
                self.cargar_estudiantes()
                messagebox.showinfo("Éxito", "Estudiante eliminado correctamente.")
            except Error as e:
                messagebox.showerror("Error", f"No se pudo eliminar: {e}")
            finally:
                if conexion:
                    conexion.close()
    
    def modificar_estudiante(self):
        seleccionado = self.tree_estudiantes.selection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Seleccione un estudiante para modificar.")
            return
        item = self.tree_estudiantes.item(seleccionado[0])
        id_estudiante, nombre, edad = item["values"]
        self.nombre_entry.delete(0, "end")
        self.nombre_entry.insert(0, nombre)
        self.edad_entry.delete(0, "end")
        self.edad_entry.insert(0, edad)
        self._id_modificar = id_estudiante

    def guardar_estudiante(self):
        if not hasattr(self, "_id_modificar"):
            messagebox.showwarning("Atención", "Primero seleccione un estudiante y presione Modificar.")
            return
        nombre = self.nombre_entry.get().strip()
        edad = self.edad_entry.get().strip()
        if not nombre or not edad.isdigit():
            messagebox.showerror("Error", "Datos inválidos. Ingrese un nombre y una edad válida.")
            return
        try:
            conexion = crear_conexion()
            cursor = conexion.cursor()
            cursor.execute("UPDATE estudiantes SET nombre=%s, edad=%s WHERE id=%s", (nombre, int(edad), self._id_modificar))
            conexion.commit()
            messagebox.showinfo("Éxito", "Estudiante modificado correctamente.")
            self.cargar_estudiantes()
            self.nombre_entry.delete(0, "end")
            self.edad_entry.delete(0, "end")
            del self._id_modificar
        except Error as e:
            messagebox.showerror("Error", f"No se pudo modificar: {e}")
        finally:
            if conexion:
                conexion.close()

    def exportar_pdf(self):
        estudiantes = []
        for row in self.tree_estudiantes.get_children():
            estudiantes.append(self.tree_estudiantes.item(row)["values"])
        if estudiantes:
            exportar_estudiantes_pdf(estudiantes)
            messagebox.showinfo("Exportar PDF", "PDF exportado correctamente como 'estudiantes.pdf'.")
        else:
            messagebox.showwarning("Exportar PDF", "No hay estudiantes para exportar.")

    # -------------------------
    # Pestañas restantes (similar a estudiantes)
    # -------------------------
    def _tab_cursos(self):
        frame = self.tabview.tab("Cursos")
        ctk.CTkLabel(frame, text="Próximamente: Gestión de Cursos", font=("Segoe UI", 16, "italic"), text_color="#232946").pack(pady=40)

    def _tab_profesores(self):
        frame = self.tabview.tab("Profesores")
        ctk.CTkLabel(frame, text="Próximamente: Gestión de Profesores", font=("Segoe UI", 16, "italic"), text_color="#232946").pack(pady=40)

    def _tab_reportes(self):
        frame = self.tabview.tab("Reportes")
        ctk.CTkLabel(frame, text="Próximamente: Reportes y Exportaciones", font=("Segoe UI", 16, "italic"), text_color="#232946").pack(pady=40)

# Ejecución
if __name__ == "__main__":
    root = ctk.CTk()
    app = GestorEscolar(root)
    root.mainloop()