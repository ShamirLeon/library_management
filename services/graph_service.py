"""
Servicio de gestión de grafos para recomendación de libros.

Este módulo implementa un sistema de grafos para modelar las relaciones
entre usuarios y libros, permitiendo recomendaciones basadas en:
- Historial de préstamos del usuario
- Libros prestados por usuarios con intereses similares
- Popularidad de libros
"""

from collections import defaultdict
from typing import Dict, List, Set, Tuple


class GraphService:
    """
    Servicio para la gestión de grafos de recomendación.
    
    Implementa dos tipos de grafos:
    1. Grafo bipartito Usuario-Libro: Representa préstamos directos
    2. Grafo Usuario-Usuario: Derivado del bipartito, conecta usuarios con libros en común
    
    Attributes:
        bipartite_graph (Dict[str, Set[int]]): Grafo bipartito representado como listas de adyacencia.
            Claves pueden ser identificaciones de usuarios o IDs de libros (como strings).
        user_user_graph (Dict[str, Dict[str, int]]): Grafo ponderado usuario-usuario.
            Clave: identificación de usuario, Valor: dict de {usuario: peso}
    """
    
    def __init__(self):
        """
        Inicializa el servicio de grafos con estructuras vacías.
        """
        # Grafo bipartito: {nodo: {vecinos}}
        # Los nodos pueden ser identificaciones de usuarios (str) o IDs de libros (str)
        self.bipartite_graph: Dict[str, Set[int]] = defaultdict(set)
        
        # Grafo usuario-usuario ponderado: {usuario: {usuario: peso}}
        self.user_user_graph: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
    
    def registrar_prestamo(self, student_identification: str, book_id: int):
        """
        Registra un préstamo en el grafo bipartito.
        
        Crea aristas bidireccionales entre el usuario y el libro,
        y actualiza el grafo usuario-usuario si es necesario.
        
        Args:
            student_identification (str): Identificación del estudiante.
            book_id (int): ID del libro prestado.
        """
        user_key = f"user_{student_identification}"
        book_key = f"book_{book_id}"
        
        # Agregar arista en el grafo bipartito (bidireccional)
        self.bipartite_graph[user_key].add(book_id)
        self.bipartite_graph[book_key].add(student_identification)
        
        # Actualizar grafo usuario-usuario
        self._actualizar_grafo_usuario_usuario(student_identification, book_id)
    
    def _actualizar_grafo_usuario_usuario(self, student_identification: str, book_id: int):
        """
        Actualiza el grafo usuario-usuario cuando se registra un nuevo préstamo.
        
        Busca otros usuarios que hayan prestado el mismo libro y actualiza
        los pesos de las aristas entre usuarios.
        
        Args:
            student_identification (str): Identificación del estudiante que prestó el libro.
            book_id (int): ID del libro prestado.
        """
        book_key = f"book_{book_id}"
        
        # Obtener todos los usuarios que han prestado este libro
        usuarios_del_libro = self.bipartite_graph.get(book_key, set())
        
        # Para cada usuario que también prestó este libro, incrementar el peso
        for otro_usuario in usuarios_del_libro:
            if otro_usuario != student_identification:
                # Incrementar peso bidireccionalmente
                self.user_user_graph[student_identification][otro_usuario] += 1
                self.user_user_graph[otro_usuario][student_identification] += 1
    
    def obtener_libros_prestados_por_usuario(self, student_identification: str) -> List[int]:
        """
        Obtiene la lista de libros prestados por un usuario.
        
        Args:
            student_identification (str): Identificación del estudiante.
            
        Returns:
            List[int]: Lista de IDs de libros prestados por el usuario.
        """
        user_key = f"user_{student_identification}"
        return list(self.bipartite_graph.get(user_key, set()))
    
    def obtener_usuarios_del_libro(self, book_id: int) -> List[str]:
        """
        Obtiene la lista de usuarios que han prestado un libro.
        
        Args:
            book_id (int): ID del libro.
            
        Returns:
            List[str]: Lista de identificaciones de usuarios que han prestado el libro.
        """
        book_key = f"book_{book_id}"
        return list(self.bipartite_graph.get(book_key, set()))
    
    def obtener_usuarios_similares(self, student_identification: str, limite: int = 5) -> List[Tuple[str, int]]:
        """
        Obtiene usuarios con gustos similares basado en libros compartidos.
        
        Args:
            student_identification (str): Identificación del estudiante.
            limite (int): Número máximo de usuarios similares a retornar.
            
        Returns:
            List[Tuple[str, int]]: Lista de tuplas (identificación_usuario, peso) ordenadas por peso descendente.
        """
        if student_identification not in self.user_user_graph:
            return []
        
        usuarios_similares = list(self.user_user_graph[student_identification].items())
        # Ordenar por peso descendente
        usuarios_similares.sort(key=lambda x: x[1], reverse=True)
        
        return usuarios_similares[:limite]
    
    def obtener_popularidad_libros(self, limite: int = 10) -> List[Tuple[int, int]]:
        """
        Determina la popularidad de los libros según la cantidad de préstamos.
        
        Args:
            limite (int): Número máximo de libros a retornar.
            
        Returns:
            List[Tuple[int, int]]: Lista de tuplas (book_id, cantidad_prestamos) ordenadas por popularidad descendente.
        """
        popularidad = []
        
        # Iterar sobre todos los nodos de libros en el grafo bipartito
        for nodo in self.bipartite_graph:
            if nodo.startswith("book_"):
                book_id = int(nodo.replace("book_", ""))
                cantidad_prestamos = len(self.bipartite_graph[nodo])
                popularidad.append((book_id, cantidad_prestamos))
        
        # Ordenar por cantidad de préstamos descendente
        popularidad.sort(key=lambda x: x[1], reverse=True)
        
        return popularidad[:limite]
    
    def recomendar_libros_por_historial(self, student_identification: str, 
                                       libros_existentes: List, 
                                       limite: int = 5) -> List:
        """
        Recomienda libros basado en el historial de préstamos del usuario.
        
        Esta es una recomendación simple que retorna libros similares a los ya prestados.
        Por ahora, retorna los libros más populares que el usuario no ha prestado.
        
        Args:
            student_identification (str): Identificación del estudiante.
            libros_existentes (List): Lista de objetos Book disponibles.
            limite (int): Número máximo de recomendaciones.
            
        Returns:
            List: Lista de objetos Book recomendados.
        """
        libros_prestados = set(self.obtener_libros_prestados_por_usuario(student_identification))
        
        # Obtener libros populares que el usuario no ha prestado
        popularidad = self.obtener_popularidad_libros(limite * 2)
        
        recomendaciones = []
        for book_id, _ in popularidad:
            if book_id not in libros_prestados:
                # Buscar el objeto Book correspondiente
                for libro in libros_existentes:
                    if libro.id == book_id:
                        recomendaciones.append(libro)
                        break
                if len(recomendaciones) >= limite:
                    break
        
        return recomendaciones
    
    def recomendar_libros_por_usuarios_similares(self, student_identification: str,
                                                 libros_existentes: List,
                                                 limite: int = 5) -> List:
        """
        Recomienda libros basado en lo que han leído usuarios con gustos similares.
        
        Implementa el algoritmo: "Usuarios con gustos similares también leyeron..."
        
        Args:
            student_identification (str): Identificación del estudiante.
            libros_existentes (List): Lista de objetos Book disponibles.
            limite (int): Número máximo de recomendaciones.
            
        Returns:
            List: Lista de objetos Book recomendados.
        """
        libros_prestados = set(self.obtener_libros_prestados_por_usuario(student_identification))
        usuarios_similares = self.obtener_usuarios_similares(student_identification, limite=10)
        
        # Contar libros prestados por usuarios similares
        recomendaciones_contador: Dict[int, int] = defaultdict(int)
        
        for usuario_similar, peso in usuarios_similares:
            libros_del_similar = self.obtener_libros_prestados_por_usuario(usuario_similar)
            for book_id in libros_del_similar:
                if book_id not in libros_prestados:
                    # El peso del libro es el peso del usuario multiplicado por la frecuencia
                    recomendaciones_contador[book_id] += peso
        
        # Ordenar por peso descendente
        libros_ordenados = sorted(recomendaciones_contador.items(), 
                                 key=lambda x: x[1], 
                                 reverse=True)
        
        # Convertir IDs a objetos Book
        recomendaciones = []
        for book_id, _ in libros_ordenados[:limite]:
            for libro in libros_existentes:
                if libro.id == book_id:
                    recomendaciones.append(libro)
                    break
        
        return recomendaciones
    
    def obtener_estadisticas_grafo(self) -> Dict:
        """
        Obtiene estadísticas generales del grafo.
        
        Returns:
            Dict: Diccionario con estadísticas del grafo.
        """
        total_usuarios = sum(1 for nodo in self.bipartite_graph if nodo.startswith("user_"))
        total_libros = sum(1 for nodo in self.bipartite_graph if nodo.startswith("book_"))
        total_aristas = sum(len(vecinos) for nodo, vecinos in self.bipartite_graph.items() if nodo.startswith("user_"))
        total_conexiones_usuario_usuario = sum(
            len(conexiones) for conexiones in self.user_user_graph.values()
        ) // 2  # Dividir por 2 porque las aristas son bidireccionales
        
        return {
            "total_usuarios": total_usuarios,
            "total_libros": total_libros,
            "total_prestamos": total_aristas,
            "total_conexiones_usuario_usuario": total_conexiones_usuario_usuario,
            "promedio_libros_por_usuario": total_aristas / total_usuarios if total_usuarios > 0 else 0,
            "promedio_usuarios_por_libro": total_aristas / total_libros if total_libros > 0 else 0
        }
    
    def obtener_relaciones_indirectas(self, student_identification: str, profundidad: int = 2) -> Dict:
        """
        Analiza relaciones indirectas entre libros y usuarios.
        
        Encuentra libros relacionados indirectamente a través de otros usuarios.
        
        Args:
            student_identification (str): Identificación del estudiante.
            profundidad (int): Profundidad máxima de búsqueda (por defecto 2).
            
        Returns:
            Dict: Diccionario con información de relaciones indirectas.
        """
        libros_directos = set(self.obtener_libros_prestados_por_usuario(student_identification))
        libros_indirectos = set()
        usuarios_relacionados = set()
        
        # Obtener usuarios conectados directamente
        usuarios_directos = set()
        for libro_id in libros_directos:
            usuarios_del_libro = self.obtener_usuarios_del_libro(libro_id)
            usuarios_directos.update(usuarios_del_libro)
        
        usuarios_directos.discard(student_identification)
        
        # Obtener libros de usuarios relacionados
        for usuario in usuarios_directos:
            libros_del_usuario = self.obtener_libros_prestados_por_usuario(usuario)
            libros_indirectos.update(libros_del_usuario)
            usuarios_relacionados.add(usuario)
        
        libros_indirectos.difference_update(libros_directos)
        
        return {
            "libros_directos": len(libros_directos),
            "libros_indirectos": len(libros_indirectos),
            "usuarios_relacionados": len(usuarios_relacionados),
            "libros_indirectos_ids": list(libros_indirectos)
        }

