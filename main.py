"""
Sistema de Gestión de Biblioteca

Este módulo principal contiene la interfaz de usuario para el sistema de gestión de biblioteca.
Permite a los usuarios autenticarse y realizar operaciones CRUD sobre usuarios, libros y movimientos.
"""

from services.users_service import UsersService
from services.books_service import BooksService
from services.movements_service import MovementsService
from services.categorias_service import ServicioCategorias
from services.persistencia_service import ServicioPersistencia
from services.graph_service import GraphService
from getpass import getpass

# Initialize services
users_service = UsersService()
books_service = BooksService()
graph_service = GraphService()
movements_service = MovementsService(books_service, graph_service)
categorias_service = ServicioCategorias(books_service)
persistencia_service = ServicioPersistencia()

# Inicializar libros con categorías de ejemplo
def inicializar_categorias_ejemplo():
    """
    Inicializa algunos libros con categorías de ejemplo para demostrar el sistema.
    """
    # Categorizar libros existentes
    try:
        # "Cien años de soledad" -> Ficción > Novela
        categorias_service.asignar_libro_a_categoria(1, "Novela")
        categorias_service.asignar_libro_a_categoria(1, "Ficción")
        
        # "1984" -> Ficción > Ciencia Ficción
        categorias_service.asignar_libro_a_categoria(2, "Ciencia Ficción")
        categorias_service.asignar_libro_a_categoria(2, "Ficción")
        
        # Si existe un tercer libro, categorizarlo manualmente
        if len(books_service.get_all_books()) > 2:
            libro_3 = books_service.get_all_books()[2]
            # Categorizar en una categoría general por defecto
            categorias_service.asignar_libro_a_categoria(libro_3.id, "No Ficción")
    except:
        # Si hay errores en la inicialización, continuar silenciosamente
        pass

# Inicializar categorías de ejemplo
inicializar_categorias_ejemplo()

# Functions
""" Users """


def login():
    """
    Permite a un usuario autenticarse en el sistema.
    
    Returns:
        User or None: El objeto usuario si las credenciales son válidas, None en caso contrario.
    """
    email = input("Ingresa tu email: ")
    password = input("Ingresa tu contraseña: ")
    user = users_service.login(email, password)
    return user


def add_user():
    """
    Permite agregar un nuevo usuario al sistema.
    
    Solicita al usuario los datos necesarios para crear un nuevo usuario:
    - Nombre del usuario
    - Email del usuario
    - Contraseña del usuario
    
    Returns:
        User or None: El objeto usuario creado si fue exitoso, None si falló.
    """
    name = input("Ingresa el nombre del usuario: ")
    email = input("Ingresa el email del usuario: ")
    password = getpass("Ingresa la contraseña del usuario: ")
    user = users_service.add_user(email, password, name)
    if user:
        print(f"Usuario {user.name} agregado exitosamente 🎉")
    else:
        print("Error al agregar usuario ❌")
    return user


def get_all_users():
    """
    Obtiene y muestra todos los usuarios registrados en el sistema.
    
    Returns:
        list[User]: Lista de todos los usuarios en el sistema.
    """
    users = users_service.get_all_users()
    for user in users:
        print(f"{user.id} - {user.name} - {user.email} - {user.created_at}")
    return users


def delete_user():
    """
    Permite eliminar un usuario del sistema por su ID.
    
    Returns:
        User or None: El objeto usuario eliminado si fue exitoso, None si no se encontró.
    """
    id = int(input("Ingresa el ID del usuario: "))
    user = users_service.delete_user(id)
    if user:
        print(f"Usuario {user.name} eliminado exitosamente 🎉")
    else:
        print("Error al eliminar usuario ❌")
    return user


""" Books """


def add_book():
    """
    Permite agregar un nuevo libro al catálogo de la biblioteca.
    
    Solicita al usuario los datos necesarios para crear un nuevo libro:
    - Título del libro
    - Autor del libro
    - Fecha de publicación
    - ISBN (debe tener 10 caracteres)
    - Cantidad disponible
    
    Returns:
        Book or None: El objeto libro creado si fue exitoso, None si falló.
    """
    title = input("Ingresa el título del libro: ")
    author = input("Ingresa el autor del libro: ")
    published_date = input("Ingresa la fecha de publicación del libro: ")
    isbn = input("Ingresa el ISBN del libro: ")
    quantity = input("Ingresa la cantidad disponible del libro: ")
    
    book = books_service.add_book(title, author, published_date, isbn, quantity)
    if book:
        print(f"Libro {book.title} agregado exitosamente 🎉✅✅")
        print("📝 Puedes categorizar el libro en el menú de categorías.")
    else:
        print("Error al agregar libro")
    return book


