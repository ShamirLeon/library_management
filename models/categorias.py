class NodoCategoria:
    """
    Nodo individual del árbol de categorías.
    
    Representa una categoría o subcategoría en la jerarquía de organización
    de libros. Cada nodo puede contener múltiples libros y subcategorías hijas.
    
    Attributes:
        nombre (str): Nombre de la categoría.
        descripcion (str): Descripción detallada de la categoría.
        hijos (list[NodoCategoria]): Lista de subcategorías hijas.
        padre (NodoCategoria): Referencia al nodo padre (None para raíz).
        libros (list[int]): Lista de IDs de libros pertenecientes a esta categoría.
    """
    
    def __init__(self, nombre, descripcion=""):
        """
        Inicializa un nuevo nodo de categoría.
        
        Args:
            nombre (str): Nombre de la categoría.
            descripcion (str, optional): Descripción de la categoría.
        """
        self.nombre = nombre
        self.descripcion = descripcion
        self.hijos = []
        self.padre = None
        self.libros = []
    
    def agregar_hijo(self, nodo_hijo):
        """
        Agrega una subcategoría como hijo de este nodo.
        
        Args:
            nodo_hijo (NodoCategoria): El nodo hijo a agregar.
        """
        nodo_hijo.padre = self
        self.hijos.append(nodo_hijo)
    
    def agregar_libro(self, id_libro):
        """
        Agrega un libro a esta categoría.
        
        Args:
            id_libro (int): ID del libro a agregar.
        """
        if id_libro not in self.libros:
            self.libros.append(id_libro)
    
    def remover_libro(self, id_libro):
        """
        Remueve un libro de esta categoría.
        
        Args:
            id_libro (int): ID del libro a remover.
            
        Returns:
            bool: True si el libro fue removido, False si no se encontró.
        """
        if id_libro in self.libros:
            self.libros.remove(id_libro)
            return True
        return False
    
    def obtener_todos_los_libros(self):
        """
        Obtiene todos los libros de esta categoría y sus subcategorías.
        
        Returns:
            list[int]: Lista de IDs de todos los libros en esta rama del árbol.
        """
        todos_los_libros = self.libros.copy()
        for hijo in self.hijos:
            todos_los_libros.extend(hijo.obtener_todos_los_libros())
        return todos_los_libros
    
    def buscar_categoria(self, nombre):
        """
        Busca una categoría por nombre en esta rama del árbol.
        
        Args:
            nombre (str): Nombre de la categoría a buscar.
            
        Returns:
            NodoCategoria: El nodo encontrado o None si no existe.
        """
        if self.nombre.lower() == nombre.lower():
            return self
        
        for hijo in self.hijos:
            resultado = hijo.buscar_categoria(nombre)
            if resultado:
                return resultado
        
        return None
    
    def obtener_ruta(self):
        """
        Obtiene la ruta completa desde la raíz hasta este nodo.
        
        Returns:
            list[str]: Lista de nombres de categorías formando la ruta.
        """
        if self.padre is None:
            return [self.nombre]
        return self.padre.obtener_ruta() + [self.nombre]
    
    def contar_libros_directos(self):
        """
        Cuenta los libros directamente asignados a esta categoría.
        
        Returns:
            int: Número de libros en esta categoría (sin subcategorías).
        """
        return len(self.libros)
    
    def contar_libros_totales(self):
        """
        Cuenta todos los libros en esta categoría y subcategorías.
        
        Returns:
            int: Número total de libros en esta rama.
        """
        return len(self.obtener_todos_los_libros())


