import string
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
app = FastAPI()

tasks = [
    {"id": 1, "title": 'Clean Room', "done": True},
    {"id": 2, "title": 'Watch Documentary', "done": False},
    {"id": 3, "title": 'Finish AI Assigment', "done": False}
]
class TaskCreate(BaseModel):
    title: str
@app.get("/")
async def root():
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }

@app.get('/health')
async def health():
    return {'status': 'ok'}

@app.get('/tasks')
async def get_tasks():
    return tasks

@app.get('/tasks/{task_id}')
async def get_task(task_id: int):
    # Search the list for a task with matching id
    task = next((t for t in tasks if t["id"] == task_id), None)
    
    if task:
        return task
    
    # Raise a standard 404 HTTP Exception
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

@app.post('/tasks', status_code=201)
async def add_task(task_data: TaskCreate):
    title = task_data.title.strip()
    if not title:
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    
    new_id = (tasks[-1]["id"] + 1) if tasks else 1
    new_task = {"id": new_id, "title": title, "done": False}
    tasks.append(new_task)
    return new_task