def get_all_books():
    """
    Obtiene y muestra todos los libros disponibles en el catálogo.
    
    Returns:
        list[Book]: Lista de todos los libros en el catálogo.
    """
    books = books_service.get_all_books()
    for book in books:
        print(
            f"ID: {book.id} - Título: {book.title} - Autor: {book.author} - Fecha de Publicación: {book.published_date} - ISBN: {book.isbn} - Cantidad: {book.quantity} - Fecha de Creación: {book.created_at}"
        )
    return books


def delete_book():
    """
    Permite eliminar un libro del catálogo por su ID.
    
    Primero muestra la lista de libros disponibles para que el usuario pueda elegir.
    
    Returns:
        Book or None: El objeto libro eliminado si fue exitoso, None si no se encontró.
    """
    print("--------------------------------")
    get_all_books()
    print("--------------------------------")
    id = int(input("Ingresa el ID del libro: "))
    book = books_service.delete_book(id)
    if book:
        print(f"Libro {book.title} eliminado exitosamente 🎉")
    else:
        print("Error al eliminar libro")
    return book


""" Movimientos """


def add_movement():
    """
    Permite crear un nuevo préstamo de libro.
    
    Solicita al usuario los datos necesarios para crear un préstamo:
    - ID del libro (muestra lista de libros disponibles)
    - Nombre del estudiante
    - Identificación del estudiante (debe tener 10 caracteres)
    - Fecha de devolución esperada (formato YYYY-MM-DD)
    
    Returns:
        Movement or None: El objeto movimiento creado si fue exitoso, None si falló.
    """
    print("--------------------------------")
    get_all_books()
    print("--------------------------------")
    book_id = int(input("Ingresa el ID del libro: "))
    student_name = input("Ingresa el nombre del estudiante: ")
    student_identification = input("Ingresa la identificación del estudiante: ")
    return_date = input("Ingresa la fecha de devolución (YYYY-MM-DD): ")
    movement = movements_service.add_movement(
        book_id, student_name, student_identification, return_date
    )
    if movement:
        print(f"Movimiento {movement.id} agregado exitosamente 🎉")
    else:
        print("Error al agregar movimiento")
    return movement


def get_all_movements():
    """
    Obtiene y muestra todos los movimientos (préstamos) registrados en el sistema.
    
    Returns:
        list[Movement]: Lista de todos los movimientos en el sistema.
    """
    movements = movements_service.get_all_movements()
    for movement in movements:
        print(
            f"ID: {movement.id} - ID del Libro: {movement.book_id} - Nombre del Estudiante: {movement.student_name} - Identificación del Estudiante: {movement.student_identification} - Fecha de Préstamo: {movement.loan_date} - Fecha de Devolución: {movement.return_date} - Devuelto: {'Sí' if movement.returned else 'No'} - Creado el: {movement.created_at} - Actualizado el: {movement.updated_at}"
        )
    return movements


def return_movement():
    """
    Permite marcar un libro como devuelto.
    
    Primero muestra la lista de movimientos para que el usuario pueda elegir.
    Al devolver un libro, se incrementa la cantidad disponible del mismo.
    
    Returns:
        Movement or None: El objeto movimiento actualizado si fue exitoso, None si falló.
    """
    print("--------------------------------")
    get_all_movements()
    print("--------------------------------")
    id = int(input("Ingresa el ID del movimiento: "))
    movement = movements_service.return_movement(id)
    if movement:
        print(f"Libro devuelto exitosamente 🎉")
    else:
        print("Error al devolver movimiento")
    return movement


""" Categorías """


def mostrar_estructura_categorias():
    """
    Muestra la estructura completa del árbol de categorías.
    
    Permite al usuario ver la organización jerárquica de las categorías
    y la cantidad de libros en cada una.
    """
    print("\nESTRUCTURA DE CATEGORÍAS")
    print("=" * 50)
    estructura = categorias_service.mostrar_estructura_categorias()
    print(estructura)
    
    # Mostrar resumen general
    resumen = categorias_service.obtener_resumen_general()
    print(f"\nRESUMEN GENERAL:")
    print(f"   • Total de categorías: {resumen['total_categorias']}")
    print(f"   • Categorías con libros: {resumen['categorias_con_libros']}")
    print(f"   • Categorías vacías: {resumen['categorias_vacias']}")
    print(f"   • Total de libros categorizados: {resumen['total_libros_categorizados']}")
    print(f"   • Utilización: {resumen['porcentaje_categorias_utilizadas']}%")
    if resumen['categoria_mas_poblada']['nombre']:
        print(f"   • Categoría más popular: {resumen['categoria_mas_poblada']['nombre']} ({resumen['categoria_mas_poblada']['cantidad']} libros)")


