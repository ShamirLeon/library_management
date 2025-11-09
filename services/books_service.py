"""
Servicio de gestión de libros.

Este módulo contiene la lógica de negocio para la gestión del catálogo
de libros de la biblioteca, incluyendo operaciones CRUD y control de inventario.
"""

from models.books import Book
from datetime import datetime as dt
from services.persistencia_service import ServicioPersistencia


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
        Inicializa el servicio de libros cargando desde archivo JSON.
        Si no existen datos, crea libros de ejemplo por defecto.
        """
        self.persistencia = ServicioPersistencia()
        self.books = []
        self._cargar_libros()
        
        # Si no hay libros, crear algunos por defecto
        if not self.books:
            self.books = [
                Book(
                    1,
                    "Cien años de soledad",
                    "Gabriel García Márquez",
                    "1967-05-30",
                    "9780307474728",
                    5,
                    dt.today().date(),
                    dt.today().date(),
                ),
                Book(
                    2,
                    "1984",
                    "George Orwell",
                    "1949-06-08",
                    "9780451524935",
                    4,
                    dt.today().date(),
                    dt.today().date(),
                ),
                Book(
                    3,
                    "Don Quijote de la Mancha",
                    "Miguel de Cervantes",
                    "1605-01-16",
                    "9788420412145",
                    3,
                    dt.today().date(),
                    dt.today().date(),
                ),
            ]
            self._guardar_libros()
    
    def _cargar_libros(self):
        """
        Carga libros desde archivo JSON y los convierte a objetos Book.
        """
        datos_libros = self.persistencia.cargar_libros()
        self.books = []
        
        for datos in datos_libros:
            libro = Book(
                datos['id'],
                datos['title'],
                datos['author'],
                datos['published_date'],
                datos['isbn'],
                datos['quantity'],
                datos['created_at'],
                datos['updated_at']
            )
            self.books.append(libro)
    
    def _guardar_libros(self):
        """
        Guarda la lista actual de libros en archivo JSON.
        """
        self.persistencia.guardar_libros(self.books)

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
            print("❌❌❌ El ISBN debe tener 10 caracteres ❌❌❌")
            return None
        if len(quantity) == 0:
            print("❌❌❌ La cantidad debe ser mayor que 0 ❌❌❌")
            return None
        if title.strip() == "":
            print("❌❌❌ El título no puede estar vacío ❌❌❌")
            return None
        if author.strip() == "":
            print("❌❌❌ El autor no puede estar vacío ❌❌❌")
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
        self._guardar_libros()
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
        print(f"Eliminando libro {id}...")
        for book in self.books:
            if book.id == id:
                self.books.remove(book)
                self._guardar_libros()
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
        print(f"Disminuyendo cantidad del libro {id}...")
        for book in self.books:
            print(book.id == id)
            if book.id == id:
                book.quantity -= 1
                book.updated_at = dt.today().date()
                self._guardar_libros()
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
                self._guardar_libros()
                return book
        return None
    
    def obtener_libro_por_id(self, id):
        """
        Busca un libro por su ID (versión en español).
        
        Args:
            id (int): Identificador único del libro.
            
        Returns:
            Book or None: El objeto libro si fue encontrado, None si no existe.
        """
        return self.get_book_by_id(id)

