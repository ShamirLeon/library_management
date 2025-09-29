# 📚 Sistema de Gestión de Biblioteca

Un sistema completo de gestión de biblioteca desarrollado en Python que permite administrar usuarios, libros y préstamos de manera eficiente.

# Integrantes del equipo

- Shamir León
- Carlos Rodríguez

# Estructuras de datos (William Ruiz)

## 🚀 Características Principales

### 👥 **Gestión de Usuarios**
- ✅ Autenticación segura con email y contraseña
- ✅ Registro de nuevos usuarios con validaciones
- ✅ Listado completo de usuarios registrados
- ✅ Eliminación de usuarios del sistema
- ✅ Validación de contraseñas (mínimo 6 caracteres)
- ✅ Validación de formato de email

### 📖 **Gestión de Libros**
- ✅ Catálogo completo de libros
- ✅ Agregar nuevos libros con información bibliográfica
- ✅ Control de inventario automático
- ✅ Validación de ISBN (10 caracteres)
- ✅ Eliminación de libros del catálogo
- ✅ Búsqueda por ID

### 🔄 **Gestión de Préstamos**
- ✅ Sistema de préstamos y devoluciones
- ✅ Validación de disponibilidad de libros
- ✅ Control automático de stock
- ✅ Seguimiento de préstamos activos
- ✅ Validación de datos del estudiante
- ✅ Prevención de préstamos duplicados

## 🏗️ Arquitectura del Sistema

### **Estructura de Módulos**

```
📁 library_management/
├── 📄 main.py                 # Interfaz principal y menús del sistema
├── 📁 models/                 # Modelos de datos
│   ├── 📄 __init__.py        # Configuración del paquete de modelos
│   ├── 📄 users.py           # Modelo de Usuario
│   ├── 📄 books.py           # Modelo de Libro
│   └── 📄 movements.py       # Modelo de Movimiento (Préstamo)
└── 📁 services/              # Lógica de negocio
    ├── 📄 __init__.py        # Configuración del paquete de servicios
    ├── 📄 users_service.py   # Servicio de gestión de usuarios
    ├── 📄 books_service.py   # Servicio de gestión de libros
    └── 📄 movements_service.py # Servicio de gestión de préstamos
```

## 🎮 Guía de Uso

### **Inicio del Sistema**
1. Ejecuta `python main.py`
2. Selecciona la opción "1. Login"
3. Usa las credenciales predeterminadas (ver sección de datos de prueba)

### **Menú Principal**
- **1. Login**: Iniciar sesión en el sistema
- **2. Exit**: Salir de la aplicación

### **Menú de Administración**
Una vez autenticado, tendrás acceso a:

#### **👥 Gestión de Usuarios**
- **1. Add User**: Agregar nuevo usuario
- **2. Get All Users**: Ver todos los usuarios
- **3. Delete User**: Eliminar usuario

#### **📖 Gestión de Libros**
- **4. Add Book**: Agregar nuevo libro
- **5. Get All Books**: Ver catálogo completo
- **6. Delete Book**: Eliminar libro

#### **🔄 Gestión de Préstamos**
- **7. Borrow a book**: Realizar préstamo
- **8. Get All Movements**: Ver todos los préstamos
- **9. Return Book**: Devolver libro

## 🧪 Datos de Prueba Predeterminados

### **👤 Usuario Administrador**
Para acceder al sistema, usa estas credenciales:
```
📧 Email: admin@example.com
🔑 Password: 123456
```

### **📚 Libros de Ejemplo**
El sistema incluye 3 libros predeterminados:

| ID | Título | Autor | ISBN | Cantidad |
|----|--------|-------|------|----------|
| 1 | Cien años de soledad | Gabriel García Márquez | 9780307474728 | 5 |
| 2 | 1984 | George Orwell | 9780451524935 | 4 |
| 3 | Don Quijote de la Mancha | Miguel de Cervantes | 9788420412145 | 3 |

### **🧪 Casos de Prueba**

1. **Prueba de Autenticación**:
   - Login con credenciales válidas
   - Intentar login con credenciales incorrectas

2. **Prueba de Gestión de Libros**:
   - Agregar un nuevo libro
   - Intentar agregar libro con ISBN inválido
   - Ver catálogo completo

3. **Prueba de Préstamos**:
   - Realizar préstamo de un libro
   - Verificar que el stock disminuye
   - Intentar prestar libro sin stock
   - Devolver libro y verificar que el stock aumenta

## 🔧 Características Técnicas

### **Validaciones Implementadas**
- ✅ Contraseñas mínimo 6 caracteres
- ✅ Email con formato válido (@)
- ✅ ISBN de exactamente 10 caracteres
- ✅ Cantidad de libros mayor a 0
- ✅ Identificación de estudiante de 10 caracteres
- ✅ Campos obligatorios no vacíos

### **Control de Inventario**
- ✅ Decremento automático al prestar
- ✅ Incremento automático al devolver
- ✅ Verificación de stock disponible
- ✅ Prevención de préstamos sin stock

### **Persistencia de Datos**
- 💾 **En Memoria**: Los datos se mantienen durante la ejecución
- 🔄 **Reinicio**: Los datos se resetean al reiniciar la aplicación
- 📊 **Estado**: Información de auditoría (fechas de creación/actualización)
