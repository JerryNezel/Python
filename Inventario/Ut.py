import sqlite3
from colorama import Fore, Style

def agregar(cursor, conexion):
    while True:
        producto = input("\nIngrese el nombre del producto: ").strip().capitalize()
        if not producto:
            print(f"{Fore.RED}Error: El nombre no puede estar vacío")
            continue
        descripcion = input("Descripción (opcional): ").strip()
        categoria = input("Categoría: ").strip().capitalize()
        try:
            cantidad = int(input("Cantidad inicial: "))
            if cantidad < 0:
                print(f"{Fore.RED}Error: La cantidad no puede ser negativa")
                continue
        except ValueError:
            print(f"{Fore.RED}Error: Ingrese un número entero válido")
            continue
        try:
            precio = float(input("Precio unitario: $"))
            if precio <= 0:
                print(f"{Fore.RED}Error: El precio debe ser positivo")
                continue
        except ValueError:
            print(f"{Fore.RED}Error: Ingrese un valor numérico válido")
            continue
        try:
            cursor.execute('''INSERT INTO productos 
                          (nombre, descripcion, cantidad, precio, categoria) 
                          VALUES (?, ?, ?, ?, ?)''', 
                          (producto, descripcion, cantidad, precio, categoria))
            conexion.commit()
            print(f"{Fore.GREEN}\n¡Producto agregado exitosamente!")
            break
        except sqlite3.Error as e:
            print(f"{Fore.RED}Error al agregar producto: {e}")

def mostrar(cursor):
    cursor.execute('''SELECT * FROM productos ORDER BY nombre''')
    productos = cursor.fetchall()
    if not productos:
        print(f"{Fore.YELLOW}\nNo hay productos registrados")
        return
    print(f"\n{Fore.CYAN}=== LISTA DE PRODUCTOS ===")
    print(f"{'ID':<5}{'Nombre':<20}{'Cant.':<8}{'Precio':<10}{'Categoría':<15}")
    print("-" * 60)
    for prod in productos:
        print(f"{prod[0]:<5}{prod[1]:<20}{prod[3]:<8}${prod[4]:<9.2f}{prod[5]:<15}")

def buscar(cursor):
    cursor.execute('''SELECT COUNT(*) FROM productos''')
    if cursor.fetchone()[0] == 0:
        print(f"{Fore.YELLOW}\nNo hay productos para buscar.")
        return
    termino = input("\nIngrese nombre o categoría a buscar: ").strip().capitalize()
    cursor.execute('''
        SELECT * FROM productos 
        WHERE nombre LIKE ? OR categoria LIKE ?
        ORDER BY nombre
    ''', (f"%{termino}%", f"%{termino}%"))
    resultados = cursor.fetchall()
    if not resultados:
        print(f"\n{Fore.RED}No se encontraron coincidencias para '{termino}'")
    else:
        print(f"\n{Fore.CYAN}=== RESULTADOS ===")
        print(f"{'ID':<5}{'Nombre':<20}{'Cant.':<8}{'Precio':<10}{'Categoría':<15}")
        print("-" * 60)
        for prod in resultados:
            print(f"{prod[0]:<5}{prod[1]:<20}{prod[3]:<8}${prod[4]:<9.2f}{prod[5]:<15}")

def eliminar(cursor, conexion):
    cursor.execute('''SELECT id, nombre FROM productos ORDER BY id''')
    productos = cursor.fetchall()
    if not productos:
        print(f"{Fore.YELLOW}\nNo hay productos para eliminar.")
        return
    print(f"\n{Fore.CYAN}=== PRODUCTOS DISPONIBLES ===")
    for prod in productos:
        print(f"{Fore.WHITE}ID: {prod[0]} - {prod[1]}")
    try:
        id_eliminar = int(input("\nIngrese el ID del producto a eliminar: "))
        cursor.execute('''SELECT nombre FROM productos WHERE id = ?''', (id_eliminar,))
        resultado = cursor.fetchone()
        if resultado:
            confirmar = input(f"{Fore.RED}\n¿Seguro que desea eliminar '{resultado[0]}'? (S/N): ").upper()
            if confirmar == 'S':
                cursor.execute('''DELETE FROM productos WHERE id = ?''', (id_eliminar,))
                conexion.commit()
                print(f"{Fore.GREEN}\n¡Producto eliminado exitosamente!")
            else:
                print(f"{Fore.YELLOW}\nOperación cancelada")
        else:
            print(f"{Fore.RED}\nError: No existe producto con ese ID.")
    except ValueError:
        print(f"{Fore.RED}\nError: Debe ingresar un número válido.")

