import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


from src.data_manager import cargar_datos_libros_dinamicos
from src.printer_utils import simular_impresion
from src.alert_system import emitir_alerta

def ejecutar_programa():
    print("\n--- Sistema de Automatización de Impresión ---")

    datos_libros = cargar_datos_libros_dinamicos()
    
    if not datos_libros:
        print("--- 🚨 ATENCIÓN 🚨 ---")
        print("No se encontró ningún perfil de libro. Cree archivos .json en 'libros_config/'.")
        return

    print("\nCatálogo de Perfiles Disponibles:")
    nombres_libros = list(datos_libros.keys())
    for i, nombre in enumerate(nombres_libros):
        descripcion = datos_libros[nombre].get("descripcion", "Sin descripción")
        print(f"[{i+1}] {nombre} - ({descripcion})")


    try:
        eleccion_idx = int(input("\nEscriba el NÚMERO del perfil a imprimir: ")) - 1
        nombre_elegido = nombres_libros[eleccion_idx]
        configuracion_libro = datos_libros[nombre_elegido]
        
        cantidad = int(input(f"¿Cuántas COPIAS de '{nombre_elegido}' va a imprimir?: "))
    except (ValueError, IndexError):
        print("Selección o cantidad no válida. Terminando.")
        return
        
    print(f"\n✅ INICIANDO: {cantidad} copias de {nombre_elegido} (Config: {configuracion_libro['configuracion_impresora']})")
    

    for i in range(1, cantidad + 1):
        print(f"\n>>> COPIA {i} de {cantidad} INICIADA <<<")
        

        simular_impresion(i, configuracion_libro) 
        
        print(f"✅ COPIA {i} COMPLETADA.")
        

        emitir_alerta(i, cantidad, nombre_elegido) 
        

        if i < cantidad:
            input(">>> Presione ENTER para mandar la SIGUIENTE copia...")
            
    print("\n--- ✅ PROCESO DE IMPRESIÓN TERMINADO ---")

if __name__ == "__main__":
    ejecutar_programa()