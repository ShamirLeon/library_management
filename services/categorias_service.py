from models.categorias import ArbolCategorias
from services.persistencia_service import ServicioPersistencia

class ServicioCategorias:
    """
    Servicio para la gestión del árbol de categorías de libros.
    
    Esta clase maneja todas las operaciones relacionadas con la clasificación
    temática de libros, proporcionando funcionalidades para organizar,
    buscar y analizar el catálogo por categorías.
    
    Attributes:
        arbol_categorias (ArbolCategorias): Instancia del árbol de categorías.
        servicio_libros: Referencia al servicio de libros para validaciones.
    """
    
    def __init__(self, servicio_libros=None):
        """
        Inicializa el servicio de categorías cargando asignaciones desde archivo JSON.
        
        Args:
            servicio_libros: Instancia del servicio de libros para validaciones.
        """
        self.persistencia = ServicioPersistencia()
        self.arbol_categorias = ArbolCategorias()
        self.servicio_libros = servicio_libros
        self._cargar_asignaciones_categorias()
    
    def _cargar_asignaciones_categorias(self):
        """
        Carga las asignaciones de libros a categorías desde archivo JSON.
        """
        categorias_libros = self.persistencia.cargar_categorias_libros()
        
        # Restaurar las asignaciones en el árbol
        for nombre_categoria, ids_libros in categorias_libros.items():
            categoria = self.arbol_categorias.raiz.buscar_categoria(nombre_categoria)
            if categoria:
                categoria.libros = ids_libros.copy()
    
    def _guardar_asignaciones_categorias(self):
        """
        Guarda las asignaciones actuales de libros a categorías en archivo JSON.
        """
        categorias_libros = {}
        
        def _recopilar_asignaciones(nodo):
            if nodo.libros:  # Solo guardar categorías con libros asignados
                categorias_libros[nodo.nombre] = nodo.libros.copy()
            
            for hijo in nodo.hijos:
                _recopilar_asignaciones(hijo)
        
        _recopilar_asignaciones(self.arbol_categorias.raiz)
        self.persistencia.guardar_categorias_libros(categorias_libros)
    
    def establecer_servicio_libros(self, servicio_libros):
        """
        Establece la referencia al servicio de libros.
        
        Args:
            servicio_libros: Instancia del servicio de libros.
        """
        self.servicio_libros = servicio_libros
    
    def crear_categoria(self, nombre_padre, nombre_categoria, descripcion=""):
        """
        Crea una nueva categoría como hija de una categoría existente.
        
        Args:
            nombre_padre (str): Nombre de la categoría padre.
            nombre_categoria (str): Nombre de la nueva categoría.
            descripcion (str, optional): Descripción de la nueva categoría.
            
        Returns:
            dict: Resultado de la operación con éxito y mensaje.
        """
        if not nombre_categoria.strip():
            return {
                'exito': False,
                'mensaje': 'El nombre de la categoría no puede estar vacío.'
            }
        
        # Verificar que no exista ya una categoría con el mismo nombre
        if self.arbol_categorias.raiz.buscar_categoria(nombre_categoria):
            return {
                'exito': False,
                'mensaje': f'Ya existe una categoría con el nombre "{nombre_categoria}".'
            }
        
        exito = self.arbol_categorias.agregar_categoria(nombre_padre, nombre_categoria, descripcion)
        
        if exito:
            return {
                'exito': True,
                'mensaje': f'Categoría "{nombre_categoria}" creada exitosamente bajo "{nombre_padre}".'
            }
        else:
            return {
                'exito': False,
                'mensaje': f'No se pudo crear la categoría. La categoría padre "{nombre_padre}" no existe.'
            }
    
    def asignar_libro_a_categoria(self, id_libro, nombre_categoria):
        """
        Asigna un libro a una categoría específica.
        
        Args:
            id_libro (int): ID del libro a categorizar.
            nombre_categoria (str): Nombre de la categoría destino.
            
        Returns:
            dict: Resultado de la operación con éxito y mensaje.
        """
        # Verificar que el libro existe (si hay servicio de libros disponible)
        if self.servicio_libros:
            libro = self.servicio_libros.obtener_libro_por_id(id_libro)
            if not libro:
                return {
                    'exito': False,
                    'mensaje': f'El libro con ID {id_libro} no existe en el catálogo.'
                }
        
        exito = self.arbol_categorias.categorizar_libro(id_libro, nombre_categoria)
        
        if exito:
            self._guardar_asignaciones_categorias()
            return {
                'exito': True,
                'mensaje': f'Libro con ID {id_libro} asignado a la categoría "{nombre_categoria}".'
            }
        else:
            return {
                'exito': False,
                'mensaje': f'No se pudo asignar el libro. La categoría "{nombre_categoria}" no existe.'
            }
    
    def remover_libro_de_categoria(self, id_libro, nombre_categoria):
        """
        Remueve un libro de una categoría específica.
        
        Args:
            id_libro (int): ID del libro a remover.
            nombre_categoria (str): Nombre de la categoría origen.
            
        Returns:
            dict: Resultado de la operación con éxito y mensaje.
        """
        exito = self.arbol_categorias.descategorizar_libro(id_libro, nombre_categoria)
        
        if exito:
            self._guardar_asignaciones_categorias()
            return {
                'exito': True,
                'mensaje': f'Libro con ID {id_libro} removido de la categoría "{nombre_categoria}".'
            }
        else:
            return {
                'exito': False,
                'mensaje': f'No se pudo remover el libro. El libro no está en la categoría "{nombre_categoria}" o la categoría no existe.'
            }
    
    def obtener_libros_por_categoria(self, nombre_categoria, incluir_subcategorias=True):
        """
        Obtiene los libros de una categoría específica.
        
        Args:
            nombre_categoria (str): Nombre de la categoría.
            incluir_subcategorias (bool): Si incluir libros de subcategorías.
            
        Returns:
            dict: Resultado con lista de libros y metadatos.
        """
        ids_libros = self.arbol_categorias.obtener_libros_por_categoria(
            nombre_categoria, incluir_subcategorias
        )
        
        if ids_libros is None:
            return {
                'exito': False,
                'mensaje': f'La categoría "{nombre_categoria}" no existe.',
                'libros': [],
                'cantidad': 0
            }
        
        # Si hay servicio de libros, obtener los objetos completos
        libros_completos = []
        if self.servicio_libros:
            for id_libro in ids_libros:
                libro = self.servicio_libros.obtener_libro_por_id(id_libro)
                if libro:
                    libros_completos.append(libro)
        
        return {
            'exito': True,
            'mensaje': f'Se encontraron {len(ids_libros)} libros en la categoría "{nombre_categoria}".',
            'ids_libros': ids_libros,
            'libros': libros_completos,
            'cantidad': len(ids_libros),
            'incluye_subcategorias': incluir_subcategorias
        }
    
    def buscar_categorias_de_libro(self, id_libro):
        """
        Busca en qué categorías está clasificado un libro.
        
        Args:
            id_libro (int): ID del libro a buscar.
            
        Returns:
            dict: Resultado con lista de categorías que contienen el libro.
        """
        categorias = self.arbol_categorias.buscar_categoria_de_libro(id_libro)
        
        return {
            'id_libro': id_libro,
            'categorias': categorias,
            'cantidad_categorias': len(categorias),
            'mensaje': f'El libro está clasificado en {len(categorias)} categorías.' if categorias else 'El libro no está clasificado en ninguna categoría.'
        }
    
    def obtener_estadisticas(self, nombre_categoria=None):
        """
        Obtiene estadísticas detalladas de categorías.
        
        Args:
            nombre_categoria (str, optional): Nombre de categoría específica.
                                            Si es None, retorna estadísticas generales.
            
        Returns:
            dict: Estadísticas de la(s) categoría(s).
        """
        return self.arbol_categorias.obtener_estadisticas_categoria(nombre_categoria)
    
    def mostrar_estructura_categorias(self, mostrar_libros=False):
        """
        Muestra la estructura completa del árbol de categorías.
        
        Args:
            mostrar_libros (bool): Si mostrar los IDs de libros en cada categoría.
            
        Returns:
            str: Representación textual del árbol de categorías.
        """
        return self.arbol_categorias.mostrar_arbol(mostrar_libros=mostrar_libros)
    
    def listar_todas_las_categorias(self):
        """
        Lista todas las categorías disponibles.
        
        Returns:
            list[str]: Lista ordenada de nombres de categorías.
        """
        return self.arbol_categorias.listar_todas_las_categorias()
    
    def buscar_libros_por_termino_en_categorias(self, termino):
        """
        Busca libros en categorías cuyos nombres contengan el término especificado.
        
        Args:
            termino (str): Término a buscar en nombres de categorías.
            
        Returns:
            dict: Resultado con libros encontrados y categorías coincidentes.
        """
        termino_lower = termino.lower()
        categorias_coincidentes = []
        todos_los_libros = set()
        
        # Buscar categorías que contengan el término
        todas_las_categorias = self.listar_todas_las_categorias()
        for nombre_categoria in todas_las_categorias:
            if termino_lower in nombre_categoria.lower():
                categorias_coincidentes.append(nombre_categoria)
                ids_libros = self.arbol_categorias.obtener_libros_por_categoria(nombre_categoria)
                todos_los_libros.update(ids_libros)
        
        # Obtener libros completos si hay servicio disponible
        libros_completos = []
        if self.servicio_libros:
            for id_libro in todos_los_libros:
                libro = self.servicio_libros.obtener_libro_por_id(id_libro)
                if libro:
                    libros_completos.append(libro)
        
        return {
            'termino_busqueda': termino,
            'categorias_encontradas': categorias_coincidentes,
            'cantidad_categorias': len(categorias_coincidentes),
            'ids_libros': list(todos_los_libros),
            'libros': libros_completos,
            'cantidad_libros': len(todos_los_libros),
            'mensaje': f'Se encontraron {len(todos_los_libros)} libros en {len(categorias_coincidentes)} categorías que contienen "{termino}".'
        }
    
    def obtener_resumen_general(self):
        """
        Obtiene un resumen general del sistema de categorías.
        
        Returns:
            dict: Resumen con estadísticas generales del árbol.
        """
        estadisticas_completas = self.obtener_estadisticas()
        total_categorias = len(estadisticas_completas) - 1  # Excluir nodo raíz
        total_libros_categorizados = 0
        categorias_con_libros = 0
        categoria_mas_poblada = {'nombre': '', 'cantidad': 0}
        
        for nombre, stats in estadisticas_completas.items():
            if nombre != "Biblioteca General":  # Excluir nodo raíz
                libros_directos = stats['libros_directos']
                total_libros_categorizados += libros_directos
                
                if libros_directos > 0:
                    categorias_con_libros += 1
                
                if libros_directos > categoria_mas_poblada['cantidad']:
                    categoria_mas_poblada = {
                        'nombre': nombre,
                        'cantidad': libros_directos
                    }
        
        return {
            'total_categorias': total_categorias,
            'categorias_con_libros': categorias_con_libros,
            'categorias_vacias': total_categorias - categorias_con_libros,
            'total_libros_categorizados': total_libros_categorizados,
            'categoria_mas_poblada': categoria_mas_poblada,
            'porcentaje_categorias_utilizadas': round((categorias_con_libros / total_categorias * 100), 2) if total_categorias > 0 else 0
        }