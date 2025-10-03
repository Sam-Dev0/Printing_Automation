import json
import os

def cargar_datos_libros_dinamicos(carpeta_config='libros_config'):
    """
    Escanea la carpeta de configuración y carga todos los perfiles JSON.
    """
    datos_libros = {}

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    full_path = os.path.join(base_dir, carpeta_config)
    
    if not os.path.exists(full_path):
        print(f"Advertencia: La carpeta '{carpeta_config}' no existe en la raíz del proyecto. Creándola...")
        os.makedirs(full_path)
        return datos_libros
    
    for filename in os.listdir(full_path):
        if filename.endswith(".json"):
            filepath = os.path.join(full_path, filename)
            nombre_libro = filename.replace(".json", "")
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    datos_libros[nombre_libro] = json.load(f)
            except json.JSONDecodeError:
                print(f"Error al leer '{filename}': JSON mal formado. Ignorando.")
            except Exception as e:
                print(f"Error inesperado al cargar '{filename}': {e}. Ignorando.")
                
    return datos_libros