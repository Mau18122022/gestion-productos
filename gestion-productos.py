# Lista para almacenar los productos
productos = []

def mostrar_menu():
    print("\n=== MENÚ DE OPCIONES ===")
    print("1. Agregar producto")
    print("2. Ver productos")
    print("3. Buscar producto por nombre")
    print("4. Eliminar producto por número")
    print("5. Salir")

def agregar_producto():
    while True:
        nombre = input("Ingrese el nombre del producto: ").strip()
        if nombre:
            break
        print("El nombre no puede estar vacío.")

    while True:
        categoria = input("Ingrese la categoría del producto: ").strip()
        if categoria:
            break
        print("La categoría no puede estar vacía.")

    while True:
        precio_str = input("Ingrese el precio (entero, sin centavos): ").strip()
        if precio_str.isdigit():
            precio = int(precio_str)
            break
        print("Debe ingresar un número entero válido para el precio.")

    productos.append([nombre, categoria, precio])
    print("Producto agregado correctamente.")

def ver_productos():
    if not productos:
        print("No hay productos registrados.")
        return
    print("\n=== LISTA DE PRODUCTOS ===")
    for i, prod in enumerate(productos, start=1):
        print(f"{i}. Nombre: {prod[0]}, Categoría: {prod[1]}, Precio: ${prod[2]}")

def buscar_producto():
    termino = input("Ingrese el nombre del producto a buscar: ").strip().lower()
    encontrados = []
    for i, prod in enumerate(productos, start=1):
        if termino in prod[0].lower():
            encontrados.append((i, prod))
    if encontrados:
        print("\n=== RESULTADOS DE LA BÚSQUEDA ===")
        for idx, prod in encontrados:
            print(f"{idx}. Nombre: {prod[0]}, Categoría: {prod[1]}, Precio: ${prod[2]}")
    else:
        print("No se encontraron productos con ese nombre.")

def eliminar_producto():
    if not productos:
        print("No hay productos para eliminar.")
        return
    ver_productos()
    while True:
        try:
            indice = int(input("Ingrese el número del producto a eliminar: "))
            if 1 <= indice <= len(productos):
                eliminado = productos.pop(indice - 1)
                print(f"Producto '{eliminado[0]}' eliminado correctamente.")
                break
            else:
                print("Número fuera de rango.")
        except ValueError:
            print("Debe ingresar un número válido.")

def main():
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción (1-5): ").strip()
        if opcion == "1":
            agregar_producto()
        elif opcion == "2":
            ver_productos()
        elif opcion == "3":
            buscar_producto()
        elif opcion == "4":
            eliminar_producto()
        elif opcion == "5":
            print("Saliendo del programa. ¡Hasta luego!")
            break
        else:
            print("Opción inválida. Intente nuevamente.")

# Ejecutar el programa
main()
