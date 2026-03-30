import generadorLaberintos as genLab
import os
import New_Elements as extra
import time

#establecemos parametros:
yInicial = 1
jugadorPosY, jugadorPosX = yInicial, 0
py, px = yInicial, 0
inpExit, inpSolv = "f", "r"
exited = False
afirmaciones = {"si": True, "no": False}


### funciones auxiliares
def refrescar_laberinto(maze):
    clear()
    maze[py][px] = 0
    maze[jugadorPosY][jugadorPosX] = 3
    return genLab.convertir_laberinto_cadena(maze)
def clear(): os.system('cls' if os.name == 'nt' else 'clear')

### mapeo de teclas
claves = ["w", "s", "a", "d"]
movimiento = dict(list(zip(claves, genLab.direcciones)))

###string sacado de un generador de texto grande
print("""                                                    
 #                                                              #         ###    #####  
 #         ##   #####  ###### #####  # #    # #####  ####      ##        #   #  #     # 
 #        #  #  #    # #      #    # # ##   #   #   #    #    # #       #     #       # 
 #       #    # #####  #####  #    # # # #  #   #   #    #      #       #     #  #####  
 #       ###### #    # #      #####  # #  # #   #   #    #      #   ### #     #       # 
 #       #    # #    # #      #   #  # #   ##   #   #    #      #   ###  #   #  #     # 
 ####### #    # #####  ###### #    # # #    #   #    ####     ##### ###   ###    #####  

""")
nombre = str(input("- Ingrese su nombre para iniciar:"))

clear()

print(f"\n¡Un gusto jugar con usted, {nombre}! \nPor favor, ingrese las dimensiones del laberinto\n")

score = 0
movements = 0

while not exited:
    ### ingresar parametros pal laberinto
    while True:
        try:
            altoLaberinto = int(input("Altura del laberinto (N° de filas): \n"))
            anchoLaberinto = int(input("Ancho del laberinto (N° de columnas): \n"))
        except ValueError:
            print("Parece que no ingreso un valor valido, intentelo de nuevo: ")
        else:
            if altoLaberinto > 1 and anchoLaberinto > 1:
                clear()
                break
            else:
                print(
                    "Parece que ingreso dimensiones insuficientes para formar un laberinto real. Intente con valores mas grandes.")

    ###generar nuevos laberintos al empezar o intentar de nuevo
    labSr = genLab.crear_laberinto(altoLaberinto, anchoLaberinto, yInicial)
    lab = genLab.resolver_laberinto(labSr)
    labMat = lab[0]
    labSolucion = lab[1]
    labMat = extra.colocar_coleccionables(labMat)
    jugadorPosY, jugadorPosX = yInicial, 0
    solved = False
    Time = (altoLaberinto*anchoLaberinto)*2
    inicio_t = time.time()
    print(f"\nTendrás {int(Time)} segundos para resolver este laberinto.\n")
    while not solved:
        if time.time() - inicio_t > Time:
            print("\n¡Tiempo agotado! Has perdido la partida.")
            dimensiones = f"{altoLaberinto}x{anchoLaberinto}"
            extra.finalizar_partida(score, movements, nombre, dimensiones, inicio_t)
            solved = True
            break
        if exited:
            break

        if labMat[jugadorPosY][jugadorPosX] == 2:  ##condicion para ganar
            dimensiones = f"{altoLaberinto}x{anchoLaberinto}"
            extra.finalizar_partida(score, movements, nombre, dimensiones, inicio_t)
            solved = True
            break

        print(refrescar_laberinto(labMat))

        print(f"Movimientos: w para ir arriba,"
              f" s para ir abajo,"
              f" a para ir a la izquierda,"
              f" d para ir a la derecha,"
              f" {inpExit} para salir, {inpSolv} para mostrar la solución"
              f" ,v para ver el ranking)")

        while True:  ### revisar que el input sea válido
            jugInput = input(f"Por favor {nombre}, ingrese su siguiente movimiento: ").strip()

            if not jugInput:
                print("No escribiste ningún movimiento. Inténtalo de nuevo.")
                continue

            if jugInput.lower() in movimiento:

                ny, nx = movimiento[jugInput.lower()]

                if (jugadorPosY + ny != yInicial or jugadorPosX + nx != 0) and labMat[jugadorPosY + ny][
                    jugadorPosX + nx] != 1:
                    py, px = jugadorPosY, jugadorPosX
                    jugadorPosY += ny
                    jugadorPosX += nx
                    movements += 1

                    if labMat[jugadorPosY][jugadorPosX] == 6:
                        score += 10
                        labMat[jugadorPosY][jugadorPosX] = 0
                    break
                else:
                    print("¡Haz chocado con una pared!. Intenta moviendote en otra direccion...")

            elif jugInput.lower() == inpExit:
                exited = True
                dimensiones = f"{altoLaberinto}x{anchoLaberinto}"
                extra.finalizar_partida(score, movements, nombre, dimensiones, inicio_t)
                solved = True
                break

            elif jugInput.lower() == inpSolv:
                clear()
                genLab.mostrar_solucion(labMat, labSolucion)
                print(genLab.convertir_laberinto_cadena(labMat))
                labMat[yInicial][0] = 5
                solved = True
                break
            elif jugInput.lower() == "v":
                print("\nTabla de Ranking:\n")
                extra.mostrar_ranking()
                input("\nPresiona Enter para volver al juego...")
                print(refrescar_laberinto(labMat))

            else:
                print("¡Uy! Parece que ese movimiento no existe en este juego. Intente de nuevo...")
    clear()

    if solved:
        continuar = str(input("¿Desea generar otro laberinto? Responda si o no: "))
        while continuar not in afirmaciones:
            continuar = str(input("Ese no es un si o un no. Intente de nuevo: "))
        if not afirmaciones[continuar]:
            clear()
            print(f"¡Hasta luego! Gracias por jugar, {nombre}")
            os.system("main.py")
            exit()