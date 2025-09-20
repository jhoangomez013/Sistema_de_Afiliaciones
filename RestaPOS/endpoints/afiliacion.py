from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from Base_De_Datos.database import get_db
from Base_De_Datos import models
from schemas import Afiliacion, AfiliacionCreate, AfiliacionUpdate
from auth import get_current_user
from services import es_admin, tiene_permiso
import uuid
from typing import List

app = APIRouter()

def generar_codigo_unico() -> str:
    return f"AFL-{uuid.uuid4().hex[:8].upper()}"

def tiene_acceso_basico(usuario_id: int, db: Session) -> bool:
    permisos = db.query(models.PermisoDB).filter(models.PermisoDB.nombre.in_([
        "administrador_completo", "informador_basico"
    ])).all()
    return any(tiene_permiso(usuario_id, p.id, db) for p in permisos)

@app.post("/afiliaciones", response_model=Afiliacion)
def crear_afiliacion(
    afiliacion: AfiliacionCreate,
    db: Session = Depends(get_db),
    current_user: models.UsuarioDB = Depends(get_current_user)
):
    permiso = db.query(models.PermisoDB).filter(models.PermisoDB.nombre == "crear_afiliaciones").first()

    if not es_admin(current_user) and not (permiso and tiene_permiso(current_user.id, permiso.id, db)):
        raise HTTPException(status_code=403, detail="No tienes permiso para crear afiliaciones")

    codigo = afiliacion.codigo_unico or generar_codigo_unico()
    existente = db.query(models.AfiliacionDB).filter_by(codigo_unico=codigo).first()
    if existente:
        raise HTTPException(status_code=400, detail=f"Ya existe una afiliación con el código {codigo}")

    nueva_afiliacion = models.AfiliacionDB(
        codigo_unico=codigo,
        usuario_id=current_user.id,
        **afiliacion.dict(exclude={"codigo_unico"})
    )
    db.add(nueva_afiliacion)
    db.commit()
    db.refresh(nueva_afiliacion)
    return nueva_afiliacion

@app.get("/afiliaciones", response_model=List[Afiliacion])
def listar_afiliaciones(db: Session = Depends(get_db), current_user: models.UsuarioDB = Depends(get_current_user)):
    query = db.query(models.AfiliacionDB).options(joinedload(models.AfiliacionDB.usuario))

    if es_admin(current_user):
        return query.order_by(models.AfiliacionDB.fecha_afiliacion.desc()).all()

    permiso = db.query(models.PermisoDB).filter(models.PermisoDB.nombre == "ver_afiliaciones").first()
    if permiso and tiene_permiso(current_user.id, permiso.id, db):
        return query.filter(models.AfiliacionDB.usuario_id == current_user.id).order_by(models.AfiliacionDB.fecha_afiliacion.desc()).all()

    raise HTTPException(status_code=403, detail="No tienes permiso para ver afiliaciones")

@app.get("/afiliaciones/{afiliacion_id}", response_model=Afiliacion)
def obtener_afiliacion(afiliacion_id: int, db: Session = Depends(get_db), current_user: models.UsuarioDB = Depends(get_current_user)):
    afiliacion = db.query(models.AfiliacionDB).options(joinedload(models.AfiliacionDB.usuario)).filter(models.AfiliacionDB.id == afiliacion_id).first()
    if not afiliacion:
        raise HTTPException(status_code=404, detail="Afiliación no encontrada")

    if es_admin(current_user) or (afiliacion.usuario_id == current_user.id and tiene_acceso_basico(current_user.id, db)):
        return afiliacion

    raise HTTPException(status_code=403, detail="No tienes permiso para ver esta afiliación")

@app.put("/afiliaciones/{afiliacion_id}", response_model=Afiliacion)
def actualizar_afiliacion(afiliacion_id: int, datos: AfiliacionUpdate, db: Session = Depends(get_db), current_user: models.UsuarioDB = Depends(get_current_user)):
    afiliacion = db.query(models.AfiliacionDB).options(joinedload(models.AfiliacionDB.usuario)).filter(models.AfiliacionDB.id == afiliacion_id).first()
    if not afiliacion:
        raise HTTPException(status_code=404, detail="Afiliación no encontrada")

    if not es_admin(current_user):
        if afiliacion.usuario_id != current_user.id or not tiene_acceso_basico(current_user.id, db):
            raise HTTPException(status_code=403, detail="No tienes permiso para modificar esta afiliación")

    data = datos.dict(exclude_unset=True)
    for key, value in data.items():
        setattr(afiliacion, key, value)

    db.commit()
    db.refresh(afiliacion)
    return afiliacion

@app.delete("/afiliaciones/{afiliacion_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_afiliacion(afiliacion_id: int, db: Session = Depends(get_db), current_user: models.UsuarioDB = Depends(get_current_user)):
    afiliacion = db.query(models.AfiliacionDB).filter(models.AfiliacionDB.id == afiliacion_id).first()
    if not afiliacion:
        raise HTTPException(status_code=404, detail="Afiliación no encontrada")

    if not es_admin(current_user):
        raise HTTPException(status_code=403, detail="Solo administradores pueden eliminar afiliaciones")

    db.delete(afiliacion)
    db.commit()
    return {"message": "Afiliación eliminada"}