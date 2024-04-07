from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import sqlite3

app = FastAPI()

# Modelo de datos para la tarea
class Task(BaseModel):
    name: str
    description: str

# Conexión a la base de datos SQLite
conn = sqlite3.connect('tasks.db')
c = conn.cursor()

# Crear la tabla de tareas si no existe
c.execute('''CREATE TABLE IF NOT EXISTS tasks
             (id INTEGER PRIMARY KEY, name TEXT, description TEXT)''')
conn.commit()

@app.get("/")
async def home(task_id: int):

    return {"mensaje":"hola mundo"}



# Ruta para crear una nueva tarea
@app.post("/tasks/")
async def create_task(task: Task):
    with conn:
        c.execute("INSERT INTO tasks (name, description) VALUES (?, ?)", (task.name, task.description))
        task_id = c.lastrowid
    return {"task_id": task_id, **task.dict()}

# Ruta para obtener una tarea por su ID
@app.get("/tasks/{task_id}")
async def get_task(task_id: int):
    c.execute("SELECT * FROM tasks WHERE id=?", (task_id,))
    task = c.fetchone()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"task_id": task[0], "name": task[1], "description": task[2]}

# Ruta para obtener todas las tareas
@app.get("/tasks/")
async def get_all_tasks():
    c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()
    return [{"task_id": task[0], "name": task[1], "description": task[2]} for task in tasks]

# Ruta para actualizar una tarea por su ID
@app.put("/tasks/{task_id}")
async def update_task(task_id: int, task: Task):
    with conn:
        c.execute("UPDATE tasks SET name=?, description=? WHERE id=?", (task.name, task.description, task_id))
    return {"message": "Task updated successfully"}

# Ruta para eliminar una tarea por su ID
@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    with conn:
        c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    return {"message": "Task deleted successfully"}
