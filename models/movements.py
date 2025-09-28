class Movement():
    """
    Modelo de datos para representar un movimiento (préstamo/devolución) en el sistema.
    
    Esta clase encapsula toda la información relacionada con el préstamo
    de un libro a un estudiante, incluyendo fechas, estado y metadatos de auditoría.
    
    Attributes:
        id (int): Identificador único del movimiento.
        book_id (int): ID del libro prestado.
        student_name (str): Nombre del estudiante que solicita el préstamo.
        student_identification (str): Número de identificación del estudiante (debe tener 10 caracteres).
        loan_date (date): Fecha en que se realizó el préstamo.
        return_date (date): Fecha programada o efectiva de devolución.
        returned (bool): Indica si el libro ha sido devuelto.
        created_at (date): Fecha de creación del registro.
        updated_at (date): Fecha de última actualización del registro.
    """
    
    def __init__(self, id, book_id, student_name, student_identification, loan_date, return_date, returned, created_at, updated_at):
        """
        Inicializa una nueva instancia de Movement.
        
        Args:
            id (int): Identificador único del movimiento.
            book_id (int): ID del libro prestado.
            student_name (str): Nombre del estudiante.
            student_identification (str): Número de identificación del estudiante.
            loan_date (date): Fecha en que se realizó el préstamo.
            return_date (date): Fecha programada o efectiva de devolución.
            returned (bool): Indica si el libro ha sido devuelto.
            created_at (date): Fecha de creación del registro.
            updated_at (date): Fecha de última actualización del registro.
        """
        self.id = id
        self.book_id = book_id
        self.student_name = student_name
        self.student_identification = student_identification
        self.loan_date = loan_date
        self.return_date = return_date
        self.returned = returned
        self.created_at = created_at
        self.updated_at = updated_at
    
    def __str__(self):
        """
        Retorna una representación en cadena del objeto Movement.
        
        Returns:
            str: Representación textual del movimiento con todos sus atributos.
        """
        return f"Movement(id={self.id}, book_id={self.book_id}, student_name={self.student_name}, student_identification={self.student_identification}, loan_date={self.loan_date}, return_date={self.return_date}, created_at={self.created_at}, updated_at={self.updated_at})"