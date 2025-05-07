# API REST Interfaz de aplicaciones para compartir recursos

from typing import List, Optional
import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Inicializamos una variable donde tendrá todas las características de una API REST
app = FastAPI()


# Se define el modelo
class Curso(BaseModel):
    id: Optional[str] = None
    nombre: str
    descripcion: Optional[str] = None
    nivel: str
    duracion: int

# Simularemos una base de datos
cursos_db = []


# CRUD: Read (lectura) GET ALL: Leeremos todos los cursos que haya en la db
@app.get("/cursos/", response_model=List[Curso])
def obtener_cursos():
    return cursos_db


# CRUD: Crete (escribir) Post: agregamos nuevos cursos a la BD


@app.post("/cursos/", response_model=Curso)
def crear_curso(curso: Curso):
    curso.id = str(uuid.uuid4())  # uuid genera id unicos
    cursos_db.append(curso)
    return curso


# CRUD: Read (lectura) Get(individual) Obtenemos el curso segun el id por parametros
@app.get("/cursos/{curso_id}", response_model=Curso)
def obtener_curso(curso_id: str):
    curso = next(
        (curso for curso in cursos_db if curso.id == curso_id), None
    )  # Con next tomamos la primera coincidencia del array

    if curso is None:
        raise HTTPException(status_code=404, detalle="Curso no encontrado")
    
    return curso

#CRUD Update (Actualizar/modificar) PUT: Modificar un curso que coincida con el id de parametro

@app.put("/cursos/{curso_id}", response_model=Curso)
def actualizar_curso(curso_id: str, curso_actualizado: Curso):
    curso = next(
        (curso for curso in cursos_db if curso.id == curso_id), None
    )  # Con next tomamos la primera coincidencia del array

    if curso is None:
        raise HTTPException(status_code=404, detalle="Curso no encontrado")
    
    curso_actualizado.id = curso_id
    pos= cursos_db.index(curso)  #Buscamos el indiceexacto donde esta el curso en nuestra lista
    cursos_db[pos] = curso_actualizado
    return curso_actualizado

#CRUD delete (borrar) Delete: Eliminar un curso que coincida con el id por parametros
@app.delete("/cursos/{curso_id}", response_model=Curso)
def eliminar_curso(curso_id: str):
    curso = next(
        (curso for curso in cursos_db if curso.id == curso_id), None
    )  # Con next tomamos la primera coincidencia del array

    if curso is None:
        raise HTTPException(status_code=404, detalle="Curso no encontrado")
    
    cursos_db.remove(curso)
    return curso
