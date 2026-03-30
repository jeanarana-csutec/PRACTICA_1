
import os
<<<<<<< HEAD
#Hola
print("Bienvenido al juego del laberinto")
=======


print("Bienvenido al juego del laberinto, espero que les guste")
#Esto se empezo de esta manera XDE

>>>>>>> 6c5ac5f993230c3316719487de2ad858381174ad

while True:
    opcion = input("Escribe 'jugar' para empezar o 'salir' para terminar: ").strip().lower()
    if opcion == "jugar":
        os.system("juego_laberinto.py")
        break
    elif opcion == "salir":
        print("Gracias por jugar. ¡Hasta pronto!")
        break
    else:
        print("Opción no válida. Por favor, escribe 'jugar' o 'salir'.")
