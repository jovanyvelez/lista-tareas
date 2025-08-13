from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from db import SessionDepends
from sqlalchemy import text

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def obtener_todas_las_tareas(db: SessionDepends):
    """Función helper para obtener todas las tareas"""
    consulta = db.execute(text("SELECT * FROM tareas"))
    tareas = []
    for tarea in consulta:
        tareas.append({"id": tarea.id, "nombre": tarea.nombre, "completa": tarea.completa})
    return tareas

def crear_nueva_tarea(db: SessionDepends, nombre: str):
    """Función helper para crear una nueva tarea"""
    db.execute(text("INSERT INTO tareas (nombre, completa) VALUES (:nombre, :completa)"),
               {"nombre": nombre, "completa": 0})
    db.commit()

def eliminar_tarea_por_id(db: SessionDepends, tarea_id: int):
    """Función helper para eliminar una tarea específica"""
    db.execute(text("DELETE FROM tareas WHERE id = :id"), {"id": tarea_id})
    db.commit()

def eliminar_todas_las_tareas_db(db: SessionDepends):
    """Función helper para eliminar todas las tareas"""
    db.execute(text("DELETE FROM tareas"))
    db.commit()

def obtener_tarea_por_id(db: SessionDepends, tarea_id: int):
    """Función helper para obtener una tarea específica por su ID"""
    resultado = db.execute(text("SELECT * FROM tareas WHERE id = :id"), {"id": tarea_id})
    return resultado.fetchone()

def actualizar_nombre_tarea(db: SessionDepends, tarea_id: int, nombre: str):
    """Función helper para actualizar el nombre de una tarea"""
    db.execute(text("UPDATE tareas SET nombre = :nombre WHERE id = :id"),
               {"nombre": nombre, "id": tarea_id})
    db.commit()

def toggle_estado_tarea(db: SessionDepends, tarea_id: int):
    """Función helper para cambiar el estado de completado de una tarea"""
    resultado = db.execute(text("SELECT completa FROM tareas WHERE id = :id"), {"id": tarea_id})
    tarea = resultado.fetchone()
    
    if tarea:
        nuevo_estado = 1 if tarea.completa == 0 else 0
        db.execute(text("UPDATE tareas SET completa = :completa WHERE id = :id"),
                   {"completa": nuevo_estado, "id": tarea_id})
        db.commit()
        return True
    return False

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request, db: SessionDepends):
    """Página principal con todas las tareas"""
    tareas = obtener_todas_las_tareas(db)
    return templates.TemplateResponse("index.html", {"request": request, "tareas": tareas})

@app.get("/mostrar_tareas")
def mostrar_tareas(db: SessionDepends):
    """API endpoint que devuelve todas las tareas en formato JSON"""
    return obtener_todas_las_tareas(db)

@app.post("/crear_tarea")
def crear_tarea(request: Request, db: SessionDepends, nombre: str = Form(...)):
    """Crear una nueva tarea"""
    crear_nueva_tarea(db, nombre)
    tareas = obtener_todas_las_tareas(db)
    return templates.TemplateResponse("index.html", {"request": request, "tareas": tareas})

@app.delete("/eliminar_tarea/{tarea_id}")
def eliminar_tarea(request: Request, tarea_id: int, db: SessionDepends):
    """Eliminar una tarea específica"""
    eliminar_tarea_por_id(db, tarea_id)
    tareas = obtener_todas_las_tareas(db)
    return templates.TemplateResponse("index.html", {"request": request, "tareas": tareas})

@app.delete("/eliminar_todas_las_tareas")
def eliminar_todas_las_tareas(request: Request, db: SessionDepends):
    """Eliminar todas las tareas"""
    eliminar_todas_las_tareas_db(db)
    return templates.TemplateResponse("index.html", {"request": request, "tareas": []})

@app.get("/editar_tarea/{tarea_id}", response_class=HTMLResponse)
def editar_tarea(request: Request, tarea_id: int, db: SessionDepends):
    """Mostrar formulario de edición para una tarea"""
    tarea = obtener_tarea_por_id(db, tarea_id)
    tareas = obtener_todas_las_tareas(db)
    
    if not tarea:
        # Si no existe la tarea, mostrar la página normal
        return templates.TemplateResponse("index.html", {"request": request, "tareas": tareas})
    
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "tareas": tareas,
        "editando": {"id": tarea.id, "nombre": tarea.nombre}
    })

@app.put("/actualizar_tarea/{tarea_id}")
def actualizar_tarea(request: Request, tarea_id: int, db: SessionDepends, nombre: str = Form(...)):
    """Actualizar el nombre de una tarea"""
    actualizar_nombre_tarea(db, tarea_id, nombre)
    tareas = obtener_todas_las_tareas(db)
    return templates.TemplateResponse("index.html", {"request": request, "tareas": tareas})

@app.post("/toggle_tarea/{tarea_id}")
def toggle_tarea(request: Request, tarea_id: int, db: SessionDepends):
    """Cambiar el estado de completado de una tarea"""
    toggle_estado_tarea(db, tarea_id)
    tareas = obtener_todas_las_tareas(db)
    return templates.TemplateResponse("index.html", {"request": request, "tareas": tareas})
