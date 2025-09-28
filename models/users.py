class User():
    """
    Modelo de datos para representar un usuario del sistema.
    
    Esta clase encapsula toda la información relacionada con un usuario
    del sistema de gestión de biblioteca, incluyendo sus datos personales
    y metadatos de auditoría.
    
    Attributes:
        id (int): Identificador único del usuario.
        name (str): Nombre completo del usuario.
        email (str): Dirección de correo electrónico del usuario (debe ser única).
        password (str): Contraseña del usuario (almacenada en texto plano).
        created_at (date): Fecha de creación del registro.
        updated_at (date): Fecha de última actualización del registro.
    """
    
    def __init__(self, id, name, email, password, created_at, updated_at):
        """
        Inicializa una nueva instancia de User.
        
        Args:
            id (int): Identificador único del usuario.
            name (str): Nombre completo del usuario.
            email (str): Dirección de correo electrónico del usuario.
            password (str): Contraseña del usuario.
            created_at (date): Fecha de creación del registro.
            updated_at (date): Fecha de última actualización del registro.
        """
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.created_at = created_at
        self.updated_at = updated_at
    
    def __str__(self):
        """
        Retorna una representación en cadena del objeto User.
        
        Returns:
            str: Representación textual del usuario con todos sus atributos.
        """
        return f"User(id={self.id}, name={self.name}, email={self.email}, password={self.password}, created_at={self.created_at}, updated_at={self.updated_at})"