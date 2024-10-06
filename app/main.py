from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel, Field, validator
import os
from dotenv import load_dotenv

# Cargar variables de entorno (para la configuración de PostgreSQL)
load_dotenv()

app = FastAPI()

# Configuración de la base de datos
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelo de la tabla de usuarios en la base de datos
class Task(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True, nullable=False)
    descripcion = Column(String, nullable=True)
    estado = Column(Boolean, default=False, index=True)

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Esquema de entrada para la creación de usuarios
class TaskCreate(BaseModel):
    titulo: str = Field(..., min_length=10, max_length=500)
    descripcion: str = Field(..., min_length=10, max_length=500)
    estado: bool = Field(...)

# Esquema de salida para los usuarios
class TaskOut(BaseModel):
    id: int
    titulo: str
    descripcion: str
    estado:bool

    class Config:
        orm_mode = True

# Dependencia para la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Leer todos los usuarios
@app.get("/task/", response_model=list[TaskOut])
def read_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    task = db.query(Task).offset(skip).limit(limit).all()
    return task


# Crear una tarea
@app.post("/task/", response_model=TaskOut)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = Task(titulo=task.titulo,descripcion=task.descripcion,estado=task.estado)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task



'''


# Leer un usuario por ID
@app.get("/users/{user_id}", response_model=UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Actualizar un usuario
@app.put("/users/{user_id}", response_model=UserOut)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.name = user.name
    db_user.email = user.email
    db.commit()
    db.refresh(db_user)
    return db_user

# Eliminar un usuario
@app.delete("/users/{user_id}", response_model=UserOut)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return db_user


'''