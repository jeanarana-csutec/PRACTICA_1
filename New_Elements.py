import random
import os
import time

def colocar_coleccionables(matriz, cantidad=None):
    caminos = [(i, j) for i in range(len(matriz))
               for j in range(len(matriz[0])) if matriz[i][j] == 0] #Esto crea una lista de todas las celdas (i, j) de la matriz que son caminos transitables

    if cantidad is None:
        min_c = max(1, len(caminos) // 10)  #Calcular el 10% de los caminos disponibles
        max_c = max(1, len(caminos) // 3)   #Calcular el 33% (tecera parte)) de los caminos transitables.
        cantidad = random.randint(min_c, max_c)

    posiciones = random.sample(caminos, k=min(cantidad, len(caminos))) #seleciona k elementos de una lista únicos y al azar, el min para evitar que use todo lo transitable.

    for y, x in posiciones:
        matriz[y][x] = 6
    return matriz

def mostrar_resumen(nombre, puntaje_final, movements, coleccionables,dimensiones, tiempo_resuelto):
    print(f"\nResumen de la partida de {nombre}:")
    print(f" Coleccionables recogidos: {coleccionables}")
    print(f" Movimientos realizados: {movements}")
    print(f" Puntaje final: {puntaje_final}")
    actualizar_ranking(nombre, puntaje_final,dimensiones,coleccionables, tiempo_resuelto)

def actualizar_ranking(nombre, puntaje, dimensiones, monedas, tiempo_resuelto):
    ranking = {}
    archivo = "ranking.txt"

    # Leer archivo si existe
    if os.path.exists(archivo):
        with open(archivo, "r", encoding="utf-8") as f:
            for linea in f:
                try:
                    nombre_arch, puntos_arch, dimensiones_arch, monedas_arch, tiempo_arch = linea.strip().split("|")
                    ranking[nombre_arch] = (
                        int(puntos_arch), dimensiones_arch, int(monedas_arch), float(tiempo_arch)
                    )
                except ValueError:
                    continue

    # Actualiza si es nuevo jugador(yo) superó su puntaje anterior
    if (nombre not in ranking) or (puntaje > ranking [nombre][0]):
        ranking[nombre] = (puntaje, dimensiones, monedas, tiempo_resuelto)

    # Ordenar por puntaje de mayor a menor:
    ranking_ordenado = sorted(ranking.items(), key=lambda x: x[1][0], reverse=True)

    # Escribir el ranking actualizado:
    with open(archivo, "w", encoding="utf-8") as f:
        for jugador, (pts, dims, mons, tiempo) in ranking_ordenado:
            f.write(f"{jugador}|{pts}|{dims}|{mons}|{tiempo:.2f}\n")

def mostrar_ranking():
    archivo = "ranking.txt"

    if not os.path.exists(archivo):
        print("No hay datos de ranking disponibles aún.")
        return

    print(f"{'Jugador':<15}{'Puntaje':<10}{'Dimensiones':<15}{'Monedas':<10}{'Tiempo (s)':<12}")
    print("-" * 62)

    with open(archivo, "r", encoding="utf-8") as f:
        for linea in f:
            try:
                nombre, puntos, dimensiones, monedas, tiempo = linea.strip().split("|")
                print(f"{nombre:<15}{puntos:<10}{dimensiones:<15}{monedas:<10}{tiempo:<12}")
            except ValueError:
                continue

def finalizar_partida(score, movements, nombre, dimensiones, inicio_t):
    tiempo_resuelto = round(time.time() - inicio_t, 2)
    coleccionables_recogidos = score // 10
    TOTAL_SCORE = score - movements
    actualizar_ranking(nombre, TOTAL_SCORE, dimensiones, coleccionables_recogidos, tiempo_resuelto)
    mostrar_resumen(nombre, TOTAL_SCORE, movements, coleccionables_recogidos, dimensiones, tiempo_resuelto)
    print("\nTabla de Ranking:\n")
    mostrar_ranking()
    salir = input("¿Deseas volver al menú principal? (m para menú, cualquier otra tecla para continuar): ")
    if salir.lower() == "m":
        os.system("main.py")
        exit()