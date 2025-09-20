from fastapi import HTTPException
from Base_De_Datos.database import SessionLocal
from Base_De_Datos import models
from sqlalchemy.orm import Session



# -----------------------
# Sesión de base de datos
# -----------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -----------------------
# Permisos y roles
# -----------------------
def tiene_permiso(usuario_id: int, permiso_id: int, db: Session) -> bool:
    usuario = db.query(models.UsuarioDB).filter(models.UsuarioDB.id == usuario_id).first()
    if not usuario:
        return False
    rol_id = usuario.rol_id
    rol_permiso = db.query(models.RolPermisoDB).filter(
        models.RolPermisoDB.rol_id == rol_id,
        models.RolPermisoDB.permiso_id == permiso_id
    ).first()
    return rol_permiso is not None

def es_admin(usuario: models.UsuarioDB) -> bool:
    return usuario.rol and usuario.rol.nombre.lower() == "administrador"

# -----------------------
# Validaciones comunes
# -----------------------
def get_afiliacion_or_404(afiliacion_id: int, db: Session) -> models.AfiliacionDB:
    afiliacion = db.query(models.AfiliacionDB).filter(models.AfiliacionDB.id == afiliacion_id).first()
    if not afiliacion:
        raise HTTPException(status_code=404, detail="Afiliación no encontrada")
    return afiliacion


# -----------------------

