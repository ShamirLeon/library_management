class Book():
    """
    Modelo de datos para representar un libro en el catálogo de la biblioteca.
    
    Esta clase encapsula toda la información relacionada con un libro,
    incluyendo sus datos bibliográficos, disponibilidad y metadatos de auditoría.
    
    Attributes:
        id (int): Identificador único del libro.
        title (str): Título del libro.
        author (str): Autor del libro.
        published_date (str): Fecha de publicación del libro (formato string).
        isbn (str): Número ISBN del libro (debe tener 10 caracteres).
        quantity (int): Cantidad de ejemplares disponibles.
        created_at (date): Fecha de creación del registro.
        updated_at (date): Fecha de última actualización del registro.
    """
    
    def __init__(self, id, title, author, published_date, isbn, quantity, created_at, updated_at):
        """
        Inicializa una nueva instancia de Book.
        
        Args:
            id (int): Identificador único del libro.
            title (str): Título del libro.
            author (str): Autor del libro.
            published_date (str): Fecha de publicación del libro.
            isbn (str): Número ISBN del libro.
            quantity (int): Cantidad de ejemplares disponibles.
            created_at (date): Fecha de creación del registro.
            updated_at (date): Fecha de última actualización del registro.
        """
        self.id = id
        self.title = title
        self.author = author
        self.published_date = published_date
        self.isbn = isbn
        self.quantity = quantity
        self.created_at = created_at
        self.updated_at = updated_at
    
    def __str__(self):
        """
        Retorna una representación en cadena del objeto Book.
        
        Returns:
            str: Representación textual del libro con todos sus atributos.
        """
        return f"Book(id={self.id}, title={self.title}, author={self.author}, published_date={self.published_date}, isbn={self.isbn}, quantity={self.quantity}, created_at={self.created_at}, updated_at={self.updated_at})"