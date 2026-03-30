
import os

print("Bienvenido al juego del laberinto, esto lo hize yooo jajajaja")
print("Hola cachimbos webones")

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
