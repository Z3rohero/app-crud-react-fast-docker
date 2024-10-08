from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel, Field
from typing import Optional
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

# Cargar variables de entorno (para la configuración de PostgreSQL)
load_dotenv()

app = FastAPI()

# Configuración de la base de datos
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Modelo de la tabla de usuarios en la base de datos
class Task(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True, nullable=False)
    descripcion = Column(String, nullable=True)
    estado = Column(Boolean, default=False, index=True)

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Esquema de entrada para la creación de tareas
class TaskCreate(BaseModel):
    titulo: Optional[str] = Field(None, min_length=1, max_length=500)
    descripcion: Optional[str] = Field(None, min_length=1, max_length=500)
    estado: Optional[bool] = Field(None)

# Esquema de salida para las tareas
class TaskOut(BaseModel):
    id: int
    titulo: str 
    descripcion: str 
    estado: bool 

    class Config:
        orm_mode = True

# Dependencia para la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Leer todas las tareas
@app.get("/task/", response_model=list[TaskOut])
def read_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    task = db.query(Task).offset(skip).limit(limit).all()
    return task

# Crear una tarea
@app.post("/task/", response_model=TaskOut)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = Task(titulo=task.titulo, descripcion=task.descripcion, estado=task.estado)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

# Leer una tarea por ID
@app.get("/task/{task_id}", response_model=TaskOut)
def read_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return task

# Actualizar una tarea
@app.put("/task/{task_id}", response_model=TaskOut)
def update_task(task_id: int, task: TaskCreate, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
    # Actualizar solo los campos que no son None
    if task.titulo is not None:
        db_task.titulo = task.titulo
    if task.descripcion is not None:
        db_task.descripcion = task.descripcion
    if task.estado is not None:
        db_task.estado = task.estado
    
    db.commit()
    db.refresh(db_task)
    return db_task

# Eliminar una tarea
@app.delete("/task/{task_id}", response_model=TaskOut)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    db.delete(db_task)
    db.commit()
    return db_task
