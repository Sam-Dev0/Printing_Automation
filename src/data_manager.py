import json
import os

def cargar_datos_libros_dinamicos(carpeta_config='libros_config'):
    """
    Escanea la carpeta de configuración especificada para cargar todos los perfiles 
    de impresión de libros definidos en archivos JSON.

    La función está diseñada para ser flexible:
    1. Resuelve la ruta absoluta asumiendo que `carpeta_config` se encuentra 
       en la raíz del proyecto (dos niveles por encima del script actual).
    2. Si la carpeta no existe, la crea y devuelve un diccionario vacío.
    3. Itera sobre los archivos `.json` y los carga.
    4. Incluye manejo de errores para archivos JSON mal formados (`json.JSONDecodeError`).

    :param carpeta_config: El nombre de la carpeta que contiene los archivos JSON.
                           Por defecto es 'libros_config'.
    :type carpeta_config: str
    :return: Un diccionario (dict) donde la clave es el nombre del perfil (nombre del archivo JSON sin extensión) 
             y el valor es el contenido del perfil decodificado (otro diccionario o lista).
    :rtype: dict
    """
    datos_libros = {}

    # Determina la ruta absoluta de la carpeta de configuración.
    # Sube dos niveles (os.path.dirname anidado) para encontrar la carpeta 'libros_config' en la raíz del proyecto.
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    full_path = os.path.join(base_dir, carpeta_config)
    
    # Verifica si la carpeta existe. Si no, la crea y retorna un diccionario vacío, 
    # ya que no hay perfiles para cargar.
    if not os.path.exists(full_path):
        print(f"Advertencia: La carpeta '{carpeta_config}' no existe en la raíz del proyecto. Creándola...")
        os.makedirs(full_path)
        return datos_libros
    
    # Itera sobre todos los archivos en la carpeta de configuración.
    for filename in os.listdir(full_path):
        # Procesa solo archivos con extensión .json.
        if filename.endswith(".json"):
            filepath = os.path.join(full_path, filename)
            # El nombre del libro/perfil es el nombre del archivo sin la extensión.
            nombre_libro = filename.replace(".json", "")
            
            try:
                # Abre el archivo en modo lectura con codificación UTF-8.
                with open(filepath, 'r', encoding='utf-8') as f:
                    datos_libros[nombre_libro] = json.load(f)
            except json.JSONDecodeError:
                # Maneja el error si el contenido del archivo no es un JSON válido.
                print(f"Error al leer '{filename}': JSON mal formado. Ignorando.")
            except Exception as e:
                # Manejo de cualquier otro error durante la lectura (ej. error de permisos).
                print(f"Error inesperado al cargar '{filename}': {e}. Ignorando.")
                
    # Devuelve el diccionario de perfiles cargados.
    return datos_libros