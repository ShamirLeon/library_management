"""
Módulo de servicios de negocio.

Este paquete contiene todos los servicios que implementan la lógica de negocio
del sistema de gestión de biblioteca. Los servicios actúan como intermediarios
entre la interfaz de usuario y los modelos de datos, implementando las reglas
de negocio y validaciones necesarias.

Servicios incluidos:
- UsersService: Gestión de usuarios y autenticación
- BooksService: Gestión del catálogo de libros
- MovementsService: Gestión de préstamos y devoluciones

Autor: [Tu nombre]
Fecha: [Fecha actual]
"""

from .users_service import UsersService
from .books_service import BooksService
from .movements_service import MovementsService

__all__ = ['UsersService', 'BooksService', 'MovementsService']
