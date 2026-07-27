from fastapi import FastAPI,HTTPException
app = FastAPI()

tasks = [
    {"id": 1, "title": 'Clean Room', "done": True},
    {"id": 2, "title": 'Watch Documentary', "done": False},
    {"id": 3, "title": 'Finish AI Assigment', "done": False}
]

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