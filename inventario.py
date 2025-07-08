import sqlite3
from sqlite3 import Error
from colorama import init, Fore, Style

# Inicializar colorama para colores en terminal
init(autoreset=True)

DB_NAME = "inventario.db"

def crear_conexion():
    """Crear conexión a la base de datos SQLite"""
    try:
        conn = sqlite3.connect(DB_NAME)
        return conn
    except Error as e:
        print(Fore.RED + f"Error al conectar a la base de datos: {e}")
        return None

def crear_tabla():
    """Crear la tabla productos si no existe"""
    conn = crear_conexion()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS productos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    descripcion TEXT,
                    cantidad INTEGER NOT NULL,
                    precio REAL NOT NULL,
                    categoria TEXT
                )
            ''')
            conn.commit()
            cursor.close()
        except Error as e:
            print(Fore.RED + f"Error al crear tabla: {e}")
        finally:
            conn.close()

def agregar_producto():
    """Agregar un nuevo producto a la base de datos"""
    print(Fore.CYAN + "\n=== Agregar Producto ===")
    nombre = input("Nombre: ").strip()
    descripcion = input("Descripción: ").strip()
    
    while True:
        cantidad_str = input("Cantidad (entero): ").strip()
        if cantidad_str.isdigit():
            cantidad = int(cantidad_str)
            break
        print(Fore.YELLOW + "Cantidad inválida. Debe ser un número entero.")
    
    while True:
        precio_str = input("Precio (ejemplo: 25.50): ").strip()
        try:
            precio = float(precio_str)
            break
        except ValueError:
            print(Fore.YELLOW + "Precio inválido. Debe ser un número real.")
    
    categoria = input("Categoría: ").strip()
    
    conn = crear_conexion()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria)
                VALUES (?, ?, ?, ?, ?)
            ''', (nombre, descripcion, cantidad, precio, categoria))
            conn.commit()
            print(Fore.GREEN + "Producto agregado correctamente.")
            cursor.close()
        except Error as e:
            print(Fore.RED + f"Error al agregar producto: {e}")
        finally:
            conn.close()

def mostrar_productos():
    """Mostrar todos los productos almacenados"""
    print(Fore.CYAN + "\n=== Lista de Productos ===")
    conn = crear_conexion()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM productos")
            filas = cursor.fetchall()
            if filas:
                for fila in filas:
                    print(f"ID: {fila[0]}, Nombre: {fila[1]}, Descripción: {fila[2]}, "
                          f"Cantidad: {fila[3]}, Precio: ${fila[4]:.2f}, Categoría: {fila[5]}")
            else:
                print(Fore.YELLOW + "No hay productos registrados.")
            cursor.close()
        except Error as e:
            print(Fore.RED + f"Error al obtener productos: {e}")
        finally:
            conn.close()

def actualizar_producto():
    """Actualizar datos de un producto por su ID"""
    print(Fore.CYAN + "\n=== Actualizar Producto ===")
    id_producto = input("Ingrese el ID del producto a actualizar: ").strip()
    if not id_producto.isdigit():
        print(Fore.YELLOW + "ID inválido. Debe ser un número entero.")
        return
    id_producto = int(id_producto)

    conn = crear_conexion()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM productos WHERE id = ?", (id_producto,))
            producto = cursor.fetchone()
            if not producto:
                print(Fore.YELLOW + f"No se encontró producto con ID {id_producto}")
                return

            print(f"Producto actual: Nombre: {producto[1]}, Descripción: {producto[2]}, "
                  f"Cantidad: {producto[3]}, Precio: ${producto[4]:.2f}, Categoría: {producto[5]}")

            # Pedir nuevos datos (si dejan vacío se mantiene el actual)
            nuevo_nombre = input("Nuevo nombre (ENTER para mantener): ").strip() or producto[1]
            nueva_descripcion = input("Nueva descripción (ENTER para mantener): ").strip() or producto[2]

            while True:
                nueva_cantidad = input("Nueva cantidad (ENTER para mantener): ").strip()
                if nueva_cantidad == "":
                    nueva_cantidad = producto[3]
                    break
                elif nueva_cantidad.isdigit():
                    nueva_cantidad = int(nueva_cantidad)
                    break
                else:
                    print(Fore.YELLOW + "Cantidad inválida, debe ser entero o dejar vacío.")

            while True:
                nuevo_precio = input("Nuevo precio (ENTER para mantener): ").strip()
                if nuevo_precio == "":
                    nuevo_precio = producto[4]
                    break
                try:
                    nuevo_precio = float(nuevo_precio)
                    break
                except ValueError:
                    print(Fore.YELLOW + "Precio inválido, debe ser un número o dejar vacío.")

            nueva_categoria = input("Nueva categoría (ENTER para mantener): ").strip() or producto[5]

            cursor.execute('''
                UPDATE productos
                SET nombre = ?, descripcion = ?, cantidad = ?, precio = ?, categoria = ?
                WHERE id = ?
            ''', (nuevo_nombre, nueva_descripcion, nueva_cantidad, nuevo_precio, nueva_categoria, id_producto))
            conn.commit()
            print(Fore.GREEN + "Producto actualizado correctamente.")
            cursor.close()
        except Error as e:
            print(Fore.RED + f"Error al actualizar producto: {e}")
        finally:
            conn.close()

