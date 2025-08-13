# Lista de Tareas - Proyecto Educativo

Un proyecto básico de lista de tareas para aprender FastAPI, HTMX y Bootstrap con arquitectura limpia y buenas prácticas.

## Tecnologías Utilizadas

- **FastAPI**: Framework web de Python
- **SQLite**: Base de datos simple 
- **HTMX**: Para interactividad web sin JavaScript
- **Bootstrap**: Para estilos básicos
- **Jinja2**: Templates HTML
- **SQLAlchemy**: Solo para conexiones (sin ORM, SQL directo)

## Pasos para Ejecutar

1. Instalar dependencias:
```bash
uv sync
```

2. Crear la base de datos:
```bash
uv run python init_db.py
```

3. Ejecutar el servidor:
```bash
uv run uvicorn main:app --reload
```

4. Abrir en navegador: `http://127.0.0.1:8000`

## Rutas Disponibles

### Rutas Web (HTML)
- `GET /` - Página principal de la aplicación
- `GET /editar_tarea/{id}` - Formulario de edición

### Rutas API (JSON)
- `GET /mostrar_tareas` - Lista todas las tareas en JSON
- `POST /crear_tarea` - Crear nueva tarea (desde formulario)
- `PUT /actualizar_tarea/{id}` - Actualizar tarea (desde formulario)
- `DELETE /eliminar_tarea/{id}` - Eliminar tarea específica
- `DELETE /eliminar_todas_las_tareas` - Eliminar todas las tareas
- `POST /toggle_tarea/{id}` - Cambiar estado completado/pendiente

### Documentación Automática
- `http://127.0.0.1:8000/docs` - Swagger UI
- `http://127.0.0.1:8000/redoc` - ReDoc

## Funciones de la Aplicación

- ✅ Agregar nuevas tareas
- ✅ Marcar tareas como completadas
- ✅ Editar el texto de las tareas
- ✅ Eliminar tareas individuales
- ✅ Eliminar todas las tareas

## Estructura Básica

```
lista-tareas/
├── main.py              # Aplicación principal con rutas HTTP
├── db.py               # Configuración base de datos
├── init_db.py          # Crear tablas
├── templates/
│   └── index.html      # Template principal
├── main_original.py    # Backup del código original (solo API)
├── main_backup.py      # Backup de versión anterior
└── pyproject.toml      # Dependencias
```

## Arquitectura del Código

### Funciones Helper (Capa de Base de Datos)
El código está organizado con **separación de responsabilidades**:

- `obtener_todas_las_tareas()` - SELECT de todas las tareas
- `crear_nueva_tarea()` - INSERT de nueva tarea
- `eliminar_tarea_por_id()` - DELETE por ID
- `eliminar_todas_las_tareas_db()` - DELETE todas
- `obtener_tarea_por_id()` - SELECT por ID específico
- `actualizar_nombre_tarea()` - UPDATE nombre
- `toggle_estado_tarea()` - UPDATE estado completado

### Rutas FastAPI (Capa Web)
Las rutas HTTP se enfocan solo en:
- Recibir parámetros HTTP
- Llamar a funciones helper
- Devolver respuestas HTML/JSON

## Para Aprender

Este proyecto enseña conceptos fundamentales:

### 1. **Backend Web**
- Rutas HTTP básicas (GET, POST, DELETE, PUT)
- Formularios HTML y procesamiento
- Respuestas JSON vs HTML
- Templates con Jinja2

### 2. **Base de Datos**
- Consultas SQL directas (sin ORM)
- Operaciones CRUD completas
- Manejo de conexiones con SQLAlchemy
- Base de datos SQLite

### 3. **Frontend Interactivo**
- HTMX para interactividad sin JavaScript
- Bootstrap para estilos responsivos
- Formularios dinámicos
- Actualización de contenido en tiempo real

### 4. **Buenas Prácticas**
- **Separación de responsabilidades**: Web vs Base de datos
- **Funciones helper**: Código reutilizable y limpio
- **DRY (Don't Repeat Yourself)**: Evitar duplicación
- **Documentación**: Docstrings en todas las funciones
- **Arquitectura limpia**: Fácil de entender y mantener

### 5. **Conceptos Avanzados (Opcionales)**
- Patrón Repository (implícito en las funciones helper)
- Separación en capas (Web, Lógica de negocio, Datos)
- Testing unitario (las funciones helper son fáciles de testear)
- Escalabilidad (fácil mover helpers a módulos separados)

## Evolución del Proyecto

El proyecto incluye diferentes versiones para mostrar la evolución:

1. **`main_original.py`**: Solo API JSON (código inicial)
2. **`main_backup.py`**: Versión con templates pero código repetitivo
3. **`main.py`**: Versión final con arquitectura limpia y funciones helper

Esto permite a los estudiantes ver cómo **refactorizar** y **mejorar** el código.

## Características Técnicas

- ✅ **Sin JavaScript personalizado**: Solo HTMX
- ✅ **SQL directo**: Sin ORM, aprendizaje puro de SQL
- ✅ **Responsive**: Bootstrap 5 para móviles
- ✅ **Hot reload**: Desarrollo ágil con `fastapi dev`
- ✅ **Arquitectura limpia**: Separación clara de responsabilidades
- ✅ **Código educativo**: Comentarios y nombres descriptivos
- ✅ **Escalable**: Fácil agregar nuevas funcionalidades

## Ejercicios Propuestos

Para continuar aprendiendo, los estudiantes pueden:

### Nivel Básico
1. **Agregar fecha de creación** a las tareas
2. **Ordenar tareas** por fecha o alfabéticamente
3. **Agregar prioridades** (Alta, Media, Baja)
4. **Contar tareas** completadas vs pendientes

### Nivel Intermedio
5. **Mover funciones helper** a un archivo `database.py`
6. **Agregar validaciones** (tarea no vacía, máximo caracteres)
7. **Crear tests unitarios** para las funciones helper
8. **Agregar categorías** a las tareas

### Nivel Avanzado
9. **Autenticación de usuarios** con sesiones
10. **Base de datos PostgreSQL** en lugar de SQLite
11. **API REST completa** con paginación
12. **Frontend con JavaScript** (React, Vue, etc.)

## Comandos Útiles

```bash
# Desarrollo
uv run fastapi dev main.py

# Producción  
uv run uvicorn main:app --host 0.0.0.0 --port 8000

# Resetear base de datos
rm todo.db && uv run python init_db.py

# Ver logs detallados
uv run uvicorn main:app --reload --log-level debug
```
