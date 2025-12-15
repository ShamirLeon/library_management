"""
Tests unitarios para el servicio de grafos de recomendación.

Este módulo contiene pruebas para verificar el correcto funcionamiento
del sistema de grafos para recomendación de libros, incluyendo:
- Grafo bipartito Usuario-Libro
- Grafo Usuario-Usuario ponderado
- Sistema de recomendaciones
- Análisis de popularidad y relaciones
"""

import unittest
import sys
import os

# Agregar el directorio raíz al path para importar los módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.graph_service import GraphService
from models.books import Book
from datetime import date


class TestGraphService(unittest.TestCase):
    """
    Suite de tests para la clase GraphService.
    
    Prueba las funcionalidades principales del sistema de grafos:
    - Registro de préstamos
    - Grafo bipartito Usuario-Libro
    - Grafo Usuario-Usuario ponderado
    - Recomendaciones de libros
    - Popularidad de libros
    - Usuarios similares
    - Estadísticas y análisis
    """
    
    def setUp(self):
        """
        Configuración inicial para cada test.
        Crea un servicio de grafos limpio y datos de prueba.
        """
        self.graph_service = GraphService()
        
        # Crear libros de prueba
        self.libro1 = Book(1, "Cien años de soledad", "Gabriel García Márquez", 
                          "1967-05-30", "9780307474728", 5, date.today(), date.today())
        self.libro2 = Book(2, "1984", "George Orwell", 
                          "1949-06-08", "9780451524935", 4, date.today(), date.today())
        self.libro3 = Book(3, "Don Quijote", "Miguel de Cervantes", 
                          "1605-01-16", "9788420412145", 3, date.today(), date.today())
        self.libro4 = Book(4, "El Aleph", "Jorge Luis Borges", 
                          "1949-06-01", "9788420412146", 2, date.today(), date.today())
        self.libro5 = Book(5, "Rayuela", "Julio Cortázar", 
                          "1963-06-28", "9788420412147", 1, date.today(), date.today())
        
        self.libros = [self.libro1, self.libro2, self.libro3, self.libro4, self.libro5]
    
    def test_registro_prestamo_grafo_bipartito(self):
        """
        Test 1: Verifica el registro de préstamos en el grafo bipartito.
        
        Este test verifica que:
        - Los préstamos se registran correctamente en el grafo bipartito
        - Las aristas bidireccionales se crean correctamente
        - Los usuarios pueden acceder a sus libros prestados
        - Los libros pueden acceder a sus usuarios
        """
        # Registrar préstamos
        self.graph_service.registrar_prestamo("1234567890", 1)
        self.graph_service.registrar_prestamo("1234567890", 2)
        self.graph_service.registrar_prestamo("0987654321", 1)
        self.graph_service.registrar_prestamo("0987654321", 3)
        
        # Verificar que el usuario 1234567890 tiene los libros correctos
        libros_usuario1 = self.graph_service.obtener_libros_prestados_por_usuario("1234567890")
        self.assertEqual(len(libros_usuario1), 2)
        self.assertIn(1, libros_usuario1)
        self.assertIn(2, libros_usuario1)
        
        # Verificar que el usuario 0987654321 tiene los libros correctos
        libros_usuario2 = self.graph_service.obtener_libros_prestados_por_usuario("0987654321")
        self.assertEqual(len(libros_usuario2), 2)
        self.assertIn(1, libros_usuario2)
        self.assertIn(3, libros_usuario2)
        
        # Verificar que el libro 1 tiene los usuarios correctos
        usuarios_libro1 = self.graph_service.obtener_usuarios_del_libro(1)
        self.assertEqual(len(usuarios_libro1), 2)
        self.assertIn("1234567890", usuarios_libro1)
        self.assertIn("0987654321", usuarios_libro1)
        
        # Verificar que el libro 2 solo tiene un usuario
        usuarios_libro2 = self.graph_service.obtener_usuarios_del_libro(2)
        self.assertEqual(len(usuarios_libro2), 1)
        self.assertIn("1234567890", usuarios_libro2)
    
    def test_grafo_usuario_usuario(self):
        """
        Test 2: Verifica la construcción del grafo usuario-usuario.
        
        Este test verifica que:
        - El grafo usuario-usuario se construye correctamente
        - Los pesos se calculan correctamente (cantidad de libros compartidos)
        - Las conexiones son bidireccionales
        """
        # Registrar préstamos que generen conexiones
        # Usuario 1: libros 1, 2, 3
        self.graph_service.registrar_prestamo("1111111111", 1)
        self.graph_service.registrar_prestamo("1111111111", 2)
        self.graph_service.registrar_prestamo("1111111111", 3)
        
        # Usuario 2: libros 1, 2 (2 libros en común con usuario 1)
        self.graph_service.registrar_prestamo("2222222222", 1)
        self.graph_service.registrar_prestamo("2222222222", 2)
        
        # Usuario 3: libros 1, 4 (1 libro en común con usuario 1)
        self.graph_service.registrar_prestamo("3333333333", 1)
        self.graph_service.registrar_prestamo("3333333333", 4)
        
        # Verificar conexión entre usuario 1 y 2 (2 libros compartidos)
        usuarios_similares_1 = self.graph_service.obtener_usuarios_similares("1111111111")
        self.assertGreater(len(usuarios_similares_1), 0)
        
        # Encontrar el peso de la conexión con usuario 2
        peso_usuario2 = None
        for usuario, peso in usuarios_similares_1:
            if usuario == "2222222222":
                peso_usuario2 = peso
                break
        
        self.assertIsNotNone(peso_usuario2)
        self.assertEqual(peso_usuario2, 2)  # 2 libros compartidos
        
        # Verificar conexión entre usuario 1 y 3 (1 libro compartido)
        peso_usuario3 = None
        for usuario, peso in usuarios_similares_1:
            if usuario == "3333333333":
                peso_usuario3 = peso
                break
        
        self.assertIsNotNone(peso_usuario3)
        self.assertEqual(peso_usuario3, 1)  # 1 libro compartido
    
    def test_obtener_usuarios_similares(self):
        """
        Test 3: Verifica la obtención de usuarios similares.
        
        Este test verifica que:
        - Se obtienen usuarios con gustos similares
        - Los usuarios están ordenados por peso descendente
        - Se respeta el límite de resultados
        """
        # Crear un escenario con múltiples usuarios
        self.graph_service.registrar_prestamo("A111111111", 1)
        self.graph_service.registrar_prestamo("A111111111", 2)
        self.graph_service.registrar_prestamo("A111111111", 3)
        
        self.graph_service.registrar_prestamo("B222222222", 1)
        self.graph_service.registrar_prestamo("B222222222", 2)
        self.graph_service.registrar_prestamo("B222222222", 4)
        
        self.graph_service.registrar_prestamo("C333333333", 1)
        self.graph_service.registrar_prestamo("C333333333", 5)
        
        # Obtener usuarios similares al usuario A
        similares = self.graph_service.obtener_usuarios_similares("A111111111", limite=5)
        
        # Debe haber al menos 2 usuarios similares
        self.assertGreaterEqual(len(similares), 2)
        
        # Verificar que están ordenados por peso descendente
        pesos = [peso for _, peso in similares]
        self.assertEqual(pesos, sorted(pesos, reverse=True))
        
        # El usuario B debe tener mayor peso que C (2 vs 1 libros compartidos)
        peso_B = next((p for u, p in similares if u == "B222222222"), None)
        peso_C = next((p for u, p in similares if u == "C333333333"), None)
        
        if peso_B and peso_C:
            self.assertGreater(peso_B, peso_C)
    
    def test_popularidad_libros(self):
        """
        Test 4: Verifica el cálculo de popularidad de libros.
        
        Este test verifica que:
        - La popularidad se calcula correctamente según préstamos
        - Los libros están ordenados por popularidad descendente
        - Se respeta el límite de resultados
        """
        # Registrar préstamos para crear popularidad
        # Libro 1: 3 préstamos (más popular)
        self.graph_service.registrar_prestamo("1111111111", 1)
        self.graph_service.registrar_prestamo("2222222222", 1)
        self.graph_service.registrar_prestamo("3333333333", 1)
        
        # Libro 2: 2 préstamos
        self.graph_service.registrar_prestamo("1111111111", 2)
        self.graph_service.registrar_prestamo("2222222222", 2)
        
        # Libro 3: 1 préstamo
        self.graph_service.registrar_prestamo("1111111111", 3)
        
        # Obtener popularidad
        popularidad = self.graph_service.obtener_popularidad_libros(limite=10)
        
        # Debe haber al menos 3 libros
        self.assertGreaterEqual(len(popularidad), 3)
        
        # Verificar que están ordenados por popularidad descendente
        cantidades = [cantidad for _, cantidad in popularidad]
        self.assertEqual(cantidades, sorted(cantidades, reverse=True))
        
        # El libro 1 debe ser el más popular
        libro_mas_popular = popularidad[0]
        self.assertEqual(libro_mas_popular[0], 1)
        self.assertEqual(libro_mas_popular[1], 3)
        
        # El libro 2 debe ser el segundo
        libro_segundo = popularidad[1]
        self.assertEqual(libro_segundo[0], 2)
        self.assertEqual(libro_segundo[1], 2)
    
    def test_recomendar_libros_por_historial(self):
        """
        Test 5: Verifica las recomendaciones basadas en historial.
        
        Este test verifica que:
        - Se recomiendan libros populares que el usuario no ha prestado
        - Se respeta el límite de recomendaciones
        """
        # Crear historial de préstamos
        self.graph_service.registrar_prestamo("1111111111", 1)
        self.graph_service.registrar_prestamo("1111111111", 2)
        
        # Crear popularidad para otros libros
        self.graph_service.registrar_prestamo("2222222222", 3)
        self.graph_service.registrar_prestamo("3333333333", 3)
        self.graph_service.registrar_prestamo("4444444444", 3)
        
        self.graph_service.registrar_prestamo("2222222222", 4)
        self.graph_service.registrar_prestamo("3333333333", 4)
        
        # Obtener recomendaciones
        recomendaciones = self.graph_service.recomendar_libros_por_historial(
            "1111111111", self.libros, limite=3
        )
        
        # Debe haber recomendaciones
        self.assertGreater(len(recomendaciones), 0)
        
        # Los libros recomendados no deben estar en el historial del usuario
        libros_prestados = self.graph_service.obtener_libros_prestados_por_usuario("1111111111")
        for libro in recomendaciones:
            self.assertNotIn(libro.id, libros_prestados)
    
    def test_recomendar_libros_por_usuarios_similares(self):
        """
        Test 6: Verifica las recomendaciones basadas en usuarios similares.
        
        Este test verifica que:
        - Se recomiendan libros de usuarios con gustos similares
        - Los libros recomendados no están en el historial del usuario
        - Se respeta el límite de recomendaciones
        """
        # Usuario objetivo: libros 1, 2
        self.graph_service.registrar_prestamo("TARGET_USER", 1)
        self.graph_service.registrar_prestamo("TARGET_USER", 2)
        
        # Usuario similar 1: libros 1, 2, 3 (2 libros en común)
        self.graph_service.registrar_prestamo("SIMILAR_1", 1)
        self.graph_service.registrar_prestamo("SIMILAR_1", 2)
        self.graph_service.registrar_prestamo("SIMILAR_1", 3)
        
        # Usuario similar 2: libros 1, 4 (1 libro en común)
        self.graph_service.registrar_prestamo("SIMILAR_2", 1)
        self.graph_service.registrar_prestamo("SIMILAR_2", 4)
        
        # Obtener recomendaciones
        recomendaciones = self.graph_service.recomendar_libros_por_usuarios_similares(
            "TARGET_USER", self.libros, limite=5
        )
        
        # Debe haber recomendaciones
        self.assertGreater(len(recomendaciones), 0)
        
        # Los libros recomendados no deben estar en el historial del usuario objetivo
        libros_prestados = self.graph_service.obtener_libros_prestados_por_usuario("TARGET_USER")
        for libro in recomendaciones:
            self.assertNotIn(libro.id, libros_prestados)
        
        # El libro 3 debe tener mayor prioridad que el 4 (usuario similar con más peso)
        ids_recomendados = [libro.id for libro in recomendaciones]
        if 3 in ids_recomendados and 4 in ids_recomendados:
            indice_3 = ids_recomendados.index(3)
            indice_4 = ids_recomendados.index(4)
            self.assertLess(indice_3, indice_4)
    
    def test_estadisticas_grafo(self):
        """
        Test 7: Verifica las estadísticas del grafo.
        
        Este test verifica que:
        - Se calculan correctamente las estadísticas generales
        - Los promedios se calculan correctamente
        """
        # Registrar algunos préstamos
        self.graph_service.registrar_prestamo("1111111111", 1)
        self.graph_service.registrar_prestamo("1111111111", 2)
        self.graph_service.registrar_prestamo("2222222222", 1)
        self.graph_service.registrar_prestamo("3333333333", 3)
        
        # Obtener estadísticas
        stats = self.graph_service.obtener_estadisticas_grafo()
        
        # Verificar que las estadísticas existen
        self.assertIn("total_usuarios", stats)
        self.assertIn("total_libros", stats)
        self.assertIn("total_prestamos", stats)
        self.assertIn("total_conexiones_usuario_usuario", stats)
        self.assertIn("promedio_libros_por_usuario", stats)
        self.assertIn("promedio_usuarios_por_libro", stats)
        
        # Verificar valores esperados
        self.assertEqual(stats["total_usuarios"], 3)
        self.assertEqual(stats["total_libros"], 3)
        self.assertEqual(stats["total_prestamos"], 4)
        
        # Verificar promedios
        self.assertAlmostEqual(stats["promedio_libros_por_usuario"], 4/3, places=2)
        self.assertAlmostEqual(stats["promedio_usuarios_por_libro"], 4/3, places=2)
    
    def test_relaciones_indirectas(self):
        """
        Test 8: Verifica el análisis de relaciones indirectas.
        
        Este test verifica que:
        - Se identifican correctamente las relaciones indirectas
        - Se calculan correctamente los libros indirectos
        - Se identifican usuarios relacionados
        """
        # Usuario objetivo: libros 1, 2
        self.graph_service.registrar_prestamo("OBJETIVO", 1)
        self.graph_service.registrar_prestamo("OBJETIVO", 2)
        
        # Usuario relacionado 1: libros 1, 3
        self.graph_service.registrar_prestamo("REL_1", 1)
        self.graph_service.registrar_prestamo("REL_1", 3)
        
        # Usuario relacionado 2: libros 2, 4
        self.graph_service.registrar_prestamo("REL_2", 2)
        self.graph_service.registrar_prestamo("REL_2", 4)
        
        # Obtener relaciones indirectas
        relaciones = self.graph_service.obtener_relaciones_indirectas("OBJETIVO")
        
        # Verificar estructura
        self.assertIn("libros_directos", relaciones)
        self.assertIn("libros_indirectos", relaciones)
        self.assertIn("usuarios_relacionados", relaciones)
        self.assertIn("libros_indirectos_ids", relaciones)
        
        # Verificar valores
        self.assertEqual(relaciones["libros_directos"], 2)
        self.assertEqual(relaciones["libros_indirectos"], 2)  # Libros 3 y 4
        self.assertEqual(relaciones["usuarios_relacionados"], 2)
        
        # Verificar que los libros indirectos son correctos
        self.assertIn(3, relaciones["libros_indirectos_ids"])
        self.assertIn(4, relaciones["libros_indirectos_ids"])
        self.assertNotIn(1, relaciones["libros_indirectos_ids"])
        self.assertNotIn(2, relaciones["libros_indirectos_ids"])
    
    def test_grafo_vacio(self):
        """
        Test 9: Verifica el comportamiento con grafo vacío.
        
        Este test verifica que:
        - El sistema maneja correctamente un grafo sin datos
        - No se producen errores con consultas en grafo vacío
        """
        graph_vacio = GraphService()
        
        # Obtener libros de usuario inexistente
        libros = graph_vacio.obtener_libros_prestados_por_usuario("9999999999")
        self.assertEqual(len(libros), 0)
        
        # Obtener usuarios de libro inexistente
        usuarios = graph_vacio.obtener_usuarios_del_libro(999)
        self.assertEqual(len(usuarios), 0)
        
        # Obtener usuarios similares de usuario inexistente
        similares = graph_vacio.obtener_usuarios_similares("9999999999")
        self.assertEqual(len(similares), 0)
        
        # Obtener popularidad
        popularidad = graph_vacio.obtener_popularidad_libros()
        self.assertEqual(len(popularidad), 0)
        
        # Obtener estadísticas
        stats = graph_vacio.obtener_estadisticas_grafo()
        self.assertEqual(stats["total_usuarios"], 0)
        self.assertEqual(stats["total_libros"], 0)
        self.assertEqual(stats["total_prestamos"], 0)
    
    def test_multiples_prestamos_mismo_libro(self):
        """
        Test 10: Verifica el manejo de múltiples préstamos del mismo libro.
        
        Este test verifica que:
        - Se pueden registrar múltiples préstamos del mismo libro
        - El grafo maneja correctamente préstamos duplicados
        """
        # Múltiples usuarios prestan el mismo libro
        self.graph_service.registrar_prestamo("1111111111", 1)
        self.graph_service.registrar_prestamo("2222222222", 1)
        self.graph_service.registrar_prestamo("3333333333", 1)
        self.graph_service.registrar_prestamo("4444444444", 1)
        
        # Verificar que todos los usuarios están conectados al libro
        usuarios_libro1 = self.graph_service.obtener_usuarios_del_libro(1)
        self.assertEqual(len(usuarios_libro1), 4)
        
        # Verificar que todos los usuarios están conectados entre sí
        # Cada usuario debe tener 3 conexiones (con los otros 3 usuarios)
        for usuario in ["1111111111", "2222222222", "3333333333", "4444444444"]:
            similares = self.graph_service.obtener_usuarios_similares(usuario)
            self.assertEqual(len(similares), 3)  # 3 conexiones con los otros usuarios
            
            # Todas las conexiones deben tener peso 1 (1 libro compartido)
            for _, peso in similares:
                self.assertEqual(peso, 1)


if __name__ == '__main__':
    unittest.main()