def crear_nueva_categoria():
    """
    Permite crear una nueva categoría en el sistema.
    
    Solicita el nombre de la categoría padre, el nombre de la nueva categoría
    y opcionalmente una descripción.
    """
    print("CREAR NUEVA CATEGORÍA")
    print("=" * 30)
    
    # Mostrar categorías disponibles
    categorias_disponibles = categorias_service.listar_todas_las_categorias()
    print("Categorías disponibles como padre:")
    for i, categoria in enumerate(categorias_disponibles, 1):
        print(f"   {i}. {categoria}")
    
    print("\nTambién puedes usar: 'Biblioteca General' como categoría principal")
    
    nombre_padre = input("\nIngresa el nombre de la categoría padre: ").strip()
    nombre_categoria = input("Ingresa el nombre de la nueva categoría: ").strip()
    descripcion = input("Ingresa una descripción (opcional): ").strip()
    
    resultado = categorias_service.crear_categoria(nombre_padre, nombre_categoria, descripcion)
    
    if resultado['exito']:
        print(f"{resultado['mensaje']}")
    else:
        print(f"{resultado['mensaje']}")


def asignar_libro_a_categoria():
    """
    Permite asignar un libro existente a una categoría.
    
    Muestra la lista de libros disponibles y categorías para facilitar la selección.
    """
    print("\nASIGNAR LIBRO A CATEGORÍA")
    print("=" * 40)
    
    # Mostrar libros disponibles
    print("Libros disponibles:")
    libros = books_service.get_all_books()
    if not libros:
        print("❌ No hay libros disponibles en el catálogo.")
        return
    
    for libro in libros:
        # Mostrar categorías actuales del libro
        categorias_actuales = categorias_service.buscar_categorias_de_libro(libro.id)
        cats_str = ", ".join(categorias_actuales['categorias']) if categorias_actuales['categorias'] else "Sin categorizar"
        print(f"   ID: {libro.id} - {libro.title} por {libro.author} (Categorías: {cats_str})")
    
    # Mostrar categorías disponibles
    print("\nCategorías disponibles:")
    categorias_disponibles = categorias_service.listar_todas_las_categorias()
    for i, categoria in enumerate(categorias_disponibles, 1):
        stats = categorias_service.obtener_estadisticas(categoria)
        print(f"   {i}. {categoria} ({stats['libros_directos']} libros)")
    
    try:
        id_libro = int(input("\nIngresa el ID del libro: "))
        nombre_categoria = input("Ingresa el nombre de la categoría: ").strip()
        
        resultado = categorias_service.asignar_libro_a_categoria(id_libro, nombre_categoria)
        
        if resultado['exito']:
            print(f"✅ {resultado['mensaje']}")
        else:
            print(f"❌ {resultado['mensaje']}")
            
    except ValueError:
        print("❌ Por favor ingresa un ID de libro válido.")


def ver_libros_por_categoria():
    """
    Muestra los libros pertenecientes a una categoría específica.
    
    Permite al usuario elegir si incluir subcategorías en la búsqueda.
    """
    print("\nVER LIBROS POR CATEGORÍA")
    print("=" * 35)
    
    # Mostrar categorías disponibles con cantidad de libros
    categorias_disponibles = categorias_service.listar_todas_las_categorias()
    print("Categorías disponibles:")
    for i, categoria in enumerate(categorias_disponibles, 1):
        stats = categorias_service.obtener_estadisticas(categoria)
        print(f"   {i}. {categoria} ({stats['libros_directos']} directos, {stats['libros_totales']} total)")
    
    nombre_categoria = input("\nIngresa el nombre de la categoría: ").strip()
    incluir_subcategorias = input("¿Incluir subcategorías? (s/n): ").strip().lower() == 's'
    
    resultado = categorias_service.obtener_libros_por_categoria(nombre_categoria, incluir_subcategorias)
    
    if resultado['exito']:
        print(f"\n{resultado['mensaje']}")
        if resultado['libros']:
            print("\n📚 Libros encontrados:")
            for libro in resultado['libros']:
                print(f"   • ID: {libro.id} - {libro.title} por {libro.author}")
                print(f"     Publicado: {libro.published_date} | ISBN: {libro.isbn} | Cantidad: {libro.quantity}")
        else:
            print("No se encontraron libros en esta categoría.")
    else:
        print(f"❌ {resultado['mensaje']}")


