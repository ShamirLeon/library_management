"""
Servicio de gestión de libros.

Este módulo contiene la lógica de negocio para la gestión del catálogo
de libros de la biblioteca, incluyendo operaciones CRUD y control de inventario.
"""

from models.books import Book
from datetime import datetime as dt


class BooksService:
    """
    Servicio para la gestión del catálogo de libros.
    
    Esta clase maneja todas las operaciones relacionadas con libros,
    incluyendo creación, consulta, eliminación y control de inventario.
    Mantiene una lista en memoria de libros disponibles en el catálogo.
    
    Attributes:
        books (list[Book]): Lista de libros en el catálogo de la biblioteca.
    """
    
    def __init__(self):
        """
        Inicializa el servicio de libros con un catálogo predeterminado.
        
        Crea tres libros de ejemplo para demostración:
        - Book 1: Author 1 (3 ejemplares)
        - Book 2: Author 2 (10 ejemplares)  
        - Book 3: Author 3 (10 ejemplares)
        """
        self.books = [
            Book(
                1,
                "Book 1",
                "Author 1",
                "2021-01-01",
                "1234567890",
                3,
                dt.today().date(),
                dt.today().date(),
            ),
            Book(
                2,
                "Book 2",
                "Author 2",
                "2021-01-01",
                "1234567890",
                10,
                dt.today().date(),
                dt.today().date(),
            ),
            Book(
                3,
                "Book 3",
                "Author 3",
                "2021-01-01",
                "1234567890",
                10,
                dt.today().date(),
                dt.today().date(),
            ),
        ]

    def add_book(self, title, author, published_date, isbn, quantity):
        """
        Agrega un nuevo libro al catálogo.
        
        Valida los datos del libro antes de crearlo:
        - El ISBN debe tener exactamente 10 caracteres
        - La cantidad debe ser mayor que 0
        - El título no puede estar vacío
        - El autor no puede estar vacío
        - Los campos se limpian de espacios en blanco
        
        Args:
            title (str): Título del libro.
            author (str): Autor del libro.
            published_date (str): Fecha de publicación del libro.
            isbn (str): Número ISBN del libro (debe tener 10 caracteres).
            quantity (str): Cantidad de ejemplares (se convierte a int).
            
        Returns:
            Book or None: El objeto libro creado si fue exitoso, None si falló la validación.
        """
        id = len(self.books) + 1
        if len(isbn) != 10:
            print("❌❌❌ ISBN must be 10 characters long ❌❌❌")
            return None
        if len(quantity) == 0:
            print("❌❌❌ Quantity must be greater than 0 ❌❌❌")
            return None
        if title.strip() == "":
            print("❌❌❌ Title must be greater than 0 ❌❌❌")
            return None
        if author.strip() == "":
            print("❌❌❌ Author must be greater than 0 ❌❌❌")
            return None
        
        book = Book(
            id,
            title.strip(),
            author.strip(),
            published_date.strip(),
            isbn.strip(),
            int(quantity.strip()),
            dt.today().date(),
            dt.today().date(),
        )
        self.books.append(book)
        return book

    def get_all_books(self):
        """
        Obtiene todos los libros del catálogo.
        
        Returns:
            list[Book]: Lista de todos los libros en el catálogo.
        """
        return self.books
    
    def get_book_by_id(self, id):
        """
        Busca un libro por su ID.
        
        Args:
            id (int): Identificador único del libro.
            
        Returns:
            Book or None: El objeto libro si fue encontrado, None si no existe.
        """
        for book in self.books:
            if book.id == id:
                return book
        return None

    def delete_book(self, id):
        """
        Elimina un libro del catálogo por su ID.
        
        Args:
            id (int): Identificador único del libro a eliminar.
            
        Returns:
            Book or None: El objeto libro eliminado si fue encontrado, None si no existe.
        """
        print(f"Deleting book {id}...")
        for book in self.books:
            if book.id == id:
                self.books.remove(book)
                return book
        return None
    
    def decrement_quantity(self, id):
        """
        Disminuye la cantidad disponible de un libro en 1 unidad.
        
        Utilizado cuando se presta un libro. Actualiza la fecha de modificación.
        
        Args:
            id (int): Identificador único del libro.
            
        Returns:
            Book or None: El objeto libro actualizado si fue encontrado, None si no existe.
        """
        print(f"Decrementing quantity of book {id}...")
        for book in self.books:
            print(book.id == id)
            if book.id == id:
                book.quantity -= 1
                book.updated_at = dt.today().date()
                return book
        return None
    
    def increment_quantity(self, id):
        """
        Aumenta la cantidad disponible de un libro en 1 unidad.
        
        Utilizado cuando se devuelve un libro. Actualiza la fecha de modificación.
        
        Args:
            id (int): Identificador único del libro.
            
        Returns:
            Book or None: El objeto libro actualizado si fue encontrado, None si no existe.
        """
        for book in self.books:
            if book.id == id:
                book.quantity += 1
                book.updated_at = dt.today().date()
                return book
        return None

