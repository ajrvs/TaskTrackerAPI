from fastapi import FastAPI, HTTPException, Path, Response
from pydantic import BaseModel
from enum import Enum
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import sessionmaker

app = FastAPI()

SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class TaskStatus(str, Enum):
    todo = "to do"
    in_progress = "in progress"
    done = "done"

class Task(BaseModel):
    id: int
    title: str
    description: str
    status: TaskStatus

# Define the SQLAlchemy table
class TaskTable(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    status = Column(SQLAlchemyEnum(TaskStatus), default=TaskStatus.todo)


@app.get("/", description="Home endpoint returns a welcome message to indicate that the Task Management System is operational.")
def home():
    return {"message": "Welcome to the Task Management System!"}

@app.get("/tasks/{status}", description="Tasks endpoint returns a list of tasks filtered by status.")
def filter_tasks(status: TaskStatus = Path(..., title="The status of the tasks to filter")):
    # filtered_tasks = [task for task in tasks if task.status == status]
    # return filtered_tasks
    db = SessionLocal()
    tasks = db.query(Task).filter(Task.status == status).all()
    db.close()
    if not tasks:
        raise HTTPException(status_code=404, detail="Task wth specified status does not exist")
    return tasks

@app.get("/task/{task_id}", description="Task endpoint returns a specific task identified by its ID.")
def get_task(task_id: int = Path(..., title="The ID of the task to retrieve", ge=0)):
    # if task_id < len(tasks):
    #     return tasks[task_id]
    # else:
    #     raise HTTPException(status_code=404, detail="Task wth specified ID does not exist")
    db = SessionLocal()
    try:
        task = db.query(Task).filter(Task.id == task_id).first()  # Fix the typo in the query line
    finally:
        db.close()
    if task is None:
        raise HTTPException(status_code=404, detail="Task wth specified ID does not exist")
    return task

@app.post("/new", description="New endpoint returns a message indicating that a new task has been created.", response_model=None)
def new_task(new_task: Task):
    # tasks.append(new_task)
    # return {"message": "Task created successfully"}
    db = SessionLocal()
    db.add(new_task)
    db.commit()
    db.close()
    return {"message": "Task created successfully"}

@app.put("/edit/{task_id}", description="Edit endpoint returns a message indicating successful updation of task or raises an exception if task ID specified is not found.")
def edit_task(updated_task: Task, task_id: int = Path(..., title="The ID of the task to edit", ge=0)):
    # if task_id < len(tasks):
    #     tasks[task_id] = updated_task
    #     return {"message": "Task updated successfully"}
    # else:
    #     raise HTTPException(status_code=404, detail="Task with specified ID does not exist")
    db = SessionLocal()
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        task.title = updated_task.title
        task.description = updated_task.description
        task.status = updated_task.status
        db.commit()
        db.close()
        return {"message": "Task updated successfully"}
    db.close()
    raise HTTPException(status_code=404, detail="Task wth specified ID does not exist")

@app.delete("/delete/{task_id}", description="Delete endpoint returns a message indicating successful deletion of task or raises an exception if task ID specified is not found.")
def delete_task(task_id: int):
    # if task_id < len(tasks):
    #     del tasks[task_id]
    #     return {"message": "Task deleted successfully"}
    # else:
    #     raise HTTPException(status_code=404, detail="Task not found")
    db = SessionLocal()
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        db.delete(task)
        db.commit()
        db.close()
        return {"message": "Task deleted successfully"}
    db.close()
    raise HTTPException(status_code=404, detail="Task wth specified ID does not exist")