def buscar_libros_por_termino_categoria():
    """
    Busca libros en categorías que contengan un término específico.
    
    Útil para encontrar libros por tema sin conocer la categoría exacta.
    """
    print("\n BUSCAR POR TÉRMINO EN CATEGORÍAS")
    print("=" * 40)
    
    termino = input("Ingresa el término a buscar en nombres de categorías: ").strip()
    
    if not termino:
        print("Debes ingresar un término de búsqueda.")
        return
    
    resultado = categorias_service.buscar_libros_por_termino_en_categorias(termino)
    
    print(f"\n🔍 {resultado['mensaje']}")
    
    if resultado['categorias_encontradas']:
        print(f"\nCategorías que contienen '{termino}':")
        for categoria in resultado['categorias_encontradas']:
            print(f"   • {categoria}")
        
        if resultado['libros']:
            print(f"\nLibros encontrados ({resultado['cantidad_libros']}):")
            for libro in resultado['libros']:
                categorias_libro = categorias_service.buscar_categorias_de_libro(libro.id)
                cats_str = ", ".join(categorias_libro['categorias'])
                print(f"   • {libro.title} por {libro.author} (en: {cats_str})")


def ver_estadisticas_categoria():
    """
    Muestra estadísticas detalladas de una categoría específica o de todo el sistema.
    """
    print("\nESTADÍSTICAS DE CATEGORÍAS")
    print("=" * 35)
    
    print("Opciones:")
    print("1. Ver estadísticas de una categoría específica")
    print("2. Ver estadísticas generales del sistema")
    
    opcion = input("Elige una opción (1-2): ").strip()
    
    if opcion == "1":
        categorias_disponibles = categorias_service.listar_todas_las_categorias()
        print("\nCategorías disponibles:")
        for i, categoria in enumerate(categorias_disponibles, 1):
            print(f"   {i}. {categoria}")
        
        nombre_categoria = input("\nIngresa el nombre de la categoría: ").strip()
        stats = categorias_service.obtener_estadisticas(nombre_categoria)
        
        if stats:
            print(f"\nEstadísticas de '{nombre_categoria}':")
            print(f"   • Descripción: {stats['descripcion']}")
            print(f"   • Ruta: {stats['ruta']}")
            print(f"   • Libros directos: {stats['libros_directos']}")
            print(f"   • Libros totales (incluyendo subcategorías): {stats['libros_totales']}")
            print(f"   • Subcategorías: {stats['subcategorias']}")
            if stats['nombres_subcategorias']:
                print(f"   • Nombres de subcategorías: {', '.join(stats['nombres_subcategorias'])}")
        else:
            print(f"❌ La categoría '{nombre_categoria}' no existe.")
    
    elif opcion == "2":
        resumen = categorias_service.obtener_resumen_general()
        print(f"\nESTADÍSTICAS GENERALES DEL SISTEMA:")
        print(f"   • Total de categorías: {resumen['total_categorias']}")
        print(f"   • Categorías con libros: {resumen['categorias_con_libros']}")
        print(f"   • Categorías vacías: {resumen['categorias_vacias']}")
        print(f"   • Total de libros categorizados: {resumen['total_libros_categorizados']}")
        print(f"   • Porcentaje de utilización: {resumen['porcentaje_categorias_utilizadas']}%")
        
        if resumen['categoria_mas_poblada']['nombre']:
            print(f"   • Categoría más popular: {resumen['categoria_mas_poblada']['nombre']} con {resumen['categoria_mas_poblada']['cantidad']} libros")
    else:
        print("❌ Opción inválida.")


