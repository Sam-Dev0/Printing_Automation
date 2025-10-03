import win32print # type: ignore 
import win32api # type: ignore 
import time
import os

def listar_impresoras_disponibles():
    """
    Obtiene una lista de los nombres de las impresoras instaladas en el sistema operativo Windows.

    Utiliza la API de impresión de Windows (`win32print.EnumPrinters(2)`).

    :return: Una lista de strings que contienen los nombres de las impresoras. 
             Si ocurre un error (ej. no se está ejecutando en Windows), retorna 
             una lista con el nombre de la impresora por defecto o un placeholder.
    :rtype: list[str]
    """
    try:
        # El parámetro 2 indica que queremos enumerar impresoras locales.
        impresoras = win32print.EnumPrinters(2)
        # Extrae el segundo elemento de cada tupla (el nombre de la impresora).
        nombres = [p[1] for p in impresoras]
        return nombres
    except Exception as e:
        # Manejo de error para sistemas operativos no compatibles con win32print.
        print(f"Error (no Windows?): {e}. Usando impresora 'Defecto'.")
        # Intenta obtener la impresora por defecto si el módulo lo soporta, sino usa un placeholder.
        return [win32print.GetDefaultPrinter()] if hasattr(win32print, 'GetDefaultPrinter') else ["Impresora_Defecto"]

def enviar_a_impresora(printer_name: str, file_path: str, config: dict):
    """
    Envía un archivo (PDF o DOCX, típicamente) a una impresora específica utilizando 
    la función ShellExecute de la API de Windows.

    Nota: ShellExecute utiliza el programa asociado al tipo de archivo para manejar 
    la impresión (ej. Adobe Reader para PDF, Word para DOCX).

    :param printer_name: Nombre exacto de la impresora de destino.
    :type printer_name: str
    :param file_path: Ruta absoluta al archivo a imprimir.
    :type file_path: str
    :param config: Diccionario que contiene la configuración del trabajo. Se usa 
                   la clave 'paginas' para estimar el tiempo de espera.
    :type config: dict
    :return: Una tupla (bool, str) indicando el éxito (True/False) y un mensaje 
             de estado o error.
    :rtype: tuple[bool, str]
    """
    # 1. Validación de existencia del archivo
    if not os.path.exists(file_path):
        return False, f"ERROR: Archivo no encontrado en la ruta: {file_path}"
    
    print(f"-> [REAL] Enviando '{os.path.basename(file_path)}' a la impresora '{printer_name}'...")
    
    try:
        # 2. Ejecución de la impresión usando ShellExecute
        # "print" es la acción que le dice a Windows que imprima el archivo.
        # '/d:"%s"' % printer_name especifica a qué impresora enviar el trabajo.
        win32api.ShellExecute(
            0, # hwnd (ventana handle): 0 para no tener ventana.
            "print",
            file_path,
            '/d:"%s"' % printer_name,
            ".", # dir: Directorio de trabajo
            0    # showcmd: SW_HIDE (oculto)
        )
        
        # 3. Pausa simulada para dar tiempo a Windows de procesar el trabajo.
        # El tiempo de espera es crucial para evitar que el siguiente trabajo 
        # se envíe antes de que la impresora esté lista.
        # Se calcula en base al número de páginas (o un valor por defecto si no está en config).
        tiempo_espera = config.get('paginas', 100) / 100 + 3 
        time.sleep(tiempo_espera)
        
        return True, f"Trabajo enviado. Espera de {tiempo_espera:.1f}s."

    except Exception as e:
        return False, f"!!! ERROR al enviar trabajo: {e}"

def simular_impresion(*args):
    """
    Función de utilidad (placeholder) para simular el proceso de impresión 
    en entornos donde win32print no es accesible o para pruebas rápidas.
    Actualmente no tiene implementación, solo actúa como un stub.
    """
    # Esta función puede ser implementada para fines de desarrollo o pruebas.
    pass
