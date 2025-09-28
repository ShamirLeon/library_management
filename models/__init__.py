"""
Módulo de modelos de datos.

Este paquete contiene todos los modelos de datos utilizados en el sistema
de gestión de biblioteca. Cada modelo representa una entidad del dominio
de negocio y encapsula sus propiedades y comportamientos.

Modelos incluidos:
- User: Representa un usuario del sistema
- Book: Representa un libro en el catálogo
- Movement: Representa un préstamo o devolución

Autor: [Tu nombre]
Fecha: [Fecha actual]
"""

from .users import User
from .books import Book
from .movements import Movement

__all__ = ['User', 'Book', 'Movement']
