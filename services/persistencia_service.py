"""
Servicio de persistencia de datos en SQLite.

Este módulo maneja el guardado y carga de datos del sistema usando SQLite,
reemplazando el sistema de archivos JSON por una base de datos relacional.
"""

import sqlite3
import os
import json
from datetime import datetime, date
from typing import Dict, List, Any


class ServicioPersistencia:
    """
    Servicio para guardar y cargar datos del sistema en SQLite.
    
    Reemplaza el sistema de archivos JSON por una base de datos SQLite,
    manteniendo la misma interfaz para compatibilidad con servicios existentes.
    
    Attributes:
        db_path (str): Ruta al archivo de base de datos SQLite.
        conn: Conexión a la base de datos.
    """
    
    def __init__(self, directorio_datos="datos"):
        """
        Inicializa el servicio de persistencia SQLite.
        
        Args:
            directorio_datos (str): Directorio donde guardar la base de datos.
        """
        self.directorio_datos = directorio_datos
        self.db_path = os.path.join(directorio_datos, "biblioteca.db")
        
        # Mantener compatibilidad con código que espera archivos JSON
        self.archivo_usuarios = os.path.join(directorio_datos, "usuarios.json")
        self.archivo_libros = os.path.join(directorio_datos, "libros.json")
        self.archivo_movimientos = os.path.join(directorio_datos, "movimientos.json")
        self.archivo_categorias_libros = os.path.join(directorio_datos, "categorias_libros.json")
        
        # Crear directorio si no existe
        self._crear_directorio_datos()
        
        # Inicializar conexión a SQLite
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  # Permite acceso por nombre de columna
        self._crear_tablas()
        
        # Migrar datos de JSON a SQLite si existen
        self._migrar_datos_json_a_sqlite()
    
    def _crear_directorio_datos(self):
        """
        Crea el directorio de datos si no existe.
        """
        if not os.path.exists(self.directorio_datos):
            os.makedirs(self.directorio_datos)
    
    def _crear_tablas(self):
        """
        Crea las tablas necesarias en la base de datos si no existen.
        """
        cursor = self.conn.cursor()
        
        # Tabla de usuarios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at DATE NOT NULL,
                updated_at DATE NOT NULL
            )
        ''')
        
        # Tabla de libros
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS libros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                published_date TEXT,
                isbn TEXT NOT NULL,
                quantity INTEGER NOT NULL DEFAULT 0,
                created_at DATE NOT NULL,
                updated_at DATE NOT NULL
            )
        ''')
        
        # Tabla de movimientos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS movimientos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NOT NULL,
                student_name TEXT NOT NULL,
                student_identification TEXT NOT NULL,
                loan_date DATE NOT NULL,
                return_date DATE,
                returned INTEGER NOT NULL DEFAULT 0,
                created_at DATE NOT NULL,
                updated_at DATE NOT NULL,
                FOREIGN KEY (book_id) REFERENCES libros(id)
            )
        ''')
        
        # Tabla de relación categorías-libros
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categorias_libros (
                categoria_nombre TEXT NOT NULL,
                libro_id INTEGER NOT NULL,
                PRIMARY KEY (categoria_nombre, libro_id),
                FOREIGN KEY (libro_id) REFERENCES libros(id)
            )
        ''')
        
        self.conn.commit()
    
    def _migrar_datos_json_a_sqlite(self):
        """
        Migra datos existentes de JSON a SQLite si los archivos JSON existen
        y la base de datos está vacía.
        """
        try:
            cursor = self.conn.cursor()
            
            # Verificar si hay datos en SQLite
            cursor.execute('SELECT COUNT(*) FROM usuarios')
            usuarios_count = cursor.fetchone()[0]
            
            # Si hay datos en SQLite, no migrar
            if usuarios_count > 0:
                return
            
            # Intentar cargar datos de JSON
            if os.path.exists(self.archivo_usuarios):
                self._migrar_usuarios_json()
            
            if os.path.exists(self.archivo_libros):
                self._migrar_libros_json()
            
            if os.path.exists(self.archivo_movimientos):
                self._migrar_movimientos_json()
            
            if os.path.exists(self.archivo_categorias_libros):
                self._migrar_categorias_json()
                
        except Exception as e:
            print(f"⚠️ Advertencia al migrar datos: {e}")
    
    def _migrar_usuarios_json(self):
        """Migra usuarios de JSON a SQLite."""
        try:
            with open(self.archivo_usuarios, 'r', encoding='utf-8') as f:
                usuarios = json.load(f)
            
            cursor = self.conn.cursor()
            for usuario in usuarios:
                cursor.execute('''
                    INSERT OR IGNORE INTO usuarios (id, name, email, password, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    usuario['id'],
                    usuario['name'],
                    usuario['email'],
                    usuario['password'],
                    usuario.get('created_at', date.today().isoformat()),
                    usuario.get('updated_at', date.today().isoformat())
                ))
            self.conn.commit()
            print("✅ Usuarios migrados de JSON a SQLite")
        except Exception as e:
            print(f"⚠️ Error al migrar usuarios: {e}")
    
    def _migrar_libros_json(self):
        """Migra libros de JSON a SQLite."""
        try:
            with open(self.archivo_libros, 'r', encoding='utf-8') as f:
                libros = json.load(f)
            
            cursor = self.conn.cursor()
            for libro in libros:
                cursor.execute('''
                    INSERT OR IGNORE INTO libros (id, title, author, published_date, isbn, quantity, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    libro['id'],
                    libro['title'],
                    libro['author'],
                    libro.get('published_date', ''),
                    libro['isbn'],
                    libro['quantity'],
                    libro.get('created_at', date.today().isoformat()),
                    libro.get('updated_at', date.today().isoformat())
                ))
            self.conn.commit()
            print("✅ Libros migrados de JSON a SQLite")
        except Exception as e:
            print(f"⚠️ Error al migrar libros: {e}")
    
    def _migrar_movimientos_json(self):
        """Migra movimientos de JSON a SQLite."""
        try:
            with open(self.archivo_movimientos, 'r', encoding='utf-8') as f:
                movimientos = json.load(f)
            
            cursor = self.conn.cursor()
            for movimiento in movimientos:
                cursor.execute('''
                    INSERT OR IGNORE INTO movimientos 
                    (id, book_id, student_name, student_identification, loan_date, return_date, returned, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    movimiento['id'],
                    movimiento['book_id'],
                    movimiento['student_name'],
                    movimiento['student_identification'],
                    movimiento.get('loan_date', date.today().isoformat()),
                    movimiento.get('return_date'),
                    1 if movimiento.get('returned', False) else 0,
                    movimiento.get('created_at', date.today().isoformat()),
                    movimiento.get('updated_at', date.today().isoformat())
                ))
            self.conn.commit()
            print("✅ Movimientos migrados de JSON a SQLite")
        except Exception as e:
            print(f"⚠️ Error al migrar movimientos: {e}")
    
    def _migrar_categorias_json(self):
        """Migra categorías de JSON a SQLite."""
        try:
            with open(self.archivo_categorias_libros, 'r', encoding='utf-8') as f:
                categorias = json.load(f)
            
            cursor = self.conn.cursor()
            for categoria_nombre, ids_libros in categorias.items():
                for libro_id in ids_libros:
                    cursor.execute('''
                        INSERT OR IGNORE INTO categorias_libros (categoria_nombre, libro_id)
                        VALUES (?, ?)
                    ''', (categoria_nombre, libro_id))
            self.conn.commit()
            print("✅ Categorías migradas de JSON a SQLite")
        except Exception as e:
            print(f"⚠️ Error al migrar categorías: {e}")
    
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
        Guarda la lista de usuarios en la base de datos SQLite.
        
        Args:
            usuarios (list): Lista de objetos Usuario.
            
        Returns:
            bool: True si se guardó exitosamente.
        """
        try:
            cursor = self.conn.cursor()
            
            # Eliminar todos los usuarios existentes
            cursor.execute('DELETE FROM usuarios')
            
            # Insertar usuarios
            for usuario in usuarios:
                cursor.execute('''
                    INSERT INTO usuarios (id, name, email, password, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    usuario.id,
                    usuario.name,
                    usuario.email,
                    usuario.password,
                    self._convertir_fecha_a_string(usuario.created_at),
                    self._convertir_fecha_a_string(usuario.updated_at)
                ))
            
            self.conn.commit()
            return True
        except Exception as e:
            print(f"❌ Error al guardar usuarios: {e}")
            return False
    
    def cargar_usuarios(self):
        """
        Carga la lista de usuarios desde la base de datos SQLite.
        
        Returns:
            list: Lista de diccionarios con datos de usuarios.
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute('SELECT * FROM usuarios')
            rows = cursor.fetchall()
            
            usuarios = []
            for row in rows:
                usuario = {
                    'id': row['id'],
                    'name': row['name'],
                    'email': row['email'],
                    'password': row['password'],
                    'created_at': self._convertir_string_a_fecha(row['created_at']),
                    'updated_at': self._convertir_string_a_fecha(row['updated_at'])
                }
                usuarios.append(usuario)
            
            return usuarios
        except Exception as e:
            print(f"❌ Error al cargar usuarios: {e}")
            return []
    
    def guardar_libros(self, libros):
        """
        Guarda la lista de libros en la base de datos SQLite.
        
        Args:
            libros (list): Lista de objetos Book.
            
        Returns:
            bool: True si se guardó exitosamente.
        """
        try:
            cursor = self.conn.cursor()
            
            # Eliminar todos los libros existentes
            cursor.execute('DELETE FROM libros')
            
            # Insertar libros
            for libro in libros:
                cursor.execute('''
                    INSERT INTO libros (id, title, author, published_date, isbn, quantity, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    libro.id,
                    libro.title,
                    libro.author,
                    libro.published_date,
                    libro.isbn,
                    libro.quantity,
                    self._convertir_fecha_a_string(libro.created_at),
                    self._convertir_fecha_a_string(libro.updated_at)
                ))
            
            self.conn.commit()
            return True
        except Exception as e:
            print(f"❌ Error al guardar libros: {e}")
            return False
    
    def cargar_libros(self):
        """
        Carga la lista de libros desde la base de datos SQLite.
        
        Returns:
            list: Lista de diccionarios con datos de libros.
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute('SELECT * FROM libros')
            rows = cursor.fetchall()
            
            libros = []
            for row in rows:
                libro = {
                    'id': row['id'],
                    'title': row['title'],
                    'author': row['author'],
                    'published_date': row['published_date'],
                    'isbn': row['isbn'],
                    'quantity': row['quantity'],
                    'created_at': self._convertir_string_a_fecha(row['created_at']),
                    'updated_at': self._convertir_string_a_fecha(row['updated_at'])
                }
                libros.append(libro)
            
            return libros
        except Exception as e:
            print(f"❌ Error al cargar libros: {e}")
            return []
    
    def guardar_movimientos(self, movimientos):
        """
        Guarda la lista de movimientos en la base de datos SQLite.
        
        Args:
            movimientos (list): Lista de objetos Movement.
            
        Returns:
            bool: True si se guardó exitosamente.
        """
        try:
            cursor = self.conn.cursor()
            
            # Eliminar todos los movimientos existentes
            cursor.execute('DELETE FROM movimientos')
            
            # Insertar movimientos
            for movimiento in movimientos:
                cursor.execute('''
                    INSERT INTO movimientos (id, book_id, student_name, student_identification, 
                                          loan_date, return_date, returned, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    movimiento.id,
                    movimiento.book_id,
                    movimiento.student_name,
                    movimiento.student_identification,
                    self._convertir_fecha_a_string(movimiento.loan_date),
                    self._convertir_fecha_a_string(movimiento.return_date),
                    1 if movimiento.returned else 0,
                    self._convertir_fecha_a_string(movimiento.created_at),
                    self._convertir_fecha_a_string(movimiento.updated_at)
                ))
            
            self.conn.commit()
            return True
        except Exception as e:
            print(f"❌ Error al guardar movimientos: {e}")
            return False
    
    def cargar_movimientos(self):
        """
        Carga la lista de movimientos desde la base de datos SQLite.
        
        Returns:
            list: Lista de diccionarios con datos de movimientos.
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute('SELECT * FROM movimientos')
            rows = cursor.fetchall()
            
            movimientos = []
            for row in rows:
                movimiento = {
                    'id': row['id'],
                    'book_id': row['book_id'],
                    'student_name': row['student_name'],
                    'student_identification': row['student_identification'],
                    'loan_date': self._convertir_string_a_fecha(row['loan_date']),
                    'return_date': self._convertir_string_a_fecha(row['return_date']) if row['return_date'] else None,
                    'returned': bool(row['returned']),
                    'created_at': self._convertir_string_a_fecha(row['created_at']),
                    'updated_at': self._convertir_string_a_fecha(row['updated_at'])
                }
                movimientos.append(movimiento)
            
            return movimientos
        except Exception as e:
            print(f"❌ Error al cargar movimientos: {e}")
            return []
    
    def guardar_categorias_libros(self, categorias_libros):
        """
        Guarda las asignaciones de categorías a libros en la base de datos SQLite.
        
        Args:
            categorias_libros (dict): Diccionario con estructura {nombre_categoria: [ids_libros]}.
            
        Returns:
            bool: True si se guardó exitosamente.
        """
        try:
            cursor = self.conn.cursor()
            
            # Eliminar todas las asignaciones existentes
            cursor.execute('DELETE FROM categorias_libros')
            
            # Insertar asignaciones
            for categoria_nombre, ids_libros in categorias_libros.items():
                for libro_id in ids_libros:
                    cursor.execute('''
                        INSERT INTO categorias_libros (categoria_nombre, libro_id)
                        VALUES (?, ?)
                    ''', (categoria_nombre, libro_id))
            
            self.conn.commit()
            return True
        except Exception as e:
            print(f"❌ Error al guardar categorías de libros: {e}")
            return False
    
    def cargar_categorias_libros(self):
        """
        Carga las asignaciones de categorías a libros desde la base de datos SQLite.
        
        Returns:
            dict: Diccionario con estructura {nombre_categoria: [ids_libros]}.
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute('SELECT * FROM categorias_libros')
            rows = cursor.fetchall()
            
            categorias_libros = {}
            for row in rows:
                categoria_nombre = row['categoria_nombre']
                libro_id = row['libro_id']
                
                if categoria_nombre not in categorias_libros:
                    categorias_libros[categoria_nombre] = []
                categorias_libros[categoria_nombre].append(libro_id)
            
            return categorias_libros
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
        Obtiene estadísticas básicas de la base de datos SQLite.
        
        Returns:
            dict: Estadísticas de los datos.
        """
        try:
            cursor = self.conn.cursor()
            
            # Contar registros en cada tabla
            cursor.execute('SELECT COUNT(*) FROM usuarios')
            count_usuarios = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM libros')
            count_libros = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM movimientos')
            count_movimientos = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(DISTINCT categoria_nombre) FROM categorias_libros')
            count_categorias = cursor.fetchone()[0]
            
            estadisticas = {
                'usuarios': {
                    'existe': True,
                    'cantidad': count_usuarios
                },
                'libros': {
                    'existe': True,
                    'cantidad': count_libros
                },
                'movimientos': {
                    'existe': True,
                    'cantidad': count_movimientos
                },
                'categorias_libros': {
                    'existe': True,
                    'cantidad_categorias': count_categorias
                }
            }
            
            return estadisticas
        except Exception as e:
            print(f"❌ Error al obtener estadísticas: {e}")
            return {
                'usuarios': {'existe': False, 'cantidad': 0},
                'libros': {'existe': False, 'cantidad': 0},
                'movimientos': {'existe': False, 'cantidad': 0},
                'categorias_libros': {'existe': False, 'cantidad_categorias': 0}
            }
    
    def cerrar(self):
        """
        Cierra la conexión a la base de datos.
        """
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()
    
    def __del__(self):
        """
        Destructor que cierra la conexión al eliminar el objeto.
        """
        self.cerrar()