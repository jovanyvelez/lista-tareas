from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from db import SessionDepends
from pydantic import BaseModel
from sqlalchemy import text

class ItemBase(BaseModel):
    nombre: str
    completed: int = 0

class ItemDatabase(ItemBase):
    id: int

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request, db: SessionDepends):
    # Obtener todas las tareas para mostrar en la página principal
    consulta = db.execute(text("SELECT * FROM tareas"))
    tareas = []
    for tarea in consulta:
        tareas.append({"id": tarea.id, "nombre": tarea.nombre, "completa": tarea.completa})
    
    return templates.TemplateResponse("index.html", {"request": request, "tareas": tareas})


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
def crear_tarea(request: Request, db: SessionDepends, nombre: str = Form(...)):
    db.execute(text("INSERT INTO tareas (nombre, completa) VALUES (:nombre, :completa)"),
               {"nombre": nombre, "completa": 0})
    db.commit()
    
    # Devolver la lista actualizada de tareas
    consulta = db.execute(text("SELECT * FROM tareas"))
    tareas = []
    for tarea in consulta:
        tareas.append({"id": tarea.id, "nombre": tarea.nombre, "completa": tarea.completa})
    
    return templates.TemplateResponse("partials/lista_tareas.html", {"request": request, "tareas": tareas})

@app.post("/toggle_tarea/{tarea_id}")
def toggle_tarea(request: Request, tarea_id: int, db: SessionDepends):
    # Obtener el estado actual de la tarea
    resultado = db.execute(text("SELECT completa FROM tareas WHERE id = :id"), {"id": tarea_id})
    tarea = resultado.fetchone()
    
    if tarea:
        nuevo_estado = 1 if tarea.completa == 0 else 0
        db.execute(text("UPDATE tareas SET completa = :completa WHERE id = :id"),
                   {"completa": nuevo_estado, "id": tarea_id})
        db.commit()
    
    # Devolver la lista actualizada de tareas
    consulta = db.execute(text("SELECT * FROM tareas"))
    tareas = []
    for tarea in consulta:
        tareas.append({"id": tarea.id, "nombre": tarea.nombre, "completa": tarea.completa})
    
    return templates.TemplateResponse("partials/lista_tareas.html", {"request": request, "tareas": tareas})

@app.delete("/eliminar_tarea/{tarea_id}")
def eliminar_tarea(request: Request, tarea_id: int, db: SessionDepends):
    db.execute(text("DELETE FROM tareas WHERE id = :id"), {"id": tarea_id})
    db.commit()
    
    # Devolver la lista actualizada de tareas
    consulta = db.execute(text("SELECT * FROM tareas"))
    tareas = []
    for tarea in consulta:
        tareas.append({"id": tarea.id, "nombre": tarea.nombre, "completa": tarea.completa})
    
    return templates.TemplateResponse("partials/lista_tareas.html", {"request": request, "tareas": tareas})

@app.delete("/eliminar_todas_las_tareas")
def eliminar_todas_las_tareas(request: Request, db: SessionDepends):
    db.execute(text("DELETE FROM tareas"))
    db.commit()
    
    # Devolver la lista vacía
    return templates.TemplateResponse("partials/lista_tareas.html", {"request": request, "tareas": []})

@app.put("/actualizar_tarea/{tarea_id}")
def actualizar_tarea(tarea_id: int, tarea: ItemBase, db: SessionDepends):
    db.execute(text("UPDATE tareas SET nombre = :nombre, completa = :completa WHERE id = :id"),
               {"nombre": tarea.nombre, "completa": tarea.completed, "id": tarea_id})
    db.commit()
    return {"mensaje": "Tarea actualizada exitosamente"}
