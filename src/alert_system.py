from plyer import notification
import time 

def emitir_alerta(libro_actual, total, nombre_libro):
    """
    Emite una notificación de escritorio (desktop notification) usando la librería 'plyer'.

    El propósito es alertar al operador de forma visual y audible cuando una copia 
    del trabajo de impresión ha terminado, indicando que se requiere intervención manual.
    
    Esta función requiere que la librería 'plyer' esté instalada (`pip install plyer`).
    En caso de que falle la emisión de la notificación (por ejemplo, si 'plyer' no puede
    interactuar con el sistema de notificaciones del OS), se imprime un mensaje 
    de advertencia en la consola como mecanismo de respaldo.

    :param libro_actual: Número de la copia actual que acaba de finalizar (int).
    :param total: Número total de copias a imprimir para el trabajo (int).
    :param nombre_libro: El nombre del perfil del libro o trabajo que se está imprimiendo (str).
    :return: None
    """
    try:
        notification.notify(
            title=f'🚨 LIBRO COMPLETADO ({nombre_libro}) 🚨',
            message=f'La copia {libro_actual} de {total} ha finalizado. ¡Presione ENTER en la terminal para continuar!',
            app_name='PrintAutomation',
            timeout=20  # La notificación permanecerá visible por 20 segundos
        )
    except Exception as e:
        # Mecanismo de fallback: si la notificación de escritorio falla, se imprime un aviso en la consola
        print(f"\n🚨 ALERTA (Fallo de Notificación): Presione ENTER en la consola. {e}")
