from typing import Annotated
from fastapi import Depends
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session



cadena_de_conexion = f"sqlite:///todo.db"

connect_args = {"check_same_thread": False}

engine = create_engine(cadena_de_conexion, connect_args=connect_args)

SessionLocal = sessionmaker(
    autocommit=False,    # NO guardar cambios automáticamente (más control)
    autoflush=False,     # NO enviar cambios automáticamente a la BD
    bind=engine          # Usar nuestro motor para las conexiones
)

def get_db():
    with SessionLocal() as session:
        yield session

SessionDepends = Annotated[Session, Depends(get_db)]