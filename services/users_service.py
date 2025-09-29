"""
Servicio de gestión de usuarios.

Este módulo contiene la lógica de negocio para la gestión de usuarios
del sistema de biblioteca, incluyendo operaciones CRUD y autenticación.
"""

from datetime import datetime as dt
from models.users import User

class UsersService():
    """
    Servicio para la gestión de usuarios del sistema.
    
    Esta clase maneja todas las operaciones relacionadas con usuarios,
    incluyendo creación, autenticación, consulta y eliminación de usuarios.
    Mantiene una lista en memoria de usuarios registrados.
    
    Attributes:
        users (list[User]): Lista de usuarios registrados en el sistema.
    """
    
    def __init__(self):
        """
        Inicializa el servicio de usuarios con un usuario administrador por defecto.
        
        Crea un usuario administrador predeterminado con las credenciales:
        - Email: admin@example.com
        - Password: 123456
        """
        self.users = [User(1, "Admin", "admin@example.com", "123456", dt.today().date(), dt.today().date())]
    
    def add_user(self, email, password, name):
        """
        Agrega un nuevo usuario al sistema.
        
        Valida los datos del usuario antes de crearlo:
        - La contraseña debe tener al menos 6 caracteres
        - El email debe tener exactamente un símbolo @
        - El nombre, email y contraseña se limpian de espacios en blanco
        
        Args:
            email (str): Dirección de correo electrónico del usuario.
            password (str): Contraseña del usuario (mínimo 6 caracteres).
            name (str): Nombre completo del usuario.
            
        Returns:
            User or None: El objeto usuario creado si fue exitoso, None si falló la validación.
        """
        id = len(self.users) + 1
        if len(password) < 6:
            print('    ')
            print("❌❌❌ La contraseña debe tener al menos 6 caracteres ❌❌❌")
            print('    ')
            return None
        if email.count("@") != 1:
            print('    ')
            print("❌❌❌ Email inválido ❌❌❌")
            print('    ')
            return None
        
        user = User(id, name.strip(), email.strip(), password.strip(), dt.today().date(), dt.today().date())
        self.users.append(user)
        return user

    def get_all_users(self):
        """
        Obtiene todos los usuarios registrados en el sistema.
        
        Returns:
            list[User]: Lista de todos los usuarios en el sistema.
        """
        return self.users
    
    def delete_user(self, id):
        """
        Elimina un usuario del sistema por su ID.
        
        Args:
            id (int): Identificador único del usuario a eliminar.
            
        Returns:
            User or None: El objeto usuario eliminado si fue encontrado, None si no existe.
        """
        print(f"Eliminando usuario {id}...")
        for user in self.users:
            if user.id == id:
                self.users.remove(user)
                return user
        return None
    
    def login(self, email, password):
        """
        Autentica a un usuario con sus credenciales.
        
        Busca un usuario que coincida con el email y contraseña proporcionados.
        
        Args:
            email (str): Dirección de correo electrónico del usuario.
            password (str): Contraseña del usuario.
            
        Returns:
            User or None: El objeto usuario si las credenciales son válidas, None en caso contrario.
        """
        for user in self.users:
            if user.email == email and user.password == password:
                return user
        return None