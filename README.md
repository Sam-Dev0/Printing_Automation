📚 PrintFlow: Sistema de Automatización de Impresión por Lotes
🚀 Descripción General
PrintFlow es una aplicación de escritorio diseñada para gestionar de manera eficiente la producción repetitiva de libros. Utiliza la Interfaz Gráfica (GUI) de Tkinter y la API de Windows (pywin32) para:

Cargar perfiles de impresión dinámicamente (.json).

Enviar trabajos reales a cualquier impresora configurada.

Implementar una pausa obligatoria y una alerta visual después de cada copia para que el operador pueda intervenir (cambiar papel, revisar, cargar el siguiente archivo) sin perder la cuenta o confundir los lotes.

Ejecutar la impresión en hilos separados para evitar que la interfaz se congele.

💻 Requisitos del Sistema
Sistema Operativo: Windows (La impresión real se basa en la API pywin32).

Python: Versión 3.6 o superior.

Archivos: Los archivos a imprimir (PDF, DOCX, etc.) deben ser manejables por las aplicaciones predeterminadas de Windows.

🛠️ Instalación y Configuración
Sigue estos pasos para dejar el sistema listo para su uso.

1. Clonar el Repositorio y Crear el Entorno Virtual
Abre tu terminal en el directorio del proyecto y ejecuta:

Bash

# 1. Crear el entorno virtual
python -m venv venv

# 2. Activar el entorno virtual (depende del SO)
.\venv\Scripts\activate  # Windows
source venv/bin/activate # Linux/macOS
2. Instalar Dependencias Críticas
Con el entorno activo (debes ver (venv) en tu terminal), instala la librería pywin32 y sus dependencias:

Bash

pip install -r requirements.txt
Nota sobre pywin32: Si estás en Windows y experimentas problemas, a veces es necesario ejecutar el post-install script: python Scripts/pywin32_postinstall.py -install (dentro del venv/Scripts).

⚙️ Uso de la Aplicación (GUI)
Ejecuta la aplicación desde la terminal con el entorno virtual activado:

Bash

python main.py
Flujo de Trabajo
Selección de Archivo: Haz clic en "Examinar..." y selecciona el archivo (PDF, DOCX, etc.) que deseas imprimir en lote.

Selección de Impresora: Elige la impresora de destino de la lista desplegable (la lista se carga automáticamente).

Selección de Perfil: Elige el perfil de libro (ej., Novela_Estandar) que contiene los detalles de papel/tamaño.

Cantidad: Introduce el número total de copias.

INICIAR TRABAJO: Presiona el botón.

🚨 La Pausa Obligatoria
Después de que cada copia sea enviada a la impresora y el tiempo de espera mínimo haya transcurrido, aparecerá una ventana de confirmación emergente:

Para Continuar: El operador debe revisar el papel o cambiar el archivo fuente si es necesario, y luego hacer clic en "Sí". Esto envía el siguiente trabajo de impresión.

Para Pausar: Si el operador hace clic en "No", el proceso se detiene y puede reanudarse presionando el botón INICIAR TRABAJO de nuevo.

➕ Configuración de Nuevos Perfiles de Libro
Para añadir nuevos tipos de trabajos (perfiles) al menú de selección, simplemente crea un nuevo archivo JSON en la carpeta libros_config/ con la siguiente estructura:

Ejemplo: libros_config/Mi_Nueva_Revista.json

JSON

{
    "descripcion": "Revista a color, papel couch brillante.",
    "paginas": 64,
    "tamano": "A4",
    "papel": "Couché 130g",
    "configuracion_impresora": "Alta_Calidad_A4"
}
El campo configuracion_impresora es una etiqueta para que el operador sepa qué preset debe usar en la impresora (ya que la API de Windows tiene un control limitado sobre las bandejas/calidades sin configuración adicional).

📚 Estructura del Proyecto
El proyecto mantiene una estructura modular para facilitar el mantenimiento:

BACK-AUT_LIB/
├── venv/                       # Entorno virtual
├── libros_config/              # Contiene los perfiles de impresión (.json)
├── src/                        # Paquete con toda la lógica de la aplicación
│   ├── __init__.py             # Hace de 'src' un paquete
│   ├── data_manager.py         # Carga los perfiles .json
│   └── printer_utils.py        # Interfaz con pywin32 para impresión real
├── main.py                     # Punto de entrada de la aplicación (La GUI Tkinter)
└── requirements.txt            # Dependencias externas
