import tkinter as tk
from tkinter import messagebox, filedialog
import threading
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

from data_manager import cargar_datos_libros_dinamicos
from printer_utils import listar_impresoras_disponibles, enviar_a_impresora

class PrintFlowApp:
    def __init__(self, master):
        self.master = master
        master.title("PrintFlow - Automatización de Impresión")

        self.libros_data = cargar_datos_libros_dinamicos()
        self.impresoras = listar_impresoras_disponibles()
        self.ruta_archivo_a_imprimir = ""
        self.current_job = {}
        self.copia_actual = 0
        self.total_copias = 0
        
        self.setup_gui()
        self.update_status("Seleccione impresora, archivo y perfil.", "blue")

    def update_status(self, text, color="black"):
        """Actualiza la etiqueta de estado de la GUI."""
        self.status_label.config(text=text, fg=color)

    def setup_gui(self):
        frame = tk.Frame(self.master, padx=10, pady=10)
        frame.pack(padx=10, pady=10)

        tk.Label(frame, text="1. Archivo a Imprimir:").grid(row=0, column=0, sticky="w")
        self.file_path_label = tk.Label(frame, text="Ningún archivo seleccionado.", anchor="w", width=40)
        self.file_path_label.grid(row=0, column=1, sticky="w")
        tk.Button(frame, text="Examinar...", command=self.seleccionar_archivo).grid(row=0, column=2)

        tk.Label(frame, text="2. Seleccione Impresora:").grid(row=1, column=0, sticky="w")
        self.selected_printer = tk.StringVar(self.master)
        if self.impresoras:
            self.selected_printer.set(self.impresoras[0])
            tk.OptionMenu(frame, self.selected_printer, *self.impresoras).grid(row=1, column=1, columnspan=2, sticky="ew")
        else:
             tk.Label(frame, text="ERROR: No se encontraron impresoras.").grid(row=1, column=1, columnspan=2, sticky="ew")

        tk.Label(frame, text="3. Perfil de Libro:").grid(row=2, column=0, sticky="w")
        libros_nombres = list(self.libros_data.keys())
        if libros_nombres:
            self.selected_libro = tk.StringVar(self.master)
            self.selected_libro.set(libros_nombres[0])
            tk.OptionMenu(frame, self.selected_libro, *libros_nombres).grid(row=2, column=1, columnspan=2, sticky="ew")
        else:
            tk.Label(frame, text="ERROR: No hay perfiles cargados.").grid(row=2, column=1, columnspan=2, sticky="ew")

        tk.Label(frame, text="4. Cantidad de Copias:").grid(row=3, column=0, sticky="w")
        self.cantidad_entry = tk.Entry(frame, width=10)
        self.cantidad_entry.insert(0, "1")
        self.cantidad_entry.grid(row=3, column=1, sticky="w")

        self.start_button = tk.Button(self.master, text="INICIAR TRABAJO", command=self.validar_e_iniciar, font=('Arial', 12, 'bold'), bg='green', fg='white')
        self.start_button.pack(pady=20)
        
        self.status_label = tk.Label(self.master, text="", bd=1, relief=tk.SUNKEN, anchor="w")
        self.status_label.pack(fill='x', padx=10, pady=5)

    def seleccionar_archivo(self):
        """Abre un diálogo para que el usuario elija el archivo a imprimir."""
        self.ruta_archivo_a_imprimir = filedialog.askopenfilename(
            title="Seleccione el archivo del libro",
            filetypes=(("Archivos PDF", "*.pdf"), ("Archivos de Word", "*.docx"), ("Todos los archivos", "*.*"))
        )
        if self.ruta_archivo_a_imprimir:
            self.file_path_label.config(text=os.path.basename(self.ruta_archivo_a_imprimir), fg="green")
            self.update_status(f"Archivo cargado: {os.path.basename(self.ruta_archivo_a_imprimir)}", "blue")
        else:
            self.file_path_label.config(text="Ningún archivo seleccionado.", fg="red")

    def validar_e_iniciar(self):
        """Valida la entrada del usuario antes de iniciar el bucle."""
        try:
            if not self.ruta_archivo_a_imprimir or not os.path.exists(self.ruta_archivo_a_imprimir):
                 messagebox.showerror("Error", "Debe seleccionar un archivo válido.")
                 return
            if not self.impresoras:
                 messagebox.showerror("Error", "No hay impresoras disponibles.")
                 return

            self.total_copias = int(self.cantidad_entry.get())
            if self.total_copias <= 0:
                 messagebox.showerror("Error", "La cantidad debe ser mayor a 0.")
                 return

            nombre_elegido = self.selected_libro.get()
            self.current_job = self.libros_data[nombre_elegido]
            self.copia_actual = 1
            
            self.start_button.config(state=tk.DISABLED, text="TRABAJO EN CURSO...")
            self.update_status(f"Iniciando: {nombre_elegido} x {self.total_copias}", "orange")

            self.ejecutar_ciclo()

        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese una cantidad válida.")
        except Exception as e:
            messagebox.showerror("Error Fatal", f"Ocurrió un error al iniciar: {e}")

    def ejecutar_ciclo(self):
        """
        Lógica que maneja el flujo de copia a copia.
        Ejecuta la impresión en un HILO SEPARADO.
        """
        if self.copia_actual <= self.total_copias:
            self.update_status(f"Imprimiendo COPIA {self.copia_actual} de {self.total_copias}...", "red")
            
            thread = threading.Thread(target=self.hilo_de_impresion, daemon=True)
            thread.start()
            
            self.master.after(500, self.verificar_hilo, thread)

        else:
            self.finalizar_trabajo()

    def hilo_de_impresion(self):
        """Función que se ejecuta en el hilo secundario (donde ocurre la pausa)."""
        impresora = self.selected_printer.get()
        ruta = self.ruta_archivo_a_imprimir
        
        exito, mensaje = enviar_a_impresora(impresora, ruta, self.current_job)
        
        self.thread_result = (exito, mensaje)

    def verificar_hilo(self, thread):
        """Verifica si el hilo de impresión ha terminado."""
        if thread.is_alive():
            self.master.after(500, self.verificar_hilo, thread)
        else:
            exito, mensaje = self.thread_result
            
            if exito:
                self.pausa_confirmacion() 
            else:
                self.update_status(f"FALLO: {mensaje}", "red")
                self.start_button.config(state=tk.NORMAL, text="FALLO - REINICIAR")

    def pausa_confirmacion(self):
        """Muestra la ventana modal de alerta y pausa."""
        confirmar = messagebox.askyesno(
            "🚨 COPIA TERMINADA 🚨",
            f"La copia {self.copia_actual} de {self.total_copias} ha finalizado.\n\n"
            f"¿Está listo para mandar la siguiente copia?",
            icon=messagebox.WARNING
        )
        
        if confirmar:
            self.copia_actual += 1
            if self.copia_actual <= self.total_copias:
                self.master.after(100, self.ejecutar_ciclo) 
            else:
                self.finalizar_trabajo()
        else:
            self.update_status(f"Proceso PAUSADO en copia {self.copia_actual}. Presione START para reanudar.", "purple")
            self.start_button.config(state=tk.NORMAL, text="REANUDAR TRABAJO")

    def finalizar_trabajo(self):
        self.update_status("✅ PROCESO TERMINADO.", "green")
        self.start_button.config(state=tk.NORMAL, text="INICIAR TRABAJO")
        messagebox.showinfo("Finalizado", "Todas las copias han sido impresas y confirmadas.")


if __name__ == "__main__":
    if os.name != 'nt':
        messagebox.showerror("Advertencia", "Este programa usa API de Windows (pywin32) y podría no funcionar correctamente en su sistema operativo.")
        
    root = tk.Tk()
    app = PrintFlowApp(root)
    root.mainloop()