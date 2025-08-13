"""
Script para inicializar la base de datos
"""
from sqlalchemy import create_engine, text

def init_database():
    """Inicializa la base de datos y crea las tablas necesarias"""
    cadena_de_conexion = "sqlite:///todo.db"
    engine = create_engine(cadena_de_conexion)
    
    with engine.connect() as conn:
        # Crear tabla de tareas si no existe
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS tareas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                completa INTEGER DEFAULT 0
            )
        """))
        conn.commit()
        print("Base de datos inicializada correctamente")

if __name__ == "__main__":
    init_database()
