"""
Sistema de Gestión de Biblioteca

Este módulo principal contiene la interfaz de usuario para el sistema de gestión de biblioteca.
Permite a los usuarios autenticarse y realizar operaciones CRUD sobre usuarios, libros y movimientos.
"""

from services.users_service import UsersService
from services.books_service import BooksService
from services.movements_service import MovementsService
from getpass import getpass

# Initialize services
users_service = UsersService()
books_service = BooksService()
movements_service = MovementsService(books_service)

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
    author = input("Enter the author of the book: ")
    published_date = input("Ingresa la fecha de publicación del libro: ")
    isbn = input("Ingresa el ISBN del libro: ")
    quantity = input("Ingresa la cantidad disponible del libro: ")
    book = books_service.add_book(title, author, published_date, isbn, quantity)
    if book:
        print(f"Libro {book.title} agregado exitosamente 🎉")
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


""" Movements """


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


# Display admin menu
def admin_menu():
    """
    Muestra el menú principal de administración del sistema.
    
    Permite al usuario autenticado realizar todas las operaciones disponibles:
    - Gestión de usuarios (agregar, listar, eliminar)
    - Gestión de libros (agregar, listar, eliminar)
    - Gestión de movimientos (préstamos y devoluciones)
    
    El menú se ejecuta en un bucle hasta que el usuario elija salir.
    """
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
        print("SALIR")
        print("10. Salir")
        option = input("Ingresa una opción: ")

        if option == "1":
            add_user()
        elif option == "2":
            get_all_users()
        elif option == "3":
            delete_user()
        elif option == "4":
            add_book()
        elif option == "5":
            get_all_books()
        elif option == "6":
            delete_book()
        elif option == "7":
            add_movement()
        elif option == "8":
            get_all_movements()
        elif option == "9":
            return_movement()
        elif option == "10":
            break
        else:
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
