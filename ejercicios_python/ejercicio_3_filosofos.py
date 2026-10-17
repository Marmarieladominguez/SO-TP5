"""
UNJu - Facultad de Ingeniería
Teoría de Sistemas Operativos (TSO) - Ciclo Lectivo 2026
Cátedra: Ing. María Fernanda Vázquez - JTP: Ing. Fabio D. Argañaraz

Ejercicio Práctico N° 3: La Cena de los Filósofos (Prevención de Deadlock)
Bibliografía de Referencia:
- Silberschatz: Cap. 6.6 (Problemas clásicos de sincronización)
- Stallings: Cap. 5.6 (Problema de los filósofos comensales)
"""

import threading
import time
import random

NUM_FILOSOFOS = 5

# Cada tenedor está representado por un Lock (exclusión mutua)
tenedores = [threading.Lock() for _ in range(NUM_FILOSOFOS)]

# Variable para contar cuántas veces comió cada filósofo
comidas = [0] * NUM_FILOSOFOS

# Lock para evitar que los mensajes se mezclen en la consola
lock_print = threading.Lock()


def log(msg):
    with lock_print:
        print(msg)


def pensar(id):
    log(f"🤔 Filósofo {id} está pensando...")
    time.sleep(random.uniform(0.1, 0.3))


def comer(id):
    log(f"🍝 Filósofo {id} está comiendo espagueti...")

    comidas[id] += 1

    time.sleep(random.uniform(0.1, 0.3))

    log(f"✨ Filósofo {id} terminó de comer "
        f"(total comidas: {comidas[id]}).")


def filosofo(id, rondas=3):
    """
    Ciclo de vida de cada filósofo:
    pensar -> tomar tenedores -> comer -> soltar tenedores.

    Prevención de deadlock mediante una estrategia asimétrica:
    - Filósofos pares: toman primero el tenedor izquierdo.
    - Filósofos impares: toman primero el tenedor derecho.
    """

    for _ in range(rondas):
        pensar(id)

        # Identificadores de los tenedores adyacentes
        tenedor_izq = id
        tenedor_der = (id + 1) % NUM_FILOSOFOS

        # Estrategia asimétrica para prevenir el deadlock
        if id % 2 == 0:
            primero = tenedor_izq
            segundo = tenedor_der
        else:
            primero = tenedor_der
            segundo = tenedor_izq

        # Tomar ambos tenedores en el orden establecido
        with tenedores[primero]:
            log(f"🍴 Filósofo {id} tomó el tenedor {primero}.")

            with tenedores[segundo]:
                log(f"🍴 Filósofo {id} tomó el tenedor {segundo}.")

                # Comer mientras mantiene ambos tenedores
                comer(id)

            # Al salir del segundo with, se libera el segundo tenedor

        # Al salir del primer with, se libera el primer tenedor
        log(f"✅ Filósofo {id} liberó ambos tenedores.")


if __name__ == "__main__":
    print("=" * 60)
    print(" Iniciando Simulación de los Filósofos Comensales (UNJu FI)")
    print("=" * 60)

    hilos = []

    # Crear e iniciar los hilos de los cinco filósofos
    for i in range(NUM_FILOSOFOS):
        t = threading.Thread(
            target=filosofo,
            args=(i, 3),
            name=f"Filosofo-{i}"
        )
        hilos.append(t)
        t.start()

    # Esperar a que todos los filósofos terminen
    for t in hilos:
        t.join()

    print("=" * 60)
    print(" Resumen de Comidas:")

    for i, c in enumerate(comidas):
        print(f" - Filósofo {i}: {c} veces comió.")

    print(" ¡Simulación completada sin Interbloqueo (Deadlock)!")
    print("=" * 60)