def reporte(cursor):
    try:
        limite = int(input("\nIngrese el límite de stock a reportar: "))
        cursor.execute('''
            SELECT id, nombre, cantidad, categoria 
            FROM productos 
            WHERE cantidad <= ? 
            ORDER BY cantidad ASC, categoria
        ''', (limite,))
        productos_bajos = cursor.fetchall()
        if not productos_bajos:
            print(f"{Fore.YELLOW}No hay productos con stock ≤ {limite}")
            return
        print(f"\n{Fore.YELLOW}=== PRODUCTOS CON STOCK BAJO (≤ {limite}) ===")
        print(f"{Fore.MAGENTA}ID  {'Nombre':<20} {'Categoría':<15} {'Stock':<10}")
        print("-" * 50)
        for prod in productos_bajos:
            color = Fore.RED if prod[2] <= (limite * 0.3) else Fore.YELLOW
            print(f"{prod[0]:<4} {prod[1]:<20} {prod[3]:<15} {color}{prod[2]:<10}{Style.RESET_ALL}")
    except ValueError:
        print(f"{Fore.RED}Error: Ingrese un número válido")
    except sqlite3.Error as e:
        print(f"{Fore.RED}Error de BD: {e}")

def actualizar(cursor, conexion):
    try:
        cursor.execute("SELECT id, nombre, cantidad FROM productos ORDER BY id")
        productos = cursor.fetchall()
        print(f"\n{Fore.YELLOW}=== LISTA DE PRODUCTOS ===")
        print(f"{'ID':<5}{'Nombre':<25}{'Stock':<10}")
        print("-" * 40)
        for prod in productos:
            print(f"{prod[0]:<5}{prod[1]:<25}{prod[2]:<10}")
        id_producto = int(input("\nIngrese el ID del producto a actualizar: "))
        cursor.execute("SELECT * FROM productos WHERE id = ?", (id_producto,))
        producto = cursor.fetchone()
        if not producto:
            print(f"{Fore.RED}Error! ID no encontrado")
            return
        print(f"\n{Fore.CYAN}Editando: {producto[1]}")
        print(f"Deje en blanco para mantener el valor actual\n")
        nuevo_nombre = input(f"Nuevo nombre [{producto[1]}]: ").strip().capitalize() or producto[1]
        nueva_desc = input(f"Nueva descripción [{producto[2]}]: ").strip() or producto[2]
        nueva_cant = input(f"Nueva cantidad [{producto[3]}]: ").strip() or producto[3]
        nuevo_precio = input(f"Nuevo precio [${producto[4]}]: ").strip('$') or producto[4]
        nueva_cat = input(f"Nueva categoría [{producto[5]}]: ").strip().capitalize() or producto[5]
        try:
            nueva_cant = int(nueva_cant)
            nuevo_precio = float(nuevo_precio)
        except ValueError:
            print(f"{Fore.RED}Error: Cantidad debe ser entero y precio numérico")
            return
        cursor.execute('''
            UPDATE productos 
            SET nombre = ?, descripcion = ?, cantidad = ?, precio = ?, categoria = ?
            WHERE id = ?
        ''', (nuevo_nombre, nueva_desc, nueva_cant, nuevo_precio, nueva_cat, id_producto))
        conexion.commit()
        print(f"{Fore.GREEN}Producto actualizado correctamente!")
    except ValueError:
        print(f"{Fore.RED}Error: ID debe ser un número")
    except sqlite3.Error as e:
        print(f"{Fore.RED}Error de BD: {e}")