from fastapi import FastAPI
from db import SessionDepends
from pydantic import BaseModel
from sqlalchemy import text

class ItemBase(BaseModel):
    nombre: str
    completed: int = 0

class ItemDatabase(ItemBase):
    id: int

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/mostrar_tareas")
def mostrar_tareas(db: SessionDepends):
    """
    Ruta para mostrar todas las tareas
    """
    consulta = db.execute(text("SELECT * FROM tareas"))

    tareas = []

    for tarea in consulta:
        tareas.append({"id": tarea.id, "nombre": tarea.nombre, "completa": tarea.completa})

    return tareas


@app.post("/crear_tarea")
def crear_tarea(tarea: ItemBase, db: SessionDepends):
    db.execute(text("INSERT INTO tareas (nombre, completa) VALUES (:nombre, :completa)"),
               {"nombre": tarea.nombre, "completa": tarea.completed})
    db.commit()
    return {"mensaje": "Tarea creada exitosamente"}

@app.delete("/eliminar_tarea/{tarea_id}")
def eliminar_tarea(tarea_id: int, db: SessionDepends):
    db.execute(text("DELETE FROM tareas WHERE id = :id"), {"id": tarea_id})
    db.commit()
    return {"mensaje": "Tarea eliminada exitosamente"}

@app.delete("/eliminar_todas_las_tareas")
def eliminar_todas_las_tareas(db: SessionDepends):
    db.execute(text("DELETE FROM tareas"))
    db.commit()
    return {"mensaje": "Todas las tareas eliminadas exitosamente"}

@app.put("/actualizar_tarea/{tarea_id}")
def actualizar_tarea(tarea_id: int, tarea: ItemBase, db: SessionDepends):
    db.execute(text("UPDATE tareas SET nombre = :nombre, completa = :completa WHERE id = :id"),
               {"nombre": tarea.nombre, "completa": tarea.completed, "id": tarea_id})
    db.commit()
    return {"mensaje": "Tarea actualizada exitosamente"}