def remover_libro_de_categoria():
    """
    Permite remover un libro de una categoría específica.
    """
    print("\nREMOVER LIBRO DE CATEGORÍA")
    print("=" * 40)
    
    print("Libros categorizados:")
    libros = books_service.get_all_books()
    libros_categorizados = []
    
    for libro in libros:
        categorias_libro = categorias_service.buscar_categorias_de_libro(libro.id)
        if categorias_libro['categorias']:
            libros_categorizados.append(libro)
            cats_str = ", ".join(categorias_libro['categorias'])
            print(f"   ID: {libro.id} - {libro.title} (Categorías: {cats_str})")
    
    if not libros_categorizados:
        print("No hay libros categorizados en el sistema.")
        return
    
    try:
        id_libro = int(input("\nIngresa el ID del libro: "))
        
        # Mostrar categorías actuales del libro
        categorias_actuales = categorias_service.buscar_categorias_de_libro(id_libro)
        if not categorias_actuales['categorias']:
            print("❌ Este libro no está categorizado.")
            return
        
        print(f"\nCategorías actuales del libro:")
        for i, categoria in enumerate(categorias_actuales['categorias'], 1):
            print(f"   {i}. {categoria}")
        
        nombre_categoria = input("\nIngresa el nombre de la categoría de donde remover el libro: ").strip()
        
        resultado = categorias_service.remover_libro_de_categoria(id_libro, nombre_categoria)
        
        if resultado['exito']:
            print(f"✅ {resultado['mensaje']}")
        else:
            print(f"❌ {resultado['mensaje']}")
            
    except ValueError:
        print("❌ Por favor ingresa un ID de libro válido.")


""" Sistema de Recomendación con Grafos """
def recomendar_libros_por_historial():
    """
    Recomienda libros basado en el historial de préstamos del usuario.
    """
    print("\n📚 RECOMENDACIONES POR HISTORIAL")
    print("=" * 40)
    
    student_identification = input("Ingresa la identificación del estudiante (10 caracteres): ").strip()
    
    if len(student_identification) != 10:
        print("❌ La identificación debe tener 10 caracteres.")
        return
    
    libros = books_service.get_all_books()
    recomendaciones = graph_service.recomendar_libros_por_historial(
        student_identification, 
        libros, 
        limite=5
    )
    
    if recomendaciones:
        print(f"\n✅ {len(recomendaciones)} recomendaciones encontradas:")
        for i, libro in enumerate(recomendaciones, 1):
            print(f"   {i}. {libro.title} por {libro.author}")
            print(f"      ISBN: {libro.isbn} | Cantidad disponible: {libro.quantity}")
    else:
        print("❌ No se encontraron recomendaciones. El usuario puede no tener historial de préstamos.")


def recomendar_libros_por_usuarios_similares():
    """
    Recomienda libros basado en lo que han leído usuarios con gustos similares.
    """
    print("\n👥 RECOMENDACIONES POR USUARIOS SIMILARES")
    print("=" * 45)
    
    student_identification = input("Ingresa la identificación del estudiante (10 caracteres): ").strip()
    
    if len(student_identification) != 10:
        print("❌ La identificación debe tener 10 caracteres.")
        return
    
    libros = books_service.get_all_books()
    recomendaciones = graph_service.recomendar_libros_por_usuarios_similares(
        student_identification,
        libros,
        limite=5
    )
    
    if recomendaciones:
        print(f"\n✅ {len(recomendaciones)} recomendaciones basadas en usuarios similares:")
        for i, libro in enumerate(recomendaciones, 1):
            print(f"   {i}. {libro.title} por {libro.author}")
            print(f"      ISBN: {libro.isbn} | Cantidad disponible: {libro.quantity}")
    else:
        print("❌ No se encontraron recomendaciones. Puede que no haya usuarios similares.")


def ver_usuarios_similares():
    """
    Muestra usuarios con gustos similares a un usuario dado.
    """
    print("\n👥 USUARIOS CON GUSTOS SIMILARES")
    print("=" * 40)
    
    student_identification = input("Ingresa la identificación del estudiante (10 caracteres): ").strip()
    
    if len(student_identification) != 10:
        print("❌ La identificación debe tener 10 caracteres.")
        return
    
    usuarios_similares = graph_service.obtener_usuarios_similares(student_identification, limite=10)
    
    if usuarios_similares:
        print(f"\n✅ {len(usuarios_similares)} usuarios con gustos similares encontrados:")
        for i, (usuario_id, peso) in enumerate(usuarios_similares, 1):
            print(f"   {i}. Usuario ID: {usuario_id} - Libros compartidos: {peso}")
    else:
        print("❌ No se encontraron usuarios similares.")