def eliminar_producto():
    """Eliminar un producto por su ID"""
    print(Fore.CYAN + "\n=== Eliminar Producto ===")
    id_producto = input("Ingrese el ID del producto a eliminar: ").strip()
    if not id_producto.isdigit():
        print(Fore.YELLOW + "ID inválido. Debe ser un número entero.")
        return
    id_producto = int(id_producto)

    conn = crear_conexion()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM productos WHERE id = ?", (id_producto,))
            producto = cursor.fetchone()
            if not producto:
                print(Fore.YELLOW + f"No se encontró producto con ID {id_producto}")
                return
            confirmar = input(f"¿Está seguro que desea eliminar el producto '{producto[1]}'? (s/n): ").strip().lower()
            if confirmar == 's':
                cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
                conn.commit()
                print(Fore.GREEN + "Producto eliminado correctamente.")
            else:
                print(Fore.YELLOW + "Eliminación cancelada.")
            cursor.close()
        except Error as e:
            print(Fore.RED + f"Error al eliminar producto: {e}")
        finally:
            conn.close()

def buscar_producto():
    """Buscar producto por ID (y opcional por nombre o categoría)"""
    print(Fore.CYAN + "\n=== Buscar Producto ===")
    print("Opciones de búsqueda:")
    print("1. Buscar por ID")
    print("2. Buscar por nombre (parcial)")
    print("3. Buscar por categoría (parcial)")
    opcion = input("Seleccione opción (1-3): ").strip()
    conn = crear_conexion()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        if opcion == "1":
            id_buscar = input("Ingrese el ID del producto: ").strip()
            if not id_buscar.isdigit():
                print(Fore.YELLOW + "ID inválido.")
                return
            cursor.execute("SELECT * FROM productos WHERE id = ?", (int(id_buscar),))
            producto = cursor.fetchone()
            if producto:
                print(f"ID: {producto[0]}, Nombre: {producto[1]}, Descripción: {producto[2]}, "
                      f"Cantidad: {producto[3]}, Precio: ${producto[4]:.2f}, Categoría: {producto[5]}")
            else:
                print(Fore.YELLOW + "No se encontró producto con ese ID.")
        elif opcion == "2":
            nombre_buscar = input("Ingrese nombre o parte del nombre: ").strip()
            cursor.execute("SELECT * FROM productos WHERE nombre LIKE ?", (f"%{nombre_buscar}%",))
            resultados = cursor.fetchall()
            if resultados:
                for p in resultados:
                    print(f"ID: {p[0]}, Nombre: {p[1]}, Descripción: {p[2]}, "
                          f"Cantidad: {p[3]}, Precio: ${p[4]:.2f}, Categoría: {p[5]}")
            else:
                print(Fore.YELLOW + "No se encontraron productos con ese nombre.")
        elif opcion == "3":
            categoria_buscar = input("Ingrese categoría o parte de la categoría: ").strip()
            cursor.execute("SELECT * FROM productos WHERE categoria LIKE ?", (f"%{categoria_buscar}%",))
            resultados = cursor.fetchall()
            if resultados:
                for p in resultados:
                    print(f"ID: {p[0]}, Nombre: {p[1]}, Descripción: {p[2]}, "
                          f"Cantidad: {p[3]}, Precio: ${p[4]:.2f}, Categoría: {p[5]}")
            else:
                print(Fore.YELLOW + "No se encontraron productos en esa categoría.")
        else:
            print(Fore.YELLOW + "Opción inválida.")
        cursor.close()
    except Error as e:
        print(Fore.RED + f"Error en la búsqueda: {e}")
    finally:
        conn.close()

def reporte_cantidad():
    """Mostrar productos con cantidad igual o menor a un límite dado"""
    print(Fore.CYAN + "\n=== Reporte por Cantidad ===")
    limite_str = input("Mostrar productos con cantidad igual o menor a: ").strip()
    if not limite_str.isdigit():
        print(Fore.YELLOW + "Debe ingresar un número entero válido.")
        return
    limite = int(limite_str)

    conn = crear_conexion()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM productos WHERE cantidad <= ?", (limite,))
            productos = cursor.fetchall()
            if productos:
                print(Fore.GREEN + f"Productos con cantidad menor o igual a {limite}:")
                for p in productos:
                    print(f"ID: {p[0]}, Nombre: {p[1]}, Cantidad: {p[3]}, Precio: ${p[4]:.2f}")
            else:
                print(Fore.YELLOW + "No hay productos con cantidad igual o menor al límite.")
            cursor.close()
        except Error as e:
            print(Fore.RED + f"Error al generar reporte: {e}")
        finally:
            conn.close()

def mostrar_menu():
    """Mostrar el menú principal"""
    print(Fore.MAGENTA + "\n=== MENÚ PRINCIPAL ===")
    print("1. Registrar nuevo producto")
    print("2. Ver productos")
    print("3. Actualizar producto por ID")
    print("4. Eliminar producto por ID")
    print("5. Buscar producto")
    print("6. Reporte por cantidad")
    print("7. Salir")

def main():
    crear_tabla()  # Asegurarse que la tabla exista
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción (1-7): ").strip()
        if opcion == "1":
            agregar_producto()
        elif opcion == "2":
            mostrar_productos()
        elif opcion == "3":
            actualizar_producto()
        elif opcion == "4":
            eliminar_producto()
        elif opcion == "5":
            buscar_producto()
        elif opcion == "6":
            reporte_cantidad()
        elif opcion == "7":
            print(Fore.BLUE + "Saliendo del programa. ¡Hasta luego!")
            break
        else:
            print(Fore.YELLOW + "Opción inválida. Intente nuevamente.")

if __name__ == "__main__":
    main()
