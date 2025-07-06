from Ut import *
import sqlite3
from colorama import init, Fore, Style
init(autoreset=True)

conexion = sqlite3.connect("inventario.db")
cursor = conexion.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    cantidad INTEGER NOT NULL,
    precio REAL NOT NULL,
    categoria TEXT)''')
conexion.commit()

def mostrar_menu():
    print(f"\n{Fore.BLUE}==== Gestión de Inventario ===={Style.RESET_ALL}")
    print(f"{Fore.WHITE}1. {Fore.CYAN}Agregar Producto")
    print(f"{Fore.WHITE}2. {Fore.CYAN}Mostrar Productos")
    print(f"{Fore.WHITE}3. {Fore.CYAN}Buscar Producto")
    print(f"{Fore.WHITE}4. {Fore.YELLOW}Actualizar Producto")
    print(f"{Fore.WHITE}5. {Fore.RED}Eliminar Producto")
    print(f"{Fore.WHITE}6. {Fore.MAGENTA}Control de Stock")
    print(f"{Fore.WHITE}7. {Fore.LIGHTRED_EX}Salir{Style.RESET_ALL}")

while True:
    mostrar_menu()
    opcion = input(f"\n{Fore.YELLOW}Seleccione una opción: {Style.RESET_ALL}").strip()
    
    if opcion == "1":
        agregar(cursor, conexion)
    elif opcion == "2":
        mostrar(cursor)
    elif opcion == "3":
        buscar(cursor)
    elif opcion == "4":
        actualizar(cursor, conexion)
    elif opcion == "5":
        eliminar(cursor, conexion)
    elif opcion == "6":
        reporte(cursor)
    elif opcion == "7":
        conexion.close()
        print(f"{Fore.GREEN}\nHasta la próxima!{Style.RESET_ALL}")
        break
    else:
        print(f"{Fore.RED}\nOpción no válida{Style.RESET_ALL}")