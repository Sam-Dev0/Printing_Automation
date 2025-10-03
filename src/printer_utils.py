import time

def simular_impresion(numero_copia, config):
    """
    Simula el trabajo de impresión, usando la configuración del libro para calcular el tiempo.
    """
    

    PAGINAS_POR_SEGUNDO = 50 
    
    paginas = config.get('paginas', 100) 
    tiempo_espera = paginas / PAGINAS_POR_SEGUNDO
    
    print(f"   [Config]: Tam: {config['tamano']}, Papel: {config['papel']}, Pág: {paginas}")
    print(f"   [Simulación]: Procesando... (espera simulada de {tiempo_espera:.1f} segundos)")
    time.sleep(tiempo_espera)