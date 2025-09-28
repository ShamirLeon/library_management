# 📚 Sistema de Gestión de Biblioteca

Un sistema completo de gestión de biblioteca desarrollado en Python que permite administrar usuarios, libros y préstamos de manera eficiente.

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

### **Patrón de Diseño**
- **Modelo-Vista-Controlador (MVC)**: Separación clara entre datos, lógica y presentación
- **Servicios de Negocio**: Lógica encapsulada en servicios especializados
- **Validaciones Robustas**: Verificación de datos en múltiples capas

## 🛠️ Requisitos del Sistema

### **Requisitos Mínimos**
- **Python**: 3.7 o superior
- **Sistema Operativo**: Windows, macOS, o Linux
- **Memoria RAM**: Mínimo 512 MB
- **Espacio en Disco**: 50 MB

### **Dependencias**
El proyecto utiliza únicamente librerías estándar de Python:
- `datetime` - Para manejo de fechas
- `input()` - Para entrada de usuario (interfaz de consola)

## 🚀 Instalación y Configuración

### **1. Clonar el Repositorio**
```bash
git clone <url-del-repositorio>
cd library_management
```

### **2. Verificar Python**
```bash
python --version
# Debe mostrar Python 3.7 o superior
```

### **3. Ejecutar el Sistema**
```bash
python main.py
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
| 1 | Book 1 | Author 1 | 1234567890 | 3 |
| 2 | Book 2 | Author 2 | 1234567890 | 10 |
| 3 | Book 3 | Author 3 | 1234567890 | 10 |

### **🧪 Casos de Prueba Sugeridos**

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

## 🐛 Solución de Problemas

### **Error: "Python no reconocido"**
```bash
# Windows
python --version
# Si no funciona, intenta:
py --version

# Linux/macOS
python3 --version
```

### **Error de Importación**
```bash
# Asegúrate de estar en el directorio correcto
cd /ruta/al/proyecto/library_management
python main.py
```

### **Error de Permisos**
```bash
# En Linux/macOS, si es necesario:
chmod +x main.py
```
---

**¡Disfruta usando el Sistema de Gestión de Biblioteca! 📚✨**
