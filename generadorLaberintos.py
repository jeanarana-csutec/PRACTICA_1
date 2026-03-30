import numpy as np
import random as rnd


direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)] # Direcciones: arriba, abajo, izquierda, derecha

def crear_laberinto(maze_width: int, maze_height: int, startingY = 1):

    maze = np.ones((maze_height * 2 + 1, maze_width * 2 + 1), dtype=int)  # Representamos las paredes como una matriz de tamaño (2h+1)x(2w+1)

    def escarbar_camino(x, y):

        maze[y][x] = 0 # Marca la celda como vacía (camino)

        dirs = direcciones[:]
        rnd.shuffle(dirs) ## chocolatea las direcciones

        for dy, dx in dirs:
            nx, ny = x + dx * 2, y + dy * 2
            ##calculo de nx y nx, los cuales suman los valores de las de direcciones
            ##para determinar si la celda siguiente es visitable
            if 1 <= nx < maze.shape[1] - 1 and 1 <= ny < maze.shape[0] - 1:
                if maze[ny][nx] == 1: # Quita la pared entre la celda actual y la vecina
                    maze[y + dy][x + dx] = 0
                    escarbar_camino(nx, ny)
    #### generar entrada
    maze[startingY][0] = 0
    escarbar_camino(1, startingY) # Empieza a escarbar el laberinto celda impar dentro del laberinto

    return list(maze)

def resolver_laberinto(maze, startingY=1):
    filas, columnas = len(maze), len(maze[0])
    soluciones = []

    def trazar_camino(x, y, dir_anterior=None, camino_actual=None):
        if camino_actual is None:
            camino_actual = [(y, x)] ##en el caso no haya direccion anterior, la iguala al x y y inicial

        dirs = direcciones[:] #duplica tus direcciones

        if dir_anterior: # evita volver hacia la dirección opuesta, al eliminarla de la lista
            opuesta = (-dir_anterior[0], -dir_anterior[1])
            dirs = [d for d in dirs if d != opuesta]

        posibles_dirs = []

        for dy, dx in dirs:
            ny, nx = y + dy, x + dx
            if 0 <= ny < filas and 0 <= nx < columnas and maze[ny][nx] == 0:
                posibles_dirs.append((dy, dx)) #revisa que posibles direcciones hay

        if len(posibles_dirs) == 0:
            soluciones.append(camino_actual[:]) #si no hay posibles direcciones, entonces termina la busqueda y le añades el camino recorrido a soluciones
            return

        for dy, dx in posibles_dirs:
            ny, nx = y + dy, x + dx
            nuevo_camino = camino_actual[:] #se crea un nuevo camino en base al anterior

            # avanza mientras el camino esté libre
            while 0 <= ny < filas  and 0 <= nx < columnas and maze[ny][nx] == 0:
                nuevo_camino.append((ny, nx))
                ny += dy
                nx += dx

            # retrocede una posición cuando choca con una pared, ya que la condicional realiza la suma antes de que se llegue al deseado
            ny -= dy
            nx -= dx

            if (ny, nx) != (y, x):  # si tus nuevos x no son los mismos que los anteriores, lanzas una nueva busqueda
                trazar_camino(nx, ny, (dy, dx), nuevo_camino)

    trazar_camino(0, startingY)
    recorridoFinal = [z for z in soluciones if (1 in z[::-1][0] or (len(maze) - 2) in z[::-1][0]) and z[::-1][0] != (1, 0)][::-1][0]
    puntosFinales = [z[::-1][0] for z in soluciones if (1 in z[::-1][0] or (len(maze) - 2) in z[::-1][0]) and z[::-1][0] != (1, 0)][::-1]
    ### sacar salida

    for x in direcciones[:]:
        if len(puntosFinales) > 0:
            if  puntosFinales[0][0] + x[0] in (0, len(maze)-1) or puntosFinales[0][1] + x[1] in (0, len(maze[0])-1):
                maze[puntosFinales[0][0] + x[0]][puntosFinales[0][1] + x[1]] = 2
                break

    return (maze, recorridoFinal)

def mostrar_solucion(maze, trail):
    for x in trail:
        if maze[x[0]][x[1]] in (0, 3):
            maze[x[0]][x[1]] = 5
    return maze

def convertir_laberinto_cadena(maze, claves = [" ", "#", "S", "P", "E", "c","o"], desconocido = "?"): return "\n".join(["".join([claves[y] if y in range(len(claves)) else desconocido for y in x ]) for x in maze])