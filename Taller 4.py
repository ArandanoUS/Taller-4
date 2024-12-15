import redis

# Configuración de la conexión con KeyDB
KEYDB_HOST = "localhost"
KEYDB_PORT = 6379
KEYDB_DB = 0

keydb = redis.Redis(host=KEYDB_HOST, port=KEYDB_PORT, db=KEYDB_DB, decode_responses=True)

# Funciones de CRUD
def agregar_receta():
    """Agregar una nueva receta."""
    try:
        nombre = input("Nombre de la receta: ")
        if keydb.exists(nombre):
            print("❌ Ya existe una receta con ese nombre.")
            return

        ingredientes = input("Ingredientes (separados por comas): ")
        pasos = input("Pasos de la receta: ")

        keydb.hset(nombre, mapping={"ingredientes": ingredientes, "pasos": pasos})
        print("✅ Receta agregada exitosamente.")
    except Exception as e:
        print(f"❌ Error: {e}")

def actualizar_receta():
    """Actualizar una receta existente."""
    try:
        nombre = input("Nombre de la receta a actualizar: ")
        if not keydb.exists(nombre):
            print("❌ No se encontró la receta especificada.")
            return

        receta = keydb.hgetall(nombre)
        print(f"Receta encontrada:\nIngredientes: {receta['ingredientes']}\nPasos: {receta['pasos']}")

        nuevo_ingredientes = input("Nuevos ingredientes (dejar en blanco para no cambiar): ")
        nuevo_pasos = input("Nuevos pasos (dejar en blanco para no cambiar): ")

        if nuevo_ingredientes:
            keydb.hset(nombre, "ingredientes", nuevo_ingredientes)
        if nuevo_pasos:
            keydb.hset(nombre, "pasos", nuevo_pasos)

        print("✅ Receta actualizada exitosamente.")
    except Exception as e:
        print(f"❌ Error: {e}")

def eliminar_receta():
    """Eliminar una receta existente."""
    try:
        nombre = input("Nombre de la receta a eliminar: ")
        if not keydb.exists(nombre):
            print("❌ No se encontró la receta especificada.")
            return

        keydb.delete(nombre)
        print("✅ Receta eliminada exitosamente.")
    except Exception as e:
        print(f"❌ Error: {e}")

def ver_listado_recetas():
    """Mostrar el listado de todas las recetas."""
    try:
        claves = keydb.keys()
        if claves:
            print("📜 Listado de recetas:")
            for i, clave in enumerate(claves, start=1):
                print(f"{i}. {clave}")
        else:
            print("❌ No hay recetas disponibles.")
    except Exception as e:
        print(f"❌ Error: {e}")

def buscar_receta():
    """Buscar los detalles de una receta específica."""
    try:
        nombre = input("Nombre de la receta a buscar: ")
        if not keydb.exists(nombre):
            print("❌ No se encontró la receta especificada.")
            return

        receta = keydb.hgetall(nombre)
        print(f"📖 Receta: {nombre}")
        print(f"Ingredientes: {receta['ingredientes']}")
        print(f"Pasos: {receta['pasos']}")
    except Exception as e:
        print(f"❌ Error: {e}")

# Menú principal
def menu():
    """Mostrar el menú principal y gestionar las opciones del usuario."""
    while True:
        print("\n=== Libro de Recetas ===")
        print("1. Agregar nueva receta")
        print("2. Actualizar receta existente")
        print("3. Eliminar receta existente")
        print("4. Ver listado de recetas")
        print("5. Buscar ingredientes y pasos de receta")
        print("6. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            agregar_receta()
        elif opcion == "2":
            actualizar_receta()
        elif opcion == "3":
            eliminar_receta()
        elif opcion == "4":
            ver_listado_recetas()
        elif opcion == "5":
            buscar_receta()
        elif opcion == "6":
            print("👋 ¡Hasta luego!")
            break
        else:
            print("❌ Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    menu()
