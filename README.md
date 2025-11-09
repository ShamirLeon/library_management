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
│   ├── 📄 movements.py       # Modelo de Movimiento (Préstamo)
│   └── 📄 categorias.py      # Modelo de Árbol de Categorías
├── 📁 services/              # Lógica de negocio
│   ├── 📄 __init__.py        # Configuración del paquete de servicios
│   ├── 📄 users_service.py   # Servicio de gestión de usuarios
│   ├── 📄 books_service.py   # Servicio de gestión de libros
│   ├── 📄 movements_service.py # Servicio de gestión de préstamos
│   ├── 📄 categorias_service.py # Servicio de gestión de categorías
│   └── 📄 persistencia_service.py # Servicio de persistencia de datos
└── 📁 tests/                 # Tests unitarios
    ├── 📄 __init__.py        # Inicialización del paquete de tests
    └── 📄 test_categorias.py # Tests para nodos de categorías
```

## 🎮 Guía de Uso

### **Inicio del Sistema**
1. Ejecuta `python main.py`
2. Selecciona la opción "1. Login"
3. Usa las credenciales predeterminadas (ver sección de datos de prueba)

### **Menú Principal**
- **1. Iniciar sesión**: Iniciar sesión en el sistema
- **2. Salir**: Salir de la aplicación

### **Menú de Administración**
Una vez autenticado, tendrás acceso a:

#### **👥 Gestión de Usuarios**
- **1. Añadir usuario**: Agregar nuevo usuario
- **2. Obtener todos los usuarios**: Ver todos los usuarios
- **3. Eliminar usuario**: Eliminar usuario

#### **📖 Gestión de Libros**
- **4. Añadir libro**: Agregar nuevo libro
- **5. Obtener todos los usuarios**: Ver catálogo completo
- **6. Eliminar libro**: Eliminar libro

#### **🔄 Gestión de Préstamos**
- **7. Prestar un libro**: Realizar préstamo
- **8. Obtener todos los movimientos**: Ver todos los préstamos
- **9. Devolver un libro**: Devolver libro

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
- Se implementó persistencia de datos para todos los servicios disponibles en la aplicación. Se almacenan en la carpeta `datos/` mediante archivos JSON.

## 🧪 Tests

### **Estructura de Tests**

El proyecto incluye una suite de tests unitarios ubicada en la carpeta `tests/`. Los tests utilizan el framework `unittest` de Python para verificar el correcto funcionamiento de los componentes del sistema.

### **Ejecutar Tests**

Para ejecutar los tests, puedes usar cualquiera de los siguientes comandos:

```bash
# Opción 1: Ejecutar todos los tests usando unittest
python3 -m unittest discover tests -v

# Opción 2: Ejecutar un archivo de test específico
python3 -m unittest tests.test_categorias -v

# Opción 3: Ejecutar el archivo de test directamente
python3 tests/test_categorias.py
```

### **Tests Disponibles**

#### **Tests de Nodos de Categorías** (`test_categorias.py`)

Los tests para los nodos de categorías verifican las funcionalidades principales de la clase `NodoCategoria`:

1. **Test de Creación y Relación Padre-Hijo** (`test_creacion_nodo_y_relacion_padre_hijo`)
   - ✅ Verifica la creación correcta de nodos con nombre y descripción
   - ✅ Valida la relación padre-hijo entre nodos
   - ✅ Comprueba que los hijos se agregan correctamente a la lista del padre
   - ✅ Verifica que el atributo padre se establece en los nodos hijos
   - ✅ Valida la construcción correcta de rutas en el árbol

2. **Test de Gestión de Libros** (`test_gestion_libros_en_nodo`)
   - ✅ Verifica la adición de libros a nodos
   - ✅ Valida que no se pueden agregar libros duplicados
   - ✅ Comprueba la eliminación correcta de libros
   - ✅ Verifica el conteo de libros directos
   - ✅ Valida el conteo total de libros incluyendo subcategorías
   - ✅ Comprueba que los libros de subcategorías se incluyen en el conteo total

### **Cobertura de Tests**

Los tests actuales cubren:
- ✅ Inicialización de nodos de categorías
- ✅ Establecimiento de relaciones jerárquicas
- ✅ Gestión completa de libros (agregar, remover, contar)
- ✅ Búsqueda de categorías en el árbol
- ✅ Obtención de rutas completas
- ✅ Conteo de libros directos y totales

### **Estructura de Carpetas de Tests**

```
📁 tests/
├── 📄 __init__.py          # Inicialización del paquete de tests
└── 📄 test_categorias.py   # Tests para nodos de categorías
```

#  Documentación del Árbol de Categorías implementado 

## Características Principales

### Funcionalidades Clave

1. **Estructura Jerárquica**: Organización en árbol con categorías padre e hijos
2. **Clasificación Automática**: Sugerencias inteligentes basadas en título, autor y género
3. **Búsqueda Avanzada**: Múltiples formas de buscar y filtrar libros
4. **Estadísticas Detalladas**: Métricas completas del sistema de categorización
5. **Gestión Dinámica**: Crear, modificar y eliminar categorías fácilmente

### Estadísticas Disponibles

#### Estadísticas Generales:
- Total de categorías en el sistema
- Categorías con libros vs. categorías vacías
- Porcentaje de utilización del sistema
- Categoría más popular
- Total de libros categorizados

#### Estadísticas por Categoría:
- Libros directos en la categoría
- Libros totales (incluyendo subcategorías)  
- Número de subcategorías
- Ruta completa en la jerarquía
- Descripción de la categoría

## Ejemplos de Uso

### Categorizar un Libro Nuevo

Al agregar un libro, el sistema automáticamente:
1. Sugiere categorías
2. Permite seleccionar una categoría sugerida
3. Categoriza el libro inmediatamente


## Ventajas del Sistema

### Beneficios de Implementación

1. **Organización Intuitiva**: Estructura familiar tipo explorador de archivos
2. **Escalabilidad**: Fácil agregar nuevas categorías sin límites de profundidad
3. **Búsqueda Eficiente**: Múltiples métodos de búsqueda y filtrado
4. **Flexibilidad**: Libros pueden pertenecer a múltiples categorías
5. **Mantenimiento Sencillo**: Operaciones CRUD completas


## Arquitectura Técnica

### Diseño del Árbol

- **Estructura**: Árbol n-ario donde cada nodo puede tener múltiples hijos
- **Navegación**: Búsqueda en profundidad (DFS) para recorridos
- **Almacenamiento**: En memoria con referencias padre-hijo bidireccionales
- **Eficiencia**: O(n) para búsquedas, O(1) para inserciones

## ¿Por qué escogimos este tipo de árbol?

- Escogimos este árbol ya que cumple con nuestros requisitos de una búsqueda eficiente en memoria y tiempo, nos permite tener complejidades algorítmicas ideales en casos de búsqueda e inserción.