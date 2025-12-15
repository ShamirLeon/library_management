"""
Servicio de gestión de movimientos (préstamos y devoluciones).

Este módulo contiene la lógica de negocio para la gestión de préstamos
y devoluciones de libros en la biblioteca, incluyendo validaciones
y control de inventario automático.
"""

from models.movements import Movement
from datetime import datetime as dt
from services.books_service import BooksService
from services.persistencia_service import ServicioPersistencia

class MovementsService():
    """
    Servicio para la gestión de movimientos (préstamos y devoluciones).
    
    Esta clase maneja todas las operaciones relacionadas con préstamos y devoluciones
    de libros, incluyendo validaciones de disponibilidad, control de inventario
    automático y seguimiento del estado de los préstamos.
    
    Attributes:
        movements (list[Movement]): Lista de movimientos registrados en el sistema.
        books_service (BooksService): Referencia al servicio de libros para control de inventario.
    """
    
    def __init__(self, books_service, graph_service=None):
        """
        Inicializa el servicio de movimientos cargando desde archivo JSON.
        
        Args:
            books_service (BooksService): Instancia del servicio de libros para integración.
            graph_service (GraphService, optional): Instancia del servicio de grafos para registrar préstamos.
        """
        self.persistencia = ServicioPersistencia()
        self.movements = []
        self.books_service = books_service
        self.graph_service = graph_service
        self._cargar_movimientos()
    
    def _cargar_movimientos(self):
        """
        Carga movimientos desde archivo JSON y los convierte a objetos Movement.
        También registra los préstamos en el grafo si está disponible.
        """
        datos_movimientos = self.persistencia.cargar_movimientos()
        self.movements = []
        
        for datos in datos_movimientos:
            movimiento = Movement(
                datos['id'],
                datos['book_id'],
                datos['student_name'],
                datos['student_identification'],
                datos['loan_date'],
                datos['return_date'],
                datos['returned'],
                datos['created_at'],
                datos['updated_at']
            )
            self.movements.append(movimiento)
            
            # Registrar préstamo en el grafo si está disponible y no está devuelto
            if self.graph_service and not datos['returned']:
                self.graph_service.registrar_prestamo(
                    datos['student_identification'],
                    datos['book_id']
                )
    
    def _guardar_movimientos(self):
        """
        Guarda la lista actual de movimientos en archivo JSON.
        """
        self.persistencia.guardar_movimientos(self.movements)
    
    def add_movement(self, book_id, student_name, student_identification, return_date):
        """
        Crea un nuevo préstamo de libro.
        
        Realiza múltiples validaciones antes de crear el préstamo:
        - Valida los campos del movimiento (nombre, identificación, fecha)
        - Verifica que el libro exista
        - Verifica que haya ejemplares disponibles
        - Verifica que el libro no esté ya prestado al mismo estudiante
        - Disminuye automáticamente la cantidad disponible del libro
        
        Args:
            book_id (int): ID del libro a prestar.
            student_name (str): Nombre del estudiante.
            student_identification (str): Número de identificación del estudiante.
            return_date (str): Fecha programada de devolución.
            
        Returns:
            Movement or None: El objeto movimiento creado si fue exitoso, None si falló alguna validación.
        """
        id = len(self.movements) + 1
        if not self.check_movement_fields(student_name, student_identification, return_date):
            return None
        
        book = self.books_service.get_book_by_id(book_id)
        if book is None:
            print("❌❌❌ Libro no encontrado ❌❌❌")
            return None
        if book.quantity == 0:
            print("❌❌❌ El libro está agotado ❌❌❌")
            return None
        
        if self.check_movement_by_book_id(book_id, student_identification):
            print("❌❌❌ El libro ya está prestado ❌❌❌")
            return None
        
        movement = Movement(id, book_id, student_name, student_identification, dt.today().date(), return_date, False, dt.today().date(), dt.today().date())
        if movement:
            uptaded_book = self.books_service.decrement_quantity(book_id)
            if uptaded_book:
                print(f"Nuevo stock del libro {book_id} - {uptaded_book.title}: {uptaded_book.quantity}")
            else:
                print(f"Error al disminuir la cantidad del libro {book_id}")
                return None
        self.movements.append(movement)
        
        # Registrar préstamo en el grafo si está disponible
        if self.graph_service:
            self.graph_service.registrar_prestamo(student_identification, book_id)
        
        self._guardar_movimientos()
        return movement
    
    def return_movement(self, id):
        """
        Marca un libro como devuelto.
        
        Busca el movimiento por ID y:
        - Verifica que el libro esté efectivamente prestado
        - Marca el movimiento como devuelto
        - Actualiza la fecha de devolución a la fecha actual
        - Incrementa automáticamente la cantidad disponible del libro
        
        Args:
            id (int): ID del movimiento a procesar.
            
        Returns:
            Movement or None: El objeto movimiento actualizado si fue exitoso, None si no se encontró o falló.
        """
        for movement in self.movements:
            if movement.id == id:
                if not self.check_movement_by_book_id(movement.book_id, movement.student_identification):
                    print("❌❌❌ El libro no está prestado ❌❌❌")
                    return None
                movement.returned = True
                movement.return_date = dt.today().date()
                
                uptaded_book = self.books_service.increment_quantity(movement.book_id)
                if uptaded_book:
                    print(f"Nuevo stock del libro {movement.book_id} - {uptaded_book.title}: {uptaded_book.quantity}")
                else:
                    print(f"Error al incrementar la cantidad del libro {movement.book_id}")
                    return None
                
                self._guardar_movimientos()
                return movement
        print("❌❌❌ Movimiento no encontrado ❌❌❌")
        return None
    
    def get_all_movements(self):
        """
        Obtiene todos los movimientos registrados en el sistema.
        
        Returns:
            list[Movement]: Lista de todos los movimientos (préstamos y devoluciones).
        """
        return self.movements
    
    def check_movement_fields(self, student_name, student_identification, return_date):
        """
        Valida los campos requeridos para crear un movimiento.
        
        Verifica que:
        - El nombre del estudiante no esté vacío
        - La identificación del estudiante no esté vacía
        - La identificación tenga exactamente 10 caracteres
        - La fecha de devolución no esté vacía
        
        Args:
            student_name (str): Nombre del estudiante.
            student_identification (str): Número de identificación del estudiante.
            return_date (str): Fecha programada de devolución.
            
        Returns:
            bool: True si todos los campos son válidos, False en caso contrario.
        """
        if student_name == "":
            print("❌❌❌ El nombre del estudiante es requerido ❌❌❌")
            return False
        if student_identification == "":
            print("❌❌❌ La identificación del estudiante es requerida ❌❌❌")
            return False
        if len(student_identification) != 10:
            print("❌❌❌ La identificación del estudiante debe tener 10 caracteres ❌❌❌")
            return False
        if return_date == "":
            print("❌❌❌ La fecha de devolución es requerida ❌❌❌")
            return False
        return True
    
    def check_movement_by_book_id(self, book_id, student_identification):
        """
        Verifica si un libro específico está prestado a un estudiante específico.
        
        Busca movimientos activos (no devueltos) que coincidan con:
        - El ID del libro
        - La identificación del estudiante
        - Estado de no devuelto
        
        Args:
            book_id (int): ID del libro a verificar.
            student_identification (str): Número de identificación del estudiante.
            
        Returns:
            bool: True si el libro está prestado al estudiante, False en caso contrario.
        """
        print(f"Verificando si el libro {book_id} está prestado...")
        for movement in self.movements:
            print(f"Movimiento {movement.id} - ID del Libro: {movement.book_id} - Devuelto: {movement.returned}")
            if movement.book_id == book_id and not movement.returned and movement.student_identification == student_identification:
                print(f"El libro {book_id} está prestado")
                return True
        return False