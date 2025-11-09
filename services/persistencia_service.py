"""
Servicio de persistencia de datos en JSON.

Este módulo maneja el guardado y carga de datos del usuario en archivos JSON,
priorizando la simplicidad y enfocándose en los datos que el usuario modifica.
"""

import json
import os
from datetime import datetime, date
from typing import Dict, List, Any


class ServicioPersistencia:
    """
    Servicio para guardar y cargar datos del sistema en archivos JSON.
    
    Se enfoca únicamente en los datos que el usuario puede crear, editar o eliminar:
    - Usuarios
    - Libros 
    - Movimientos
    - Asignaciones de categorías (qué libro está en qué categoría)
    
    Attributes:
        directorio_datos (str): Directorio donde se guardan los archivos JSON.
        archivo_usuarios (str): Ruta del archivo de usuarios.
        archivo_libros (str): Ruta del archivo de libros.
        archivo_movimientos (str): Ruta del archivo de movimientos.
        archivo_categorias_libros (str): Ruta del archivo de categorías asignadas.
    """
    
    def __init__(self, directorio_datos="datos"):
        """
        Inicializa el servicio de persistencia.
        
        Args:
            directorio_datos (str): Directorio donde guardar los archivos.
        """
        self.directorio_datos = directorio_datos
        self.archivo_usuarios = os.path.join(directorio_datos, "usuarios.json")
        self.archivo_libros = os.path.join(directorio_datos, "libros.json")
        self.archivo_movimientos = os.path.join(directorio_datos, "movimientos.json")
        self.archivo_categorias_libros = os.path.join(directorio_datos, "categorias_libros.json")
        
        # Crear directorio si no existe
        self._crear_directorio_datos()
    
    def _crear_directorio_datos(self):
        """
        Crea el directorio de datos si no existe.
        """
        if not os.path.exists(self.directorio_datos):
            os.makedirs(self.directorio_datos)
    
    def _convertir_fecha_a_string(self, obj):
        """
        Convierte objetos datetime y date a string para JSON.
        
        Args:
            obj: Objeto a convertir.
            
        Returns:
            str o objeto original: String si es fecha, objeto original si no.
        """
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return obj
    
    def _convertir_string_a_fecha(self, fecha_str):
        """
        Convierte string ISO a objeto date.
        
        Args:
            fecha_str (str): Fecha en formato ISO string.
            
        Returns:
            date: Objeto date o None si hay error.
        """
        try:
            if 'T' in fecha_str:
                # Es datetime, convertir a date
                return datetime.fromisoformat(fecha_str).date()
            else:
                # Es date
                return datetime.fromisoformat(fecha_str).date()
        except:
            return date.today()
    
    def _objeto_a_diccionario(self, obj):
        """
        Convierte un objeto a diccionario para serialización JSON.
        
        Args:
            obj: Objeto a convertir.
            
        Returns:
            dict: Diccionario con los atributos del objeto.
        """
        if hasattr(obj, '__dict__'):
            diccionario = {}
            for clave, valor in obj.__dict__.items():
                diccionario[clave] = self._convertir_fecha_a_string(valor)
            return diccionario
        return obj
    
    def guardar_usuarios(self, usuarios):
        """
        Guarda la lista de usuarios en archivo JSON.
        
        Args:
            usuarios (list): Lista de objetos Usuario.
            
        Returns:
            bool: True si se guardó exitosamente.
        """
        try:
            datos_usuarios = []
            for usuario in usuarios:
                datos_usuarios.append(self._objeto_a_diccionario(usuario))
            
            with open(self.archivo_usuarios, 'w', encoding='utf-8') as archivo:
                json.dump(datos_usuarios, archivo, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"❌ Error al guardar usuarios: {e}")
            return False
    
    def cargar_usuarios(self):
        """
        Carga la lista de usuarios desde archivo JSON.
        
        Returns:
            list: Lista de diccionarios con datos de usuarios.
        """
        try:
            if os.path.exists(self.archivo_usuarios):
                with open(self.archivo_usuarios, 'r', encoding='utf-8') as archivo:
                    datos_usuarios = json.load(archivo)
                    
                    # Convertir fechas de string a date
                    for usuario in datos_usuarios:
                        if 'created_at' in usuario:
                            usuario['created_at'] = self._convertir_string_a_fecha(usuario['created_at'])
                        if 'updated_at' in usuario:
                            usuario['updated_at'] = self._convertir_string_a_fecha(usuario['updated_at'])
                    
                    return datos_usuarios
            return []
        except Exception as e:
            print(f"❌ Error al cargar usuarios: {e}")
            return []
    
    def guardar_libros(self, libros):
        """
        Guarda la lista de libros en archivo JSON.
        
        Args:
            libros (list): Lista de objetos Book.
            
        Returns:
            bool: True si se guardó exitosamente.
        """
        try:
            datos_libros = []
            for libro in libros:
                datos_libros.append(self._objeto_a_diccionario(libro))
            
            with open(self.archivo_libros, 'w', encoding='utf-8') as archivo:
                json.dump(datos_libros, archivo, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"❌ Error al guardar libros: {e}")
            return False
    
    def cargar_libros(self):
        """
        Carga la lista de libros desde archivo JSON.
        
        Returns:
            list: Lista de diccionarios con datos de libros.
        """
        try:
            if os.path.exists(self.archivo_libros):
                with open(self.archivo_libros, 'r', encoding='utf-8') as archivo:
                    datos_libros = json.load(archivo)
                    
                    # Convertir fechas de string a date
                    for libro in datos_libros:
                        if 'created_at' in libro:
                            libro['created_at'] = self._convertir_string_a_fecha(libro['created_at'])
                        if 'updated_at' in libro:
                            libro['updated_at'] = self._convertir_string_a_fecha(libro['updated_at'])
                    
                    return datos_libros
            return []
        except Exception as e:
            print(f"❌ Error al cargar libros: {e}")
            return []
    
    def guardar_movimientos(self, movimientos):
        """
        Guarda la lista de movimientos en archivo JSON.
        
        Args:
            movimientos (list): Lista de objetos Movement.
            
        Returns:
            bool: True si se guardó exitosamente.
        """
        try:
            datos_movimientos = []
            for movimiento in movimientos:
                datos_movimientos.append(self._objeto_a_diccionario(movimiento))
            
            with open(self.archivo_movimientos, 'w', encoding='utf-8') as archivo:
                json.dump(datos_movimientos, archivo, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"❌ Error al guardar movimientos: {e}")
            return False
    
    def cargar_movimientos(self):
        """
        Carga la lista de movimientos desde archivo JSON.
        
        Returns:
            list: Lista de diccionarios con datos de movimientos.
        """
        try:
            if os.path.exists(self.archivo_movimientos):
                with open(self.archivo_movimientos, 'r', encoding='utf-8') as archivo:
                    datos_movimientos = json.load(archivo)
                    
                    # Convertir fechas de string a date
                    for movimiento in datos_movimientos:
                        if 'loan_date' in movimiento:
                            movimiento['loan_date'] = self._convertir_string_a_fecha(movimiento['loan_date'])
                        if 'return_date' in movimiento and movimiento['return_date']:
                            movimiento['return_date'] = self._convertir_string_a_fecha(movimiento['return_date'])
                        if 'created_at' in movimiento:
                            movimiento['created_at'] = self._convertir_string_a_fecha(movimiento['created_at'])
                        if 'updated_at' in movimiento:
                            movimiento['updated_at'] = self._convertir_string_a_fecha(movimiento['updated_at'])
                    
                    return datos_movimientos
            return []
        except Exception as e:
            print(f"❌ Error al cargar movimientos: {e}")
            return []
    
    def guardar_categorias_libros(self, categorias_libros):
        """
        Guarda las asignaciones de categorías a libros.
        
        Args:
            categorias_libros (dict): Diccionario con estructura {nombre_categoria: [ids_libros]}.
            
        Returns:
            bool: True si se guardó exitosamente.
        """
        try:
            with open(self.archivo_categorias_libros, 'w', encoding='utf-8') as archivo:
                json.dump(categorias_libros, archivo, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"❌ Error al guardar categorías de libros: {e}")
            return False
    
    def cargar_categorias_libros(self):
        """
        Carga las asignaciones de categorías a libros.
        
        Returns:
            dict: Diccionario con estructura {nombre_categoria: [ids_libros]}.
        """
        try:
            if os.path.exists(self.archivo_categorias_libros):
                with open(self.archivo_categorias_libros, 'r', encoding='utf-8') as archivo:
                    return json.load(archivo)
            return {}
        except Exception as e:
            print(f"❌ Error al cargar categorías de libros: {e}")
            return {}
    
    def _preparar_datos_para_json(self, datos):
        """
        Convierte objetos date en los datos a strings para JSON.
        
        Args:
            datos: Lista de diccionarios con posibles objetos date.
            
        Returns:
            list: Datos con fechas convertidas a string.
        """
        datos_convertidos = []
        for item in datos:
            item_convertido = {}
            for clave, valor in item.items():
                item_convertido[clave] = self._convertir_fecha_a_string(valor)
            datos_convertidos.append(item_convertido)
        return datos_convertidos
    
    def exportar_todo(self, nombre_archivo="respaldo_completo.json"):
        """
        Exporta todos los datos a un solo archivo de respaldo.
        
        Args:
            nombre_archivo (str): Nombre del archivo de respaldo.
            
        Returns:
            bool: True si se exportó exitosamente.
        """
        try:
            # Cargar datos y convertir fechas a string para JSON
            usuarios_raw = self.cargar_usuarios()
            libros_raw = self.cargar_libros()
            movimientos_raw = self.cargar_movimientos()
            
            datos_completos = {
                'fecha_exportacion': datetime.now().isoformat(),
                'usuarios': self._preparar_datos_para_json(usuarios_raw),
                'libros': self._preparar_datos_para_json(libros_raw),
                'movimientos': self._preparar_datos_para_json(movimientos_raw),
                'categorias_libros': self.cargar_categorias_libros()
            }
            
            ruta_respaldo = os.path.join(self.directorio_datos, nombre_archivo)
            with open(ruta_respaldo, 'w', encoding='utf-8') as archivo:
                json.dump(datos_completos, archivo, ensure_ascii=False, indent=2)
            
            print(f"✅ Respaldo completo guardado en: {ruta_respaldo}")
            return True
        except Exception as e:
            print(f"❌ Error al crear respaldo: {e}")
            return False
    
    def obtener_estadisticas_archivos(self):
        """
        Obtiene estadísticas básicas de los archivos de datos.
        
        Returns:
            dict: Estadísticas de los archivos.
        """
        estadisticas = {
            'usuarios': {
                'existe': os.path.exists(self.archivo_usuarios),
                'cantidad': len(self.cargar_usuarios()) if os.path.exists(self.archivo_usuarios) else 0
            },
            'libros': {
                'existe': os.path.exists(self.archivo_libros),
                'cantidad': len(self.cargar_libros()) if os.path.exists(self.archivo_libros) else 0
            },
            'movimientos': {
                'existe': os.path.exists(self.archivo_movimientos),
                'cantidad': len(self.cargar_movimientos()) if os.path.exists(self.archivo_movimientos) else 0
            },
            'categorias_libros': {
                'existe': os.path.exists(self.archivo_categorias_libros),
                'cantidad_categorias': len(self.cargar_categorias_libros()) if os.path.exists(self.archivo_categorias_libros) else 0
            }
        }
        
        return estadisticas