class ArbolCategorias:
    """
    Árbol completo de categorías para organizar el catálogo de libros.
    
    Proporciona una estructura jerárquica para clasificar libros temáticamente,
    con operaciones para navegar, buscar y gestionar la taxonomía.
    
    Attributes:
        raiz (NodoCategoria): Nodo raíz del árbol que contiene todas las categorías.
    """
    
    def __init__(self):
        """
        Inicializa el árbol con categorías predeterminadas.
        """
        self.raiz = NodoCategoria("Biblioteca General", "Catálogo completo de la biblioteca")
        self._configurar_categorias_por_defecto()
    
    def _configurar_categorias_por_defecto(self):
        """
        Configura la estructura inicial de categorías y subcategorías.
        """
        # Categoría: Ficción
        ficcion = NodoCategoria("Ficción", "Literatura de ficción y narrativa imaginativa")
        self.raiz.agregar_hijo(ficcion)
        
        # Subcategorías de Ficción
        ficcion.agregar_hijo(NodoCategoria("Novela", "Novelas largas de ficción"))
        ficcion.agregar_hijo(NodoCategoria("Cuento", "Relatos cortos y cuentos"))
        ficcion.agregar_hijo(NodoCategoria("Ciencia Ficción", "Literatura de ciencia ficción y futurismo"))
        ficcion.agregar_hijo(NodoCategoria("Fantasía", "Literatura fantástica y mundos imaginarios"))
        ficcion.agregar_hijo(NodoCategoria("Misterio", "Novelas de misterio y suspenso"))
        ficcion.agregar_hijo(NodoCategoria("Romance", "Literatura romántica"))
        ficcion.agregar_hijo(NodoCategoria("Terror", "Literatura de terror y horror"))
        
        # Categoría: No Ficción
        no_ficcion = NodoCategoria("No Ficción", "Obras basadas en hechos reales y conocimiento")
        self.raiz.agregar_hijo(no_ficcion)
        
        # Subcategorías de No Ficción
        no_ficcion.agregar_hijo(NodoCategoria("Historia", "Libros de historia y acontecimientos pasados"))
        no_ficcion.agregar_hijo(NodoCategoria("Biografía", "Biografías y autobiografías"))
        no_ficcion.agregar_hijo(NodoCategoria("Ciencia", "Divulgación científica y textos académicos"))
        no_ficcion.agregar_hijo(NodoCategoria("Tecnología", "Libros sobre tecnología e innovación"))
        no_ficcion.agregar_hijo(NodoCategoria("Filosofía", "Obras filosóficas y pensamiento"))
        no_ficcion.agregar_hijo(NodoCategoria("Arte", "Libros sobre arte y cultura"))
        no_ficcion.agregar_hijo(NodoCategoria("Deportes", "Literatura deportiva y actividad física"))
        
        # Categoría: Educación
        educacion = NodoCategoria("Educación", "Material educativo y académico")
        self.raiz.agregar_hijo(educacion)
        
        # Subcategorías de Educación
        educacion.agregar_hijo(NodoCategoria("Matemáticas", "Libros de matemáticas y álgebra"))
        educacion.agregar_hijo(NodoCategoria("Lengua", "Gramática, literatura y lingüística"))
        educacion.agregar_hijo(NodoCategoria("Ciencias Naturales", "Biología, química, física"))
        educacion.agregar_hijo(NodoCategoria("Ciencias Sociales", "Sociología, antropología, política"))
        educacion.agregar_hijo(NodoCategoria("Idiomas", "Aprendizaje de idiomas extranjeros"))
        
        # Categoría: Referencia
        referencia = NodoCategoria("Referencia", "Material de consulta y referencia")
        self.raiz.agregar_hijo(referencia)
        
        # Subcategorías de Referencia
        referencia.agregar_hijo(NodoCategoria("Diccionarios", "Diccionarios monolingües y bilingües"))
        referencia.agregar_hijo(NodoCategoria("Enciclopedias", "Enciclopedias generales y especializadas"))
        referencia.agregar_hijo(NodoCategoria("Atlas", "Atlas geográficos y mapas"))
        referencia.agregar_hijo(NodoCategoria("Manuales", "Manuales técnicos y guías"))
        
        # Categoría: Literatura Infantil
        infantil = NodoCategoria("Literatura Infantil", "Libros para niños y jóvenes")
        self.raiz.agregar_hijo(infantil)
        
        # Subcategorías de Literatura Infantil
        infantil.agregar_hijo(NodoCategoria("Cuentos Infantiles", "Cuentos para niños pequeños"))
        infantil.agregar_hijo(NodoCategoria("Literatura Juvenil", "Libros para adolescentes"))
        infantil.agregar_hijo(NodoCategoria("Libros Ilustrados", "Libros con ilustraciones"))
        infantil.agregar_hijo(NodoCategoria("Educativos Infantiles", "Material educativo para niños"))
    
    def agregar_categoria(self, nombre_padre, nombre_categoria, descripcion=""):
        """
        Agrega una nueva categoría como hija de una categoría existente.
        
        Args:
            nombre_padre (str): Nombre de la categoría padre.
            nombre_categoria (str): Nombre de la nueva categoría.
            descripcion (str, optional): Descripción de la nueva categoría.
            
        Returns:
            bool: True si la categoría fue agregada exitosamente.
        """
        padre = self.raiz.buscar_categoria(nombre_padre)
        if padre:
            nueva_categoria = NodoCategoria(nombre_categoria, descripcion)
            padre.agregar_hijo(nueva_categoria)
            return True
        return False
    
    def categorizar_libro(self, id_libro, nombre_categoria):
        """
        Asigna un libro a una categoría específica.
        
        Args:
            id_libro (int): ID del libro a categorizar.
            nombre_categoria (str): Nombre de la categoría destino.
            
        Returns:
            bool: True si el libro fue categorizado exitosamente.
        """
        categoria = self.raiz.buscar_categoria(nombre_categoria)
        if categoria:
            categoria.agregar_libro(id_libro)
            return True
        return False
    
    def descategorizar_libro(self, id_libro, nombre_categoria):
        """
        Remueve un libro de una categoría específica.
        
        Args:
            id_libro (int): ID del libro a remover.
            nombre_categoria (str): Nombre de la categoría origen.
            
        Returns:
            bool: True si el libro fue removido exitosamente.
        """
        categoria = self.raiz.buscar_categoria(nombre_categoria)
        if categoria:
            return categoria.remover_libro(id_libro)
        return False
    
    def obtener_libros_por_categoria(self, nombre_categoria, incluir_subcategorias=True):
        """
        Obtiene los libros de una categoría específica.
        
        Args:
            nombre_categoria (str): Nombre de la categoría.
            incluir_subcategorias (bool): Si incluir libros de subcategorías.
            
        Returns:
            list[int]: Lista de IDs de libros en la categoría.
        """
        categoria = self.raiz.buscar_categoria(nombre_categoria)
        if categoria:
            if incluir_subcategorias:
                return categoria.obtener_todos_los_libros()
            else:
                return categoria.libros.copy()
        return []
    
    def buscar_categoria_de_libro(self, id_libro):
        """
        Busca en qué categorías está clasificado un libro.
        
        Args:
            id_libro (int): ID del libro a buscar.
            
        Returns:
            list[str]: Lista de nombres de categorías que contienen el libro.
        """
        categorias_encontradas = []
        
        def _buscar_en_nodo(nodo):
            if id_libro in nodo.libros:
                categorias_encontradas.append(nodo.nombre)
            
            for hijo in nodo.hijos:
                _buscar_en_nodo(hijo)
        
        _buscar_en_nodo(self.raiz)
        return categorias_encontradas
    
    def obtener_estadisticas_categoria(self, nombre_categoria=None):
        """
        Obtiene estadísticas detalladas de una categoría o de todo el árbol.
        
        Args:
            nombre_categoria (str, optional): Nombre de la categoría específica.
                                            Si es None, retorna estadísticas de todo el árbol.
            
        Returns:
            dict: Diccionario con estadísticas de la categoría.
        """
        if nombre_categoria:
            categoria = self.raiz.buscar_categoria(nombre_categoria)
            if not categoria:
                return {}
            
            return {
                'nombre': categoria.nombre,
                'descripcion': categoria.descripcion,
                'ruta': ' -> '.join(categoria.obtener_ruta()),
                'libros_directos': categoria.contar_libros_directos(),
                'libros_totales': categoria.contar_libros_totales(),
                'subcategorias': len(categoria.hijos),
                'nombres_subcategorias': [hijo.nombre for hijo in categoria.hijos]
            }
        else:
            # Estadísticas de todo el árbol
            estadisticas = {}
            
            def _recopilar_estadisticas(nodo):
                estadisticas[nodo.nombre] = {
                    'descripcion': nodo.descripcion,
                    'ruta': ' -> '.join(nodo.obtener_ruta()),
                    'libros_directos': nodo.contar_libros_directos(),
                    'libros_totales': nodo.contar_libros_totales(),
                    'subcategorias': len(nodo.hijos),
                    'nombres_subcategorias': [hijo.nombre for hijo in nodo.hijos]
                }
                
                for hijo in nodo.hijos:
                    _recopilar_estadisticas(hijo)
            
            _recopilar_estadisticas(self.raiz)
            return estadisticas
    
    def mostrar_arbol(self, nodo=None, nivel=0, mostrar_libros=False):
        """
        Muestra la estructura del árbol de categorías de forma visual.
        
        Args:
            nodo (NodoCategoria, optional): Nodo desde donde comenzar.
                                            Si es None, comienza desde la raíz.
            nivel (int): Nivel de indentación actual.
            mostrar_libros (bool): Si mostrar los IDs de libros en cada categoría.
        
        Returns:
            str: Representación textual del árbol.
        """
        if nodo is None:
            nodo = self.raiz
        
        indentacion = "  " * nivel
        simbolo = "├─ " if nivel > 0 else ""
        
        # Información básica del nodo
        total_libros = nodo.contar_libros_totales()
        directos_libros = nodo.contar_libros_directos()
        
        resultado = f"{indentacion}{simbolo}{nodo.nombre}"
        
        if total_libros > 0:
            if directos_libros > 0 and directos_libros != total_libros:
                resultado += f" ({directos_libros} directos, {total_libros} total)"
            else:
                resultado += f" ({total_libros} libros)"
        
        if mostrar_libros and directos_libros > 0:
            resultado += f" - IDs: {nodo.libros}"
        
        resultado += "\n"
        
        # Recursivamente mostrar hijos
        for i, hijo in enumerate(nodo.hijos):
            es_ultimo = i == len(nodo.hijos) - 1
            resultado += self.mostrar_arbol(hijo, nivel + 1, mostrar_libros)
        
        return resultado
    
    def listar_todas_las_categorias(self):
        """
        Lista todos los nombres de categorías disponibles en el árbol.
        
        Returns:
            list[str]: Lista ordenada de nombres de todas las categorías.
        """
        categorias = []
        
        def _recopilar_nombres(nodo):
            if nodo != self.raiz:  # Excluir el nodo raíz
                categorias.append(nodo.nombre)
            
            for hijo in nodo.hijos:
                _recopilar_nombres(hijo)
        
        _recopilar_nombres(self.raiz)
        return sorted(categorias)