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

¡Claro! Para mostrar la estructura de tu proyecto en el archivo README de Git (que usa el formato Markdown), la mejor manera es usar una tabla combinada con una representación jerárquica de texto.

Aquí tienes el código Markdown que puedes copiar y pegar directamente en tu archivo README.md, basado en la estructura de tu proyecto PrintFlow:

📁 Estructura del Proyecto
Utilizamos una tabla para explicar el rol de cada componente principal y una vista de árbol para mostrar la jerarquía de directorios.

Markdown

### Vista de Árbol

```bash
BACK-AUT_LIB/
├── libros_config/
│   ├── mi_novela_a5.json
│   └── guia_tecnica.json
├── src/
│   ├── __init__.py
│   ├── data_manager.py
│   └── printer_utils.py
├── venv/
├── main.py
└── requirements.txt
Componentes Principales
Archivo/Carpeta	Tipo	Propósito Principal
main.py	Archivo Python	Punto de Entrada (GUI). Inicializa la interfaz de Tkinter, valida la entrada y orquesta el flujo de impresión/pausa en hilos separados.
src/	Paquete	Contenedor de toda la lógica interna del programa.
src/data_manager.py	Módulo	Carga dinámicamente los perfiles de impresión (.json) de la carpeta libros_config/.
src/printer_utils.py	Módulo	Contiene las funciones para interactuar con la API de Windows (pywin32) para listar impresoras y enviar trabajos.
libros_config/	Carpeta	Almacena los archivos JSON que definen los perfiles y parámetros específicos de cada trabajo de impresión.
venv/	Carpeta	Entorno Virtual. Contiene las librerías aisladas del proyecto (ej. pywin32). Debe ignorarse en Git (.gitignore).
requirements.txt	Archivo de texto	Lista las dependencias necesarias para el proyecto.

Exportar a Hojas de cálculo

### Explicación de las Herramientas Markdown

* **`###`:** Se usa para crear subtítulos dentro de una sección (`H3`).
* **Bloque de código (` ```bash `):** El bloque de código `bash` se utiliza para mostrar la estructura de árbol. Esto lo aísla visualmente del resto del texto.
* **Tabla (`|` y `---`):**
    * `| Columna 1 | Columna 2 |...|` define las celdas.
    * `| :--- | :--- |` define la alineación. **`| :--- |`** significa alineación a la izquierda (la más común).
