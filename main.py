"""
Sistema de Gestión de Biblioteca

Este módulo principal contiene la interfaz de usuario para el sistema de gestión de biblioteca.
Permite a los usuarios autenticarse y realizar operaciones CRUD sobre usuarios, libros y movimientos.

Autor: [Tu nombre]
Fecha: [Fecha actual]
"""

from services.users_service import UsersService
from services.books_service import BooksService
from services.movements_service import MovementsService

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
    email = input("Enter your email: ")
    password = input("Enter your password: ")
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
    name = input("Enter the name of the user: ")
    email = input("Enter the email of the user: ")
    password = input("Enter the password of the user: ")
    user = users_service.add_user(email, password, name)
    if user:
        print(f"User {user.name} added successfully 🎉")
    else:
        print("Failed to add user ❌")
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
    id = int(input("Enter the id of the user: "))
    user = users_service.delete_user(id)
    if user:
        print(f"User {user.name} deleted successfully 🎉")
    else:
        print("Failed to delete user ❌")
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
    title = input("Enter the title of the book: ")
    author = input("Enter the author of the book: ")
    published_date = input("Enter the published date of the book: ")
    isbn = input("Enter the isbn of the book: ")
    quantity = input("Enter the quantity of the book: ")
    book = books_service.add_book(title, author, published_date, isbn, quantity)
    if book:
        print(f"Book {book.title} added successfully 🎉")
    else:
        print("Failed to add book")
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
            f"ID: {book.id} - Title: {book.title} - Author: {book.author} - Published Date: {book.published_date} - ISBN: {book.isbn} - Quantity: {book.quantity} - Created At: {book.created_at}"
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
    id = int(input("Enter the id of the book: "))
    book = books_service.delete_book(id)
    if book:
        print(f"Book {book.title} deleted successfully 🎉")
    else:
        print("Failed to delete book")
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
    book_id = int(input("Enter the id of the book: "))
    student_name = input("Enter the name of the student: ")
    student_identification = input("Enter the identification of the student: ")
    return_date = input("Enter the date of the return (YYYY-MM-DD): ")
    movement = movements_service.add_movement(
        book_id, student_name, student_identification, return_date
    )
    if movement:
        print(f"Movement {movement.id} added successfully 🎉")
    else:
        print("Failed to add movement")
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
            f"ID: {movement.id} - Book ID: {movement.book_id} - Student Name: {movement.student_name} - Student Identification: {movement.student_identification} - Loan Date: {movement.loan_date} - Return Date: {movement.return_date} - Returned: {'Yes' if movement.returned  else 'No'} - Created At: {movement.created_at} - Updated At: {movement.updated_at}"
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
    id = int(input("Enter the id of the movement: "))
    movement = movements_service.return_movement(id)
    if movement:
        print(f"Book returned successfully 🎉")
    else:
        print("Failed to return movement")
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
        print("Admin Menu")
        print("--------------------------------")
        print("USERS")
        print("1. Add User")
        print("2. Get All Users")
        print("3. Delete User")
        print("--------------------------------")
        print("BOOKS")
        print("4. Add Book")
        print("5. Get All Books")
        print("6. Delete Book")
        print("--------------------------------")
        print("MOVEMENTS")
        print("7. Borrow a book")
        print("8. Get All Movements")
        print("9. Return Book")
        print("--------------------------------")
        print("EXIT")
        print("10. Exit")
        option = input("Enter an option: ")

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
            print("Invalid option")


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
        print("Library Management System")
        print("--------------------------------")
        print("1. Login")
        print("2. Exit")
        option = input("Enter an option: ")
        if option == "1":
            print("Logging in...")
            user = login()
            if user:
                print(f"Welcome {user.name}")
                admin_menu()
            else:
                print("Invalid email or password")
        elif option == "2":
            print("Exiting...")
            break
        else:
            print("Invalid option")


if __name__ == "__main__":
    menu()
