from fastapi import FastAPI, HTTPException
from enum import Enum
from sqlalchemy import create_engine, Column, Integer, String, Enum as SQLAlchemyEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Set up FastAPI app
app = FastAPI()

# Define SQLAlchemy engine
SQLALCHEMY_DATABASE_URL = "sqlite:///./tasks.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define SQLAlchemy Base
Base = declarative_base()

# Define TaskStatus enum
class TaskStatus(str, Enum):
    todo = "to do"
    in_progress = "in progress"
    done = "done"

# Define SQLAlchemy Task model
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    status = Column(SQLAlchemyEnum(TaskStatus), default=TaskStatus.todo)

# Create the tasks table in the database
Base.metadata.create_all(bind=engine)

# FastAPI endpoints
@app.get("/tasks/{status}", response_model=list[Task])
def get_tasks(status: TaskStatus):
    db = SessionLocal()
    tasks = db.query(Task).filter(Task.status == status).all()
    db.close()
    return tasks

@app.get("/task/{id}", response_model=Task)
def get_task(id: int):
    db = SessionLocal()
    task = db.query(Task).filter(Task.id == id).first()
    db.close()
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task not found for ID {id}")
    return task

@app.post("/new")
def new_task(new_task: Task):
    db = SessionLocal()
    db.add(new_task)
    db.commit()
    db.close()
    return {"message": "Task created successfully"}

@app.put("/edit/{id}")
def update_task(id: int, updated_task: Task):
    db = SessionLocal()
    task = db.query(Task).filter(Task.id == id).first()
    if task:
        task.title = updated_task.title
        task.description = updated_task.description
        task.status = updated_task.status
        db.commit()
        db.close()
        return {"message": "Task updated successfully"}
    db.close()
    raise HTTPException(status_code=404, detail=f"Task not found for ID {id}")

@app.delete("/delete/{id}")
def delete_task(id: int):
    db = SessionLocal()
    task = db.query(Task).filter(Task.id == id).first()
    if task:
        db.delete(task)
        db.commit()
        db.close()
        return {"message": "Task deleted successfully"}
    db.close()
    raise HTTPException(status_code=404, detail=f"Task not found for ID {id}")
