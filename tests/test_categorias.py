"""
Tests unitarios para los nodos de categorías.

Este módulo contiene pruebas para verificar el correcto funcionamiento
de la clase NodoCategoria y sus métodos principales.
"""

import unittest
import sys
import os

# Agregar el directorio raíz al path para importar los módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.categorias import NodoCategoria


class TestNodoCategoria(unittest.TestCase):
    """
    Suite de tests para la clase NodoCategoria.
    
    Prueba las funcionalidades principales de los nodos de categorías:
    - Creación e inicialización
    - Relaciones padre-hijo
    - Gestión de libros
    - Búsqueda de categorías
    - Obtención de rutas
    """
    
    def setUp(self):
        """
        Configuración inicial para cada test.
        Crea una estructura de nodos de prueba.
        """
        # Crear nodo raíz
        self.raiz = NodoCategoria("Biblioteca", "Biblioteca principal")
        
        # Crear categorías hijas
        self.ficcion = NodoCategoria("Ficción", "Libros de ficción")
        self.no_ficcion = NodoCategoria("No Ficción", "Libros de no ficción")
        
        # Crear subcategorías
        self.novela = NodoCategoria("Novela", "Novelas")
        self.ciencia_ficcion = NodoCategoria("Ciencia Ficción", "Ciencia ficción")
        self.historia = NodoCategoria("Historia", "Libros de historia")
        
        # Construir la estructura del árbol
        self.raiz.agregar_hijo(self.ficcion)
        self.raiz.agregar_hijo(self.no_ficcion)
        self.ficcion.agregar_hijo(self.novela)
        self.ficcion.agregar_hijo(self.ciencia_ficcion)
        self.no_ficcion.agregar_hijo(self.historia)
    
    def test_creacion_nodo_y_relacion_padre_hijo(self):
        """
        Test 1: Verifica la creación de nodos y la relación padre-hijo.
        
        Este test verifica que:
        - Los nodos se crean correctamente con nombre y descripción
        - La relación padre-hijo se establece correctamente
        - Los hijos se agregan a la lista de hijos del padre
        - El atributo padre se establece en el nodo hijo
        """
        # Verificar que el nodo raíz se creó correctamente
        self.assertEqual(self.raiz.nombre, "Biblioteca")
        self.assertEqual(self.raiz.descripcion, "Biblioteca principal")
        self.assertIsNone(self.raiz.padre)
        self.assertEqual(len(self.raiz.hijos), 2)
        
        # Verificar que los hijos se agregaron correctamente
        self.assertIn(self.ficcion, self.raiz.hijos)
        self.assertIn(self.no_ficcion, self.raiz.hijos)
        
        # Verificar que la relación padre se estableció en los hijos
        self.assertEqual(self.ficcion.padre, self.raiz)
        self.assertEqual(self.no_ficcion.padre, self.raiz)
        
        # Verificar subcategorías
        self.assertEqual(len(self.ficcion.hijos), 2)
        self.assertIn(self.novela, self.ficcion.hijos)
        self.assertIn(self.ciencia_ficcion, self.ficcion.hijos)
        self.assertEqual(self.novela.padre, self.ficcion)
        self.assertEqual(self.ciencia_ficcion.padre, self.ficcion)
        
        # Verificar que la ruta se construye correctamente
        ruta_novela = self.novela.obtener_ruta()
        self.assertEqual(ruta_novela, ["Biblioteca", "Ficción", "Novela"])
        
        ruta_historia = self.historia.obtener_ruta()
        self.assertEqual(ruta_historia, ["Biblioteca", "No Ficción", "Historia"])
    
    def test_gestion_libros_en_nodo(self):
        """
        Test 2: Verifica la gestión de libros en los nodos.
        
        Este test verifica que:
        - Se pueden agregar libros a un nodo
        - No se pueden agregar libros duplicados
        - Se pueden remover libros de un nodo
        - Se cuenta correctamente el número de libros directos
        - Se cuenta correctamente el número total de libros incluyendo subcategorías
        - Los libros de las subcategorías se incluyen en el conteo total
        """
        # Agregar libros a la categoría Novela
        self.novela.agregar_libro(1)
        self.novela.agregar_libro(2)
        self.novela.agregar_libro(3)
        
        # Verificar que los libros se agregaron
        self.assertEqual(len(self.novela.libros), 3)
        self.assertIn(1, self.novela.libros)
        self.assertIn(2, self.novela.libros)
        self.assertIn(3, self.novela.libros)
        
        # Verificar que no se pueden agregar libros duplicados
        self.novela.agregar_libro(1)
        self.assertEqual(len(self.novela.libros), 3)
        
        # Verificar conteo de libros directos
        self.assertEqual(self.novela.contar_libros_directos(), 3)
        
        # Agregar libros a Ciencia Ficción
        self.ciencia_ficcion.agregar_libro(4)
        self.ciencia_ficcion.agregar_libro(5)
        
        # Verificar conteo de libros directos en Ciencia Ficción
        self.assertEqual(self.ciencia_ficcion.contar_libros_directos(), 2)
        
        # Verificar conteo total en Ficción (debe incluir libros de subcategorías)
        libros_totales_ficcion = self.ficcion.contar_libros_totales()
        self.assertEqual(libros_totales_ficcion, 5)  # 3 de Novela + 2 de Ciencia Ficción
        
        # Verificar que obtener_todos_los_libros funciona correctamente
        todos_libros_ficcion = self.ficcion.obtener_todos_los_libros()
        self.assertEqual(len(todos_libros_ficcion), 5)
        self.assertIn(1, todos_libros_ficcion)
        self.assertIn(2, todos_libros_ficcion)
        self.assertIn(3, todos_libros_ficcion)
        self.assertIn(4, todos_libros_ficcion)
        self.assertIn(5, todos_libros_ficcion)
        
        # Agregar libros directamente a Ficción
        self.ficcion.agregar_libro(10)
        self.assertEqual(self.ficcion.contar_libros_directos(), 1)
        self.assertEqual(self.ficcion.contar_libros_totales(), 6)  # 1 directo + 5 de subcategorías
        
        # Remover un libro de Novela
        resultado = self.novela.remover_libro(2)
        self.assertTrue(resultado)
        self.assertEqual(len(self.novela.libros), 2)
        self.assertNotIn(2, self.novela.libros)
        
        # Intentar remover un libro que no existe
        resultado = self.novela.remover_libro(99)
        self.assertFalse(resultado)
        self.assertEqual(len(self.novela.libros), 2)
        
        # Verificar que el conteo total se actualizó después de remover
        self.assertEqual(self.ficcion.contar_libros_totales(), 5)  # 1 directo + 4 de subcategorías


if __name__ == '__main__':
    unittest.main()

