from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from typing import List

from Base_De_Datos.database import SessionLocal
from Base_De_Datos import models
from schemas import Usuario, UsuarioCreate, UsuarioUpdate
from auth import get_current_user
from services import tiene_permiso, es_admin

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
app = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# GET /usuarios - Lista todos los usuarios si se tiene permiso
@app.get("/usuarios", response_model=List[Usuario])
def get_usuarios(db: Session = Depends(get_db), current_user: models.UsuarioDB = Depends(get_current_user)):
    permiso = db.query(models.PermisoDB).filter(models.PermisoDB.nombre.in_([
        "administrador_completo", "ver_usuarios"
    ])).first()

    if not es_admin(current_user) and not (permiso and tiene_permiso(current_user.id, permiso.id, db)):
        raise HTTPException(status_code=403, detail="No tienes permiso para ver la lista de usuarios")

    return db.query(models.UsuarioDB).all()

# POST /usuarios - Crea un nuevo usuario
@app.post("/usuarios", status_code=status.HTTP_201_CREATED)
def create_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db), current_user: models.UsuarioDB = Depends(get_current_user)):
    permiso = db.query(models.PermisoDB).filter(models.PermisoDB.nombre.in_([
        "administrador_completo", "crear_usuarios"
    ])).first()

    if not es_admin(current_user) and not (permiso and tiene_permiso(current_user.id, permiso.id, db)):
        raise HTTPException(status_code=403, detail="No tienes permiso para crear usuarios")
    
    existing = db.query(models.UsuarioDB).filter(models.UsuarioDB.email == usuario.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    rol = db.query(models.RolDB).filter(models.RolDB.id == usuario.rol_id).first()
    if not rol:
        raise HTTPException(status_code=400, detail="El rol especificado no existe")

    hashed_password = pwd_context.hash(usuario.password)
    payload = usuario.dict(exclude={"password"})
    db_usuario = models.UsuarioDB(**payload, password=hashed_password)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return {"message": "Usuario creado", "id": db_usuario.id}

# GET /usuarios/me - Info del usuario actual
@app.get("/usuarios/me")
def read_users_me(current_user: models.UsuarioDB = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "nombre": current_user.nombre,
        "apellido": current_user.apellido,
        "rol_id": current_user.rol_id,
        "oficina": current_user.oficina,
    }

# GET /usuarios/{id} - Info de un usuario específico
@app.get("/usuarios/{id}", response_model=Usuario)
def get_usuario(id: int, db: Session = Depends(get_db), current_user: models.UsuarioDB = Depends(get_current_user)):
    if current_user.id == id or es_admin(current_user):
        user = db.query(models.UsuarioDB).filter(models.UsuarioDB.id == id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return user

    permiso = db.query(models.PermisoDB).filter(models.PermisoDB.nombre.in_([
        "administrador_completo", "ver_usuarios"
    ])).first()

    if permiso and tiene_permiso(current_user.id, permiso.id, db):
        user = db.query(models.UsuarioDB).filter(models.UsuarioDB.id == id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return user

    raise HTTPException(status_code=403, detail="No tienes permiso para ver esta información")

# PUT /usuarios/{id} - Actualiza su propia cuenta o si es admin
@app.put("/usuarios/{id}")
def update_usuario(id: int, usuario: UsuarioUpdate, db: Session = Depends(get_db), current_user: models.UsuarioDB = Depends(get_current_user)):
    if current_user.id != id and not es_admin(current_user):
        raise HTTPException(status_code=403, detail="No tienes permiso para actualizar a este usuario")

    db_usuario = db.query(models.UsuarioDB).filter(models.UsuarioDB.id == id).first()
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    data = usuario.dict(exclude_unset=True)
    if "password" in data and data["password"]:
        data["password"] = pwd_context.hash(data["password"])

    for k, v in data.items():
        setattr(db_usuario, k, v)

    db.commit()
    db.refresh(db_usuario)
    return {"message": "Usuario actualizado"}

# DELETE /usuarios/{id} - Elimina su propia cuenta o si es admin
@app.delete("/usuarios/{id}")
def delete_usuario(id: int, db: Session = Depends(get_db), current_user: models.UsuarioDB = Depends(get_current_user)):
    permiso = db.query(models.PermisoDB).filter(models.PermisoDB.nombre.in_([
        "administrador_completo", "eliminar_usuarios"
    ])).first()

    if current_user.id != id and not es_admin(current_user) and not (permiso and tiene_permiso(current_user.id, permiso.id, db)):
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar esta cuenta")

    db_usuario = db.query(models.UsuarioDB).filter(models.UsuarioDB.id == id).first()
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db.delete(db_usuario)
    db.commit()
    return {"message": "Usuario eliminado"}

@app.get("/usuarios/me/permisos")
def get_mis_permisos(db: Session = Depends(get_db), current_user: models.UsuarioDB = Depends(get_current_user)):
    rol_permisos = db.query(models.RolPermisoDB).filter(models.RolPermisoDB.rol_id == current_user.rol_id).all()
    permisos = [
        db.query(models.PermisoDB).filter(models.PermisoDB.id == rp.permiso_id).first().nombre
        for rp in rol_permisos
    ]

    return {
        "id": current_user.id,
        "email": current_user.email,
        "rol": current_user.rol.nombre if current_user.rol else None,
        "permisos": permisos
    }



