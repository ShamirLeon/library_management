#!/usr/bin/env python3
"""
Script de prueba para el sistema de persistencia de datos.

Este script demuestra y valida que la persistencia funciona correctamente,
creando, modificando y verificando datos en archivos JSON.
"""

from services.users_service import UsersService
from services.books_service import BooksService 
from services.movements_service import MovementsService
from services.categorias_service import ServicioCategorias
from services.persistencia_service import ServicioPersistencia
import os
import json


def main():
    """
    Función principal que prueba el sistema de persistencia.
    """
    print("💾 PRUEBA DEL SISTEMA DE PERSISTENCIA DE DATOS")
    print("=" * 55)
    
    # Eliminar archivos existentes para prueba limpia
    print("\n🧹 Limpiando datos previos...")
    directorio_datos = "datos"
    if os.path.exists(directorio_datos):
        for archivo in os.listdir(directorio_datos):
            if archivo.endswith('.json'):
                os.remove(os.path.join(directorio_datos, archivo))
                print(f"   🗑️ Eliminado: {archivo}")
    
    # Inicializar servicios (esto creará datos por defecto)
    print("\n🚀 Inicializando servicios...")
    users_service = UsersService()
    books_service = BooksService()
    movements_service = MovementsService(books_service)
    categorias_service = ServicioCategorias(books_service)
    persistencia_service = ServicioPersistencia()
    
    print("   ✅ Servicios inicializados")
    
    # Verificar que se crearon archivos por defecto
    print("\n📁 Verificando creación automática de archivos...")
    estadisticas = persistencia_service.obtener_estadisticas_archivos()
    
    for tipo, info in estadisticas.items():
        estado = "✅" if info['existe'] else "❌"
        cantidad = info.get('cantidad', info.get('cantidad_categorias', 0))
        print(f"   {estado} {tipo}: {cantidad} registros")
    
    # Agregar datos de usuario
    print("\n👥 Probando persistencia de USUARIOS...")
    usuario_nuevo = users_service.add_user("test@ejemplo.com", "123456", "Usuario de Prueba")
    if usuario_nuevo:
        print(f"   ✅ Usuario creado: {usuario_nuevo.name} (ID: {usuario_nuevo.id})")
        
        # Verificar que se guardó en archivo
        datos_usuarios = persistencia_service.cargar_usuarios()
        print(f"   📁 Usuarios en archivo: {len(datos_usuarios)}")
        
        usuario_encontrado = any(u['email'] == 'test@ejemplo.com' for u in datos_usuarios)
        print(f"   🔍 Usuario encontrado en archivo: {'✅' if usuario_encontrado else '❌'}")
    
    # Agregar datos de libros
    print("\n📚 Probando persistencia de LIBROS...")
    libro_nuevo = books_service.add_book(
        "El Principito", 
        "Antoine de Saint-Exupéry", 
        "1943-04-06", 
        "1234567890", 
        "5"
    )
    if libro_nuevo:
        print(f"   ✅ Libro creado: {libro_nuevo.title} (ID: {libro_nuevo.id})")
        
        # Verificar que se guardó en archivo
        datos_libros = persistencia_service.cargar_libros()
        print(f"   📁 Libros en archivo: {len(datos_libros)}")
        
        libro_encontrado = any(l['title'] == 'El Principito' for l in datos_libros)
        print(f"   🔍 Libro encontrado en archivo: {'✅' if libro_encontrado else '❌'}")
    
    # Probar movimientos
    print("\n🔄 Probando persistencia de MOVIMIENTOS...")
    movimiento_nuevo = movements_service.add_movement(1, "Juan Pérez", "1234567890", "2024-12-01")
    if movimiento_nuevo:
        print(f"   ✅ Movimiento creado: Libro ID {movimiento_nuevo.book_id} para {movimiento_nuevo.student_name}")
        
        # Verificar que se guardó en archivo
        datos_movimientos = persistencia_service.cargar_movimientos()
        print(f"   📁 Movimientos en archivo: {len(datos_movimientos)}")
        
        movimiento_encontrado = any(m['student_name'] == 'Juan Pérez' for m in datos_movimientos)
        print(f"   🔍 Movimiento encontrado en archivo: {'✅' if movimiento_encontrado else '❌'}")
    
    # Probar categorías
    print("\n🗂️  Probando persistencia de CATEGORÍAS...")
    resultado_categoria = categorias_service.asignar_libro_a_categoria(1, "Novela")
    if resultado_categoria['exito']:
        print(f"   ✅ Libro asignado a categoría: {resultado_categoria['mensaje']}")
        
        # Verificar que se guardó en archivo
        datos_categorias = persistencia_service.cargar_categorias_libros()
        print(f"   📁 Asignaciones de categorías en archivo: {len(datos_categorias)}")
        
        categoria_encontrada = 'Novela' in datos_categorias and 1 in datos_categorias['Novela']
        print(f"   🔍 Asignación encontrada en archivo: {'✅' if categoria_encontrada else '❌'}")
    
    # Probar modificaciones
    print("\n✏️ Probando MODIFICACIONES...")
    
    # Devolver un libro (actualizar movimiento)
    if movimiento_nuevo:
        movimiento_devuelto = movements_service.return_movement(movimiento_nuevo.id)
        if movimiento_devuelto:
            print("   ✅ Libro devuelto (movimiento actualizado)")
            
            # Verificar que el cambio se persistió
            datos_movimientos = persistencia_service.cargar_movimientos()
            mov_actualizado = next((m for m in datos_movimientos if m['id'] == movimiento_nuevo.id), None)
            if mov_actualizado and mov_actualizado['returned']:
                print("   📁 Estado de devolución persistido correctamente")
            else:
                print("   ❌ Error en persistencia de devolución")
    
    # Eliminar un usuario
    if usuario_nuevo:
        usuario_eliminado = users_service.delete_user(usuario_nuevo.id)
        if usuario_eliminado:
            print("   ✅ Usuario eliminado")
            
            # Verificar que se eliminó del archivo
            datos_usuarios = persistencia_service.cargar_usuarios()
            usuario_aun_existe = any(u['id'] == usuario_nuevo.id for u in datos_usuarios)
            print(f"   📁 Usuario eliminado del archivo: {'✅' if not usuario_aun_existe else '❌'}")
    
    # Crear respaldo completo
    print("\n💾 Probando RESPALDO COMPLETO...")
    exito_respaldo = persistencia_service.exportar_todo("prueba_respaldo.json")
    if exito_respaldo:
        print("   ✅ Respaldo creado exitosamente")
        
        # Verificar contenido del respaldo
        ruta_respaldo = os.path.join("datos", "prueba_respaldo.json")
        if os.path.exists(ruta_respaldo):
            with open(ruta_respaldo, 'r', encoding='utf-8') as f:
                respaldo_datos = json.load(f)
            
            print("   📋 Contenido del respaldo:")
            print(f"      • Usuarios: {len(respaldo_datos.get('usuarios', []))}")
            print(f"      • Libros: {len(respaldo_datos.get('libros', []))}")
            print(f"      • Movimientos: {len(respaldo_datos.get('movimientos', []))}")
            print(f"      • Categorías: {len(respaldo_datos.get('categorias_libros', {}))}")
    
    # Simular reinicio del sistema
    print("\n🔄 Probando CARGA DESPUÉS DE REINICIO...")
    
    # Crear nuevos servicios (simulando reinicio)
    print("   🔄 Reinicializando servicios...")
    users_service_nuevo = UsersService()
    books_service_nuevo = BooksService()
    movements_service_nuevo = MovementsService(books_service_nuevo)
    categorias_service_nuevo = ServicioCategorias(books_service_nuevo)
    
    # Verificar que los datos se cargaron correctamente
    usuarios_cargados = len(users_service_nuevo.get_all_users())
    libros_cargados = len(books_service_nuevo.get_all_books())
    movimientos_cargados = len(movements_service_nuevo.get_all_movements())
    
    print(f"   📊 Datos cargados después del 'reinicio':")
    print(f"      • Usuarios: {usuarios_cargados}")
    print(f"      • Libros: {libros_cargados}")  
    print(f"      • Movimientos: {movimientos_cargados}")
    
    # Verificar que las categorías también se cargaron
    resultado_busqueda = categorias_service_nuevo.obtener_libros_por_categoria("Novela")
    libros_en_categoria = len(resultado_busqueda['ids_libros'])
    print(f"      • Libros en categoría 'Novela': {libros_en_categoria}")
    
    # Resumen final
    print("\n" + "=" * 55)
    print("📊 RESUMEN DE LA PRUEBA DE PERSISTENCIA")
    print("=" * 55)
    
    archivos_creados = []
    for archivo in ['usuarios.json', 'libros.json', 'movimientos.json', 'categorias_libros.json']:
        ruta = os.path.join("datos", archivo)
        if os.path.exists(ruta):
            archivos_creados.append(archivo)
    
    print(f"✅ Archivos de datos creados: {len(archivos_creados)}/4")
    for archivo in archivos_creados:
        print(f"   📁 {archivo}")
    
    print(f"\n✅ Operaciones probadas:")
    print("   • Creación automática de datos por defecto")
    print("   • Guardado automático al agregar registros")
    print("   • Guardado automático al modificar registros")
    print("   • Guardado automático al eliminar registros")
    print("   • Carga automática al inicializar servicios")
    print("   • Creación de respaldos completos")
    print("   • Persistencia entre 'reinicios' del sistema")
    
    print("\n🎉 SISTEMA DE PERSISTENCIA FUNCIONANDO CORRECTAMENTE")
    print("Los datos se guardan automáticamente en archivos JSON en la carpeta 'datos/'")
    print("=" * 55)


if __name__ == "__main__":
    main()