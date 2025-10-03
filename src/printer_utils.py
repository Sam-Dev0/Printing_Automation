import win32print # type: ignore 
import win32api # type: ignore 
import time
import os

def listar_impresoras_disponibles():
    """Obtiene una lista de los nombres de las impresoras instaladas en Windows."""
    try:
        impresoras = win32print.EnumPrinters(2)
        nombres = [p[1] for p in impresoras]
        return nombres
    except Exception as e:
        print(f"Error (no Windows?): {e}. Usando impresora 'Defecto'.")
        return [win32print.GetDefaultPrinter()] if hasattr(win32print, 'GetDefaultPrinter') else ["Impresora_Defecto"]

def enviar_a_impresora(printer_name: str, file_path: str, config: dict):
    """
    Envía un archivo a la impresora. Retorna True si el trabajo fue enviado.
    """
    if not os.path.exists(file_path):
        return False, f"ERROR: Archivo no encontrado en la ruta: {file_path}"
    
    print(f"-> [REAL] Enviando '{os.path.basename(file_path)}' a la impresora '{printer_name}'...")
    
    try:
        win32api.ShellExecute(
            0,
            "print",
            file_path,
            '/d:"%s"' % printer_name,
            ".",
            0
        )
        
        tiempo_espera = config.get('paginas', 100) / 100 + 3 
        time.sleep(tiempo_espera)
        
        return True, f"Trabajo enviado. Espera de {tiempo_espera:.1f}s."

    except Exception as e:
        return False, f"!!! ERROR al enviar trabajo: {e}"

def simular_impresion(*args):
    pass