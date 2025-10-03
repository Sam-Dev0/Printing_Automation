import tkinter as tk
from tkinter import messagebox, filedialog
import threading
import sys
import os

# Agrega la carpeta 'src' al path del sistema para poder importar módulos locales.
# Esto asegura que `data_manager` y `printer_utils` sean accesibles.
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

# Importaciones de módulos personalizados
from data_manager import cargar_datos_libros_dinamicos
from printer_utils import listar_impresoras_disponibles, enviar_a_impresora

class PrintFlowApp:
    """
    Clase principal de la aplicación PrintFlow.
    Gestiona la interfaz gráfica (GUI) y el flujo de trabajo de impresión
    automatizada por copias con confirmación.
    """
    def __init__(self, master):
        """
        Inicializa la aplicación, carga los datos, encuentra impresoras y configura la GUI.

        :param master: La ventana principal (tk.Tk) de Tkinter.
        """
        self.master = master
        master.title("PrintFlow - Automatización de Impresión")

        # 1. Carga de datos iniciales
        # Carga los perfiles de impresión (settings dinámicos) desde data_manager.
        self.libros_data = cargar_datos_libros_dinamicos()
        # Obtiene una lista de impresoras disponibles en el sistema.
        self.impresoras = listar_impresoras_disponibles()

        # 2. Variables de estado de la aplicación
        self.ruta_archivo_a_imprimir = ""  # Ruta del PDF/DOCX seleccionado por el usuario.
        self.current_job = {}              # Configuración del perfil de impresión seleccionado.
        self.copia_actual = 0              # Contador de la copia que se está procesando actualmente.
        self.total_copias = 0              # Cantidad total de copias a imprimir.
        self.thread_result = None          # Variable para almacenar el resultado del hilo de impresión.
        
        # 3. Configuración de la interfaz
        self.setup_gui()
        self.update_status("Seleccione impresora, archivo y perfil.", "blue")

    def update_status(self, text, color="black"):
        """
        Actualiza la etiqueta de estado de la GUI con un mensaje y color específicos.

        :param text: El mensaje de estado a mostrar.
        :param color: El color del texto (ej. "black", "red", "green", "blue").
        """
        self.status_label.config(text=text, fg=color)

    def setup_gui(self):
        """
        Configura todos los elementos visuales de la interfaz de usuario (GUI).
        Utiliza un layout basado en Frame y Grid.
        """
        # Marco principal para contener los controles de entrada
        frame = tk.Frame(self.master, padx=10, pady=10)
        frame.pack(padx=10, pady=10)

        # 1. Selección de Archivo
        tk.Label(frame, text="1. Archivo a Imprimir:").grid(row=0, column=0, sticky="w")
        self.file_path_label = tk.Label(frame, text="Ningún archivo seleccionado.", anchor="w", width=40)
        self.file_path_label.grid(row=0, column=1, sticky="w")
        tk.Button(frame, text="Examinar...", command=self.seleccionar_archivo).grid(row=0, column=2)

        # 2. Selección de Impresora
        tk.Label(frame, text="2. Seleccione Impresora:").grid(row=1, column=0, sticky="w")
        self.selected_printer = tk.StringVar(self.master)
        if self.impresoras:
            self.selected_printer.set(self.impresoras[0]) # Selecciona la primera por defecto
            tk.OptionMenu(frame, self.selected_printer, *self.impresoras).grid(row=1, column=1, columnspan=2, sticky="ew")
        else:
            tk.Label(frame, text="ERROR: No se encontraron impresoras.").grid(row=1, column=1, columnspan=2, sticky="ew")

        # 3. Selección de Perfil de Libro
        tk.Label(frame, text="3. Perfil de Libro:").grid(row=2, column=0, sticky="w")
        libros_nombres = list(self.libros_data.keys())
        if libros_nombres:
            self.selected_libro = tk.StringVar(self.master)
            self.selected_libro.set(libros_nombres[0]) # Selecciona el primer perfil por defecto
            tk.OptionMenu(frame, self.selected_libro, *libros_nombres).grid(row=2, column=1, columnspan=2, sticky="ew")
        else:
            tk.Label(frame, text="ERROR: No hay perfiles cargados.").grid(row=2, column=1, columnspan=2, sticky="ew")

        # 4. Cantidad de Copias
        tk.Label(frame, text="4. Cantidad de Copias:").grid(row=3, column=0, sticky="w")
        self.cantidad_entry = tk.Entry(frame, width=10)
        self.cantidad_entry.insert(0, "1")
        self.cantidad_entry.grid(row=3, column=1, sticky="w")

        # Botón de Inicio del Proceso
        self.start_button = tk.Button(self.master, text="INICIAR TRABAJO", command=self.validar_e_iniciar, font=('Arial', 12, 'bold'), bg='green', fg='white')
        self.start_button.pack(pady=20)
        
        # Etiqueta de Estado (barra de estado)
        self.status_label = tk.Label(self.master, text="", bd=1, relief=tk.SUNKEN, anchor="w")
        self.status_label.pack(fill='x', padx=10, pady=5)

    def seleccionar_archivo(self):
        """
        Abre un diálogo de selección de archivo.
        Almacena la ruta del archivo y actualiza la etiqueta en la GUI.
        """
        self.ruta_archivo_a_imprimir = filedialog.askopenfilename(
            title="Seleccione el archivo del libro",
            filetypes=(("Archivos PDF", "*.pdf"), ("Archivos de Word", "*.docx"), ("Todos los archivos", "*.*"))
        )
        if self.ruta_archivo_a_imprimir:
            # Muestra solo el nombre del archivo en la etiqueta
            self.file_path_label.config(text=os.path.basename(self.ruta_archivo_a_imprimir), fg="green")
            self.update_status(f"Archivo cargado: {os.path.basename(self.ruta_archivo_a_imprimir)}", "blue")
        else:
            self.file_path_label.config(text="Ningún archivo seleccionado.", fg="red")

    def validar_e_iniciar(self):
        """
        Valida que todos los campos requeridos estén llenos correctamente
        antes de comenzar el ciclo de impresión.
        """
        try:
            # 1. Validar selección de archivo
            if not self.ruta_archivo_a_imprimir or not os.path.exists(self.ruta_archivo_a_imprimir):
                messagebox.showerror("Error", "Debe seleccionar un archivo válido.")
                return
            
            # 2. Validar impresoras disponibles
            if not self.impresoras:
                messagebox.showerror("Error", "No hay impresoras disponibles.")
                return

            # 3. Validar cantidad de copias
            self.total_copias = int(self.cantidad_entry.get())
            if self.total_copias <= 0:
                messagebox.showerror("Error", "La cantidad debe ser mayor a 0.")
                return

            # 4. Configurar el trabajo actual
            nombre_elegido = self.selected_libro.get()
            self.current_job = self.libros_data[nombre_elegido]
            self.copia_actual = 1 # Reinicia el contador de copias
            
            # 5. Deshabilitar el botón de inicio y actualizar el estado
            self.start_button.config(state=tk.DISABLED, text="TRABAJO EN CURSO...")
            self.update_status(f"Iniciando: {nombre_elegido} x {self.total_copias}", "orange")

            # 6. Iniciar el ciclo de impresión
            self.ejecutar_ciclo()

        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese una cantidad numérica válida.")
        except Exception as e:
            # Captura errores en la carga del perfil o lógica inicial.
            messagebox.showerror("Error Fatal", f"Ocurrió un error al iniciar: {e}")

    def ejecutar_ciclo(self):
        """
        Controla el flujo de impresión. Verifica si hay copias pendientes y,
        de haberlas, inicia un hilo de impresión para la copia actual.
        """
        if self.copia_actual <= self.total_copias:
            # Si aún quedan copias, se prepara para imprimir la siguiente.
            self.update_status(f"Imprimiendo COPIA {self.copia_actual} de {self.total_copias}...", "red")
            
            # Iniciar la impresión en un hilo separado para no congelar la GUI.
            thread = threading.Thread(target=self.hilo_de_impresion, daemon=True)
            thread.start()
            
            # Llama a `verificar_hilo` después de 500ms para empezar a monitorear.
            self.master.after(500, self.verificar_hilo, thread)

        else:
            # Si ya se completaron todas las copias.
            self.finalizar_trabajo()

    def hilo_de_impresion(self):
        """
        Función que contiene la lógica de impresión real y se ejecuta en un hilo secundario.
        Esta función llama a la utilidad externa `enviar_a_impresora`.
        Almacena el resultado de la impresión en `self.thread_result`.
        """
        impresora = self.selected_printer.get()
        ruta = self.ruta_archivo_a_imprimir
        
        # Llama a la función de impresión (puede tardar o fallar)
        exito, mensaje = enviar_a_impresora(impresora, ruta, self.current_job)
        
        # Almacena el resultado para ser leído por el hilo principal (GUI)
        self.thread_result = (exito, mensaje)

    def verificar_hilo(self, thread):
        """
        Método llamado periódicamente por `self.master.after` para verificar
        si el hilo de impresión ha finalizado.
        
        :param thread: El objeto Thread que está ejecutando la impresión.
        """
        if thread.is_alive():
            # Si el hilo sigue activo, vuelve a verificar en 500ms.
            self.master.after(500, self.verificar_hilo, thread)
        else:
            # El hilo ha terminado. Recupera el resultado y actúa en consecuencia.
            exito, mensaje = self.thread_result
            
            if exito:
                # Si la impresión se mandó correctamente, muestra la pausa de confirmación.
                self.pausa_confirmacion() 
            else:
                # Si hubo un fallo al mandar el trabajo.
                self.update_status(f"FALLO: {mensaje}", "red")
                self.start_button.config(state=tk.NORMAL, text="FALLO - REINICIAR")

    def pausa_confirmacion(self):
        """
        Muestra la ventana modal de alerta (askyesno) para solicitar
        la confirmación del usuario antes de continuar con la siguiente copia.
        Esto actúa como la pausa obligatoria.
        """
        confirmar = messagebox.askyesno(
            "🚨 COPIA TERMINADA 🚨",
            f"La copia {self.copia_actual} de {self.total_copias} ha finalizado.\n\n"
            f"¿Está listo para mandar la siguiente copia?",
            icon=messagebox.WARNING
        )
        
        if confirmar:
            # Si el usuario confirma, incrementa el contador y continúa el ciclo.
            self.copia_actual += 1
            if self.copia_actual <= self.total_copias:
                # Continúa con la siguiente copia después de un breve retraso
                self.master.after(100, self.ejecutar_ciclo) 
            else:
                # Todas las copias han sido procesadas
                self.finalizar_trabajo()
        else:
            # Si el usuario elige "No", pausa el proceso y habilita el botón para reanudar.
            self.update_status(f"Proceso PAUSADO en copia {self.copia_actual}. Presione START para reanudar.", "purple")
            self.start_button.config(state=tk.NORMAL, text="REANUDAR TRABAJO")

    def finalizar_trabajo(self):
        """
        Restablece el estado de la aplicación una vez que se han completado
        todas las copias.
        """
        self.update_status("✅ PROCESO TERMINADO.", "green")
        self.start_button.config(state=tk.NORMAL, text="INICIAR TRABAJO")
        messagebox.showinfo("Finalizado", "Todas las copias han sido impresas y confirmadas.")


if __name__ == "__main__":
    # La impresión de archivos típicamente requiere librerías específicas del SO.
    # Se añade una advertencia si el programa no se ejecuta en Windows (nt).
    if os.name != 'nt':
        messagebox.showerror("Advertencia", "Este programa usa API de Windows (pywin32) y podría no funcionar correctamente en su sistema operativo.")
        
    # Inicialización de la aplicación Tkinter
    root = tk.Tk()
    app = PrintFlowApp(root)
    # Inicia el bucle principal de Tkinter
    root.mainloop()