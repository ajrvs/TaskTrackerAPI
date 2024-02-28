from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enum import Enum

app = FastAPI()

class TaskStatus(str, Enum):
    todo = "to do"
    in_progress = "in progress"
    done = "done"

class Task(BaseModel):
    title: str
    description: str
    status: TaskStatus = TaskStatus.todo

tasks = []

@app.get("/")
def home():
    return {"message": "Welcome to Task Tracker API"}

@app.get("/tasks/{status}", response_model=list[Task])
def get_tasks(status: TaskStatus):
    filtered_tasks = [task for task in tasks if task.status == status]
    return filtered_tasks

@app.get("/task/{id}", response_model=Task)
def get_task(id: int):
    if id < len(tasks):
        return tasks[id]
    else:
        raise HTTPException(status_code=404, detail=f"Task not found for ID {id}")

@app.post("/new")
def new_task(new_task: Task):
    tasks.append(new_task)
    return {"message": "Task created successfully"}

@app.put("/edit/{id}")
def update_task(id:int, updated_task: Task):
    if id < len(tasks):
        tasks[id] = updated_task
    else:
        raise HTTPException(status_code=404, detail=f"Task not found for ID {id}")

@app.delete("/delete/{id}")
def delete_task(id: int):
    if id < len(tasks):
        del tasks[id]
        return {"message": "Task deleted"}
    else:
        raise HTTPException(status_code=404, detail=f"Task not found for ID {id}")

