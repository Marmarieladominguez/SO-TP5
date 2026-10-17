"""
UNJu - Facultad de Ingeniería
Teoría de Sistemas Operativos (TSO) - Ciclo Lectivo 2026
Cátedra: Ing. María Fernanda Vázquez - JTP: Ing. Fabio D. Argañaraz

Ejercicio Práctico N° 2: El Problema del Oso y las Abejas
Bibliografía de Referencia:
- Silberschatz: Cap. 6.6 (Problemas clásicos de sincronización)
- Stallings: Cap. 5.4 (Sincronización con semáforos)
"""

import sys
import threading
import time
import random

# Configuración UTF-8 para consola Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

M = 10                  # Capacidad del tarro de miel
NUM_ABEJAS = 5          # Número de abejas obreras
tarro_miel = 0          # Variable compartida
simulacion_activa = True

# =====================================================================
# MECANISMOS DE SINCRONIZACIÓN
# =====================================================================
mutex = threading.Lock()                # Exclusión mutua para modificar tarro_miel
sem_oso = threading.Semaphore(0)        # Duerme al oso hasta que el tarro se llena (M porciones)
sem_tarro_disponible = threading.Semaphore(1) # Controla que las abejas esperen si el tarro está lleno/siendo vaciado

def abeja(id_abeja):
    global tarro_miel, simulacion_activa
    while simulacion_activa:
        time.sleep(random.uniform(0.05, 0.2)) # Simula el tiempo de recolección de miel
        
        # 1. Esperar a que el tarro esté disponible (si el oso está comiendo o está lleno)
        sem_tarro_disponible.acquire()
        
        # 2. Entrar en sección crítica para modificar el tarro de forma segura
        mutex.acquire()
        try:
            if not simulacion_activa:
                break
            
            tarro_miel += 1
            print(f"🐝 [Abeja {id_abeja}] Deposita 1 porción. Miel en tarro: {tarro_miel}/{M}")
            
            # 3. Si el tarro se llena, se despierta al oso
            if tarro_miel == M:
                print(f"🍯 [Abeja {id_abeja}] ¡Tarro lleno! Despertando al oso...")
                sem_oso.release() # Despierta al oso
            else:
                # Si aún hay espacio, liberamos el tarro para que otra abeja pueda seguir depositando
                sem_tarro_disponible.release()
                
        finally:
            mutex.release()

def oso(max_tarros=2):
    global tarro_miel, simulacion_activa
    tarros_comidos = 0
    while tarros_comidos < max_tarros and simulacion_activa:
        print("🐻 [Oso] Durmiendo plácidamente en el bosque...")
        
        # 1. Esperar pasivamente hasta que una abeja señale que el tarro está lleno
        sem_oso.acquire()
        
        if not simulacion_activa:
            break
            
        # Entramos en exclusión mutua para vaciar el tarro
        mutex.acquire()
        try:
            print(f"🐻 [Oso] ¡Desperté! Comiendo la miel del tarro (Contenía {tarro_miel} porciones)...")
            time.sleep(random.uniform(0.1, 0.3)) # Simula el tiempo que tarda el oso comiendo
            
            # 2. Vaciar el tarro
            tarro_miel = 0
            tarros_comidos += 1
            print(f"🐻 [Oso] Terminé de comer. Tarros comidos hasta ahora: {tarros_comidos}/{max_tarros}")
            
        finally:
            mutex.release()
            
        # 3. Avisar a las abejas que el tarro está vacío y disponible para llenarse de nuevo
        sem_tarro_disponible.release()
        
    simulacion_activa = False
    # Liberar el semáforo del oso por si acaso queda algún hilo bloqueado al cerrar
    sem_oso.release()

if __name__ == "__main__":
    print("=" * 60)
    print(" Iniciando Simulación: El Oso y las Abejas (UNJu FI)")
    print("=" * 60)
    
    # Crear hilo para el oso
    hilo_oso = threading.Thread(target=oso, args=(2,))
    
    # Crear hilos para las N abejas
    hilos_abejas = [threading.Thread(target=abeja, args=(i+1,)) for i in range(NUM_ABEJAS)]
    
    # Iniciar los hilos
    hilo_oso.start()
    for h in hilos_abejas:
        h.start()
        
    # Esperar a que el oso termine de comer los tarros establecidos
    hilo_oso.join()
    
    print("=" * 60)
    print(" Simulación finalizada. El oso se durmió satisfecho.")
    print("=" * 60)