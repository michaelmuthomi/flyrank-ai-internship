from typing import Optional
from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel

app = FastAPI()

tasks = [
    {"id": 1, "title": 'Clean Room', "done": True},
    {"id": 2, "title": 'Watch Documentary', "done": False},
    {"id": 3, "title": 'Finish AI Assigment', "done": False}
]

class TaskCreate(BaseModel):
    title: str

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None

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

@app.put('/tasks/{task_id}')
async def update_task(task_id: int, task_data: TaskUpdate):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    
    if task_data.title is None and task_data.done is None:
        raise HTTPException(status_code=400, detail="At least one field (title or done) must be provided")
    
    if task_data.title is not None:
        title = task_data.title.strip()
        if not title:
            raise HTTPException(status_code=400, detail="Title cannot be empty")
        task["title"] = title
        
    if task_data.done is not None:
        task["done"] = task_data.done

    return task

@app.delete('/tasks/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    
    tasks.remove(task)
    return Response(status_code=status.HTTP_204_NO_CONTENT)