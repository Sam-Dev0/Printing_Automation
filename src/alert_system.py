from plyer import notification
import time 

def emitir_alerta(libro_actual, total, nombre_libro):
    """
    Emite una notificación de escritorio para alertar al operador.
    Requiere que la librería 'plyer' esté instalada.
    """
    try:
        notification.notify(
            title=f'🚨 LIBRO COMPLETADO ({nombre_libro}) 🚨',
            message=f'La copia {libro_actual} de {total} ha finalizado. ¡Presione ENTER en la terminal para continuar!',
            app_name='PrintAutomation',
            timeout=20  
        )
    except Exception as e:
        print(f"\n🚨 ALERTA (Fallo de Notificación): Presione ENTER en la consola. {e}")