def ver_popularidad_libros():
    """
    Muestra la popularidad de los libros según la cantidad de préstamos.
    """
    print("\n📊 POPULARIDAD DE LIBROS")
    print("=" * 35)
    
    limite = input("¿Cuántos libros deseas ver? (por defecto 10): ").strip()
    limite = int(limite) if limite.isdigit() else 10
    
    popularidad = graph_service.obtener_popularidad_libros(limite=limite)
    
    if popularidad:
        print(f"\n📚 Top {len(popularidad)} libros más populares:")
        for i, (book_id, cantidad_prestamos) in enumerate(popularidad, 1):
            libro = books_service.get_book_by_id(book_id)
            if libro:
                print(f"   {i}. {libro.title} por {libro.author}")
                print(f"      Préstamos realizados: {cantidad_prestamos}")
            else:
                print(f"   {i}. Libro ID {book_id} - Préstamos: {cantidad_prestamos}")
    else:
        print("❌ No hay datos de popularidad disponibles.")


def ver_estadisticas_grafo():
    """
    Muestra estadísticas generales del grafo de recomendación.
    """
    print("\n📊 ESTADÍSTICAS DEL GRAFO")
    print("=" * 35)
    
    stats = graph_service.obtener_estadisticas_grafo()
    
    print(f"\n📈 Estadísticas Generales:")
    print(f"   • Total de usuarios en el grafo: {stats['total_usuarios']}")
    print(f"   • Total de libros en el grafo: {stats['total_libros']}")
    print(f"   • Total de préstamos registrados: {stats['total_prestamos']}")
    print(f"   • Conexiones usuario-usuario: {stats['total_conexiones_usuario_usuario']}")
    print(f"   • Promedio de libros por usuario: {stats['promedio_libros_por_usuario']:.2f}")
    print(f"   • Promedio de usuarios por libro: {stats['promedio_usuarios_por_libro']:.2f}")


def ver_relaciones_indirectas():
    """
    Analiza relaciones indirectas entre libros y usuarios.
    """
    print("\n🔗 RELACIONES INDIRECTAS")
    print("=" * 35)
    
    student_identification = input("Ingresa la identificación del estudiante (10 caracteres): ").strip()
    
    if len(student_identification) != 10:
        print("❌ La identificación debe tener 10 caracteres.")
        return
    
    relaciones = graph_service.obtener_relaciones_indirectas(student_identification)
    
    print(f"\n📊 Análisis de relaciones indirectas:")
    print(f"   • Libros prestados directamente: {relaciones['libros_directos']}")
    print(f"   • Libros relacionados indirectamente: {relaciones['libros_indirectos']}")
    print(f"   • Usuarios relacionados: {relaciones['usuarios_relacionados']}")
    
    if relaciones['libros_indirectos_ids']:
        print(f"\n📚 Libros relacionados indirectamente:")
        for book_id in relaciones['libros_indirectos_ids'][:10]:  # Mostrar máximo 10
            libro = books_service.get_book_by_id(book_id)
            if libro:
                print(f"   • {libro.title} por {libro.author}")


def ver_historial_usuario():
    """
    Muestra el historial de préstamos de un usuario.
    """
    print("\n📖 HISTORIAL DE PRÉSTAMOS")
    print("=" * 35)
    
    student_identification = input("Ingresa la identificación del estudiante (10 caracteres): ").strip()
    
    if len(student_identification) != 10:
        print("❌ La identificación debe tener 10 caracteres.")
        return
    
    libros_prestados = graph_service.obtener_libros_prestados_por_usuario(student_identification)
    
    if libros_prestados:
        print(f"\n✅ {len(libros_prestados)} libros prestados:")
        for i, book_id in enumerate(libros_prestados, 1):
            libro = books_service.get_book_by_id(book_id)
            if libro:
                print(f"   {i}. {libro.title} por {libro.author}")
            else:
                print(f"   {i}. Libro ID {book_id} (no encontrado)")
    else:
        print("❌ El usuario no tiene historial de préstamos.")


def menu_recomendaciones():
    """
    Menú específico para el sistema de recomendación basado en grafos.
    """
    while True:
        print("\n" + "=" * 50)
        print("🔮 SISTEMA DE RECOMENDACIÓN DE LIBROS 🔮")
        print("=" * 50)
        print("📚 RECOMENDACIONES")
        print("1. Recomendar libros por historial")
        print("2. Recomendar libros por usuarios similares")
        print("-" * 50)
        print("👥 ANÁLISIS DE USUARIOS")
        print("3. Ver usuarios con gustos similares")
        print("4. Ver historial de préstamos de usuario")
        print("-" * 50)
        print("📊 ESTADÍSTICAS Y ANÁLISIS")
        print("5. Ver popularidad de libros")
        print("6. Ver estadísticas del grafo")
        print("7. Ver relaciones indirectas")
        print("-" * 50)
        print("🚪 NAVEGACIÓN")
        print("8. Volver al menú principal")
        
        opcion = input("\nIngresa una opción (1-8): ").strip()
        
        match opcion:
            case "1":
                recomendar_libros_por_historial()
            case "2":
                recomendar_libros_por_usuarios_similares()
            case "3":
                ver_usuarios_similares()
            case "4":
                ver_historial_usuario()
            case "5":
                ver_popularidad_libros()
            case "6":
                ver_estadisticas_grafo()
            case "7":
                ver_relaciones_indirectas()
            case "8":
                break
            case _:
                print("❌ Opción inválida. Por favor elige una opción del 1 al 8.")


""" Gestión de Datos y Persistencia """


def mostrar_estadisticas_datos():
    """
    Muestra estadísticas de los archivos de datos guardados.
    """
    print("\n📊 ESTADÍSTICAS DE DATOS GUARDADOS")
    print("=" * 40)
    
    estadisticas = persistencia_service.obtener_estadisticas_archivos()
    
    print("📂 Estado de archivos de datos:")
    for tipo, info in estadisticas.items():
        estado = "✅ Existe" if info['existe'] else "❌ No existe"
        cantidad = info.get('cantidad', info.get('cantidad_categorias', 0))
        
        if tipo == 'usuarios':
            print(f"   👥 Usuarios: {estado} - {cantidad} registros")
        elif tipo == 'libros':
            print(f"   📚 Libros: {estado} - {cantidad} registros")
        elif tipo == 'movimientos':
            print(f"   🔄 Movimientos: {estado} - {cantidad} registros")
        elif tipo == 'categorias_libros':
            print(f"   🗂️  Categorías: {estado} - {cantidad} asignaciones")


def crear_respaldo_completo():
    """
    Crea un respaldo completo de todos los datos del sistema.
    """
    print("\n💾 CREAR RESPALDO COMPLETO")
    print("=" * 30)
    
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_respaldo = f"respaldo_{timestamp}.json"
    
    print(f"Creando respaldo: {nombre_respaldo}")
    
    exito = persistencia_service.exportar_todo(nombre_respaldo)
    
    if exito:
        print("✅ Respaldo creado exitosamente")
        print(f"📁 Ubicación: datos/{nombre_respaldo}")
    else:
        print("❌ Error al crear el respaldo")


def mostrar_informacion_sistema():
    """
    Muestra información general del sistema y su estado.
    """
    print("\n🖥️ INFORMACIÓN DEL SISTEMA")
    print("=" * 35)
    
    # Estadísticas generales
    total_usuarios = len(users_service.get_all_users())
    total_libros = len(books_service.get_all_books())
    total_movimientos = len(movements_service.get_all_movements())
    
    # Movimientos activos (no devueltos)
    movimientos_activos = sum(1 for m in movements_service.get_all_movements() if not m.returned)
    
    # Estadísticas de categorías
    resumen_categorias = categorias_service.obtener_resumen_general()
    
    print("📊 Datos en memoria:")
    print(f"   👥 Usuarios: {total_usuarios}")
    print(f"   📚 Libros: {total_libros}")
    print(f"   🔄 Movimientos: {total_movimientos}")
    print(f"   📖 Préstamos activos: {movimientos_activos}")
    print(f"   🗂️  Categorías utilizadas: {resumen_categorias['categorias_con_libros']}")
    print(f"   📚 Libros categorizados: {resumen_categorias['total_libros_categorizados']}")
    
    print("\n💾 Estado de persistencia:")
    estadisticas = persistencia_service.obtener_estadisticas_archivos()
    archivos_existentes = sum(1 for info in estadisticas.values() if info['existe'])
    print(f"   📁 Archivos de datos: {archivos_existentes}/4 existentes")
    
    if archivos_existentes > 0:
        print("   ✅ La persistencia está funcionando")
    else:
        print("   ⚠️ No se han guardado datos aún")


def menu_gestion_datos():
    """
    Menú para la gestión de datos y persistencia del sistema.
    """
    while True:
        print("\n" + "=" * 45)
        print("💾 GESTIÓN DE DATOS Y PERSISTENCIA 💾")
        print("=" * 45)
        print("📊 INFORMACIÓN")
        print("1. Ver estadísticas de datos")
        print("2. Ver información del sistema")
        print("-" * 45)
        print("💾 RESPALDOS")
        print("3. Crear respaldo completo")
        print("-" * 45)
        print("🚪 NAVEGACIÓN")
        print("4. Volver al menú principal")
        
        opcion = input("\nIngresa una opción (1-4): ").strip()
        
        if opcion == "1":
            mostrar_estadisticas_datos()
        elif opcion == "2":
            mostrar_informacion_sistema()
        elif opcion == "3":
            crear_respaldo_completo()
        elif opcion == "4":
            break
        else:
            print("❌ Opción inválida. Por favor elige una opción del 1 al 4.")


def menu_categorias():
    """
    Menú específico para la gestión de categorías.
    
    Proporciona todas las opciones relacionadas con la organización
    temática del catálogo de libros.
    """
    while True:
        print("\n" + "=" * 50)
        print("🌳 GESTIÓN DE CATEGORÍAS DE LIBROS 🌳")
        print("=" * 50)
        print("📋 VISUALIZACIÓN")
        print("1. Ver estructura de categorías")
        print("2. Ver libros por categoría")
        print("3. Buscar por término en categorías")
        print("4. Ver estadísticas de categorías")
        print("-" * 50)
        print("📝 GESTIÓN")
        print("5. Crear nueva categoría")
        print("6. Asignar libro a categoría")
        print("7. Remover libro de categoría")
        print("-" * 50)
        print("🚪 NAVEGACIÓN")
        print("8. Volver al menú principal")
        
        opcion = input("\nIngresa una opción (1-8): ").strip()
        
        # Implementamos match-case para mejorar legibilidad y manejar opciones digitadas por el usuario.
        match opcion:
            case "1":
                mostrar_estructura_categorias()
            case "2":
                ver_libros_por_categoria()
            case "3":
                buscar_libros_por_termino_categoria()
            case "4":
                ver_estadisticas_categoria()
            case "5":
                crear_nueva_categoria()
            case "6":
                asignar_libro_a_categoria()
            case "7":
                remover_libro_de_categoria()
            case "8":
                break
            case _:
                print("Opción inválida. Por favor elige una opción del 1 al 8.")


def admin_menu():
    while True:
        print("--------------------------------")
        print("Menú de Administrador")
        print("--------------------------------")
        print("USUARIOS")
        print("1. Agregar Usuario")
        print("2. Ver Todos los Usuarios")
        print("3. Eliminar Usuario")
        print("--------------------------------")
        print("LIBROS")
        print("4. Agregar Libro")
        print("5. Ver Todos los Libros")
        print("6. Eliminar Libro")
        print("--------------------------------")
        print("MOVIMIENTOS")
        print("7. Prestar un libro")
        print("8. Ver Todos los Movimientos")
        print("9. Devolver Libro")
        print("--------------------------------")
        print("CATEGORÍAS")
        print("10. Gestionar Categorías")
        print("--------------------------------")
        print("CATEGORÍAS")
        print("10. Gestionar Categorías")
        print("--------------------------------")
        print("RECOMENDACIONES")
        print("11. Sistema de Recomendación")
        print("--------------------------------")
        print("DATOS")
        print("12. Gestión de Datos")
        print("--------------------------------")
        print("SALIR")
        print("13. Salir")
        option = input("Ingresa una opción: ")

        match option:
            case "1":
                add_user()
            case "2":
                get_all_users()
            case "3":
                delete_user()
            case "4":
                add_book()
            case "5":
                get_all_books()
            case "6":
                delete_book()
            case "7":
                add_movement()
            case "8":
                get_all_movements()
            case "9":
                return_movement()
            case "10":
                menu_categorias()
            case "11":
                menu_recomendaciones()
            case "12":
                menu_gestion_datos()
            case "13":
                break
            case _:
                print("Opción inválida")


def menu():
    """
    Muestra el menú principal del sistema de gestión de biblioteca.
    
    Permite al usuario:
    - Iniciar sesión en el sistema
    - Salir de la aplicación
    
    Si el login es exitoso, redirige al menú de administración.
    El menú se ejecuta en un bucle hasta que el usuario elija salir.
    """
    while True:
        print("--------------------------------")
        print("Sistema de Gestión de Biblioteca")
        print("--------------------------------")
        print("1. Iniciar Sesión")
        print("2. Salir")
        option = input("Ingresa una opción: ")
        if option == "1":
            print("Iniciando sesión...")
            user = login()
            if user:
                print(f"Bienvenido {user.name}")
                admin_menu()
            else:
                print("Email o contraseña inválidos")
        elif option == "2":
            print("Saliendo...")
            break
        else:
            print("Opción inválida")


if __name__ == "__main__":
    menu()
