from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session, joinedload
from io import BytesIO
import pandas as pd
from datetime import timezone
from zoneinfo import ZoneInfo

from Base_De_Datos.database import get_db
from Base_De_Datos import models
from auth import get_current_user
from services import es_admin, tiene_permiso

router = APIRouter()

def formato_fecha_para_csv(dt):
    if dt is None:
        return None
    try:
        if dt.tzinfo is None:
            dt_utc = dt.replace(tzinfo=timezone.utc)
        else:
            dt_utc = dt.astimezone(timezone.utc)
        bogota = ZoneInfo("America/Bogota")
        dt_local = dt_utc.astimezone(bogota)
        return dt_local.strftime("%Y-%m-%d %H:%M:%S%z")[:-2] + ":" + dt_local.strftime("%z")[-2:]
    except Exception:
        return str(dt)

@router.get("/reportes/afiliaciones/csv")
def exportar_afiliaciones_csv(db: Session = Depends(get_db), current_user: models.UsuarioDB = Depends(get_current_user)):
    permiso = db.query(models.PermisoDB).filter(models.PermisoDB.nombre.in_([
        "administrador_completo", "descargar_informes"
    ])).first()

    if not es_admin(current_user) and not (permiso and tiene_permiso(current_user.id, permiso.id, db)):
        raise HTTPException(status_code=403, detail="No tienes permiso para exportar reportes")

    query = db.query(models.AfiliacionDB).options(joinedload(models.AfiliacionDB.usuario))

    if es_admin(current_user):
        afiliaciones = query.all()
    else:
        afiliaciones = query.filter(models.AfiliacionDB.usuario_id == current_user.id).all()

    if not afiliaciones:
        raise HTTPException(status_code=404, detail="No hay afiliaciones registradas")

    data = []
    for a in afiliaciones:
        codigo = (a.codigo_unico or "").strip().replace(" - ", "-")
        fecha_str = formato_fecha_para_csv(a.fecha_afiliacion)
        data.append({
            "ID": a.id,
            "Codigo Unico": codigo,
            "NIT": a.nit,
            "Nombre Comercio": a.nombre_comercio,
            "Direccion": a.direccion,
            "Ciudad": a.ciudad,
            "Red Instaladora": a.red_instaladora,
            "Tipo Datafono": a.tipo_datafono,
            "Email": a.email,
            "Telefono": a.telefono,
            "Fecha Afiliacion": fecha_str,
            "Registrado Por": f"{a.usuario.nombre} {a.usuario.apellido}" if a.usuario else None,
            "Correo Usuario": a.usuario.email if a.usuario else None,
        })

    df = pd.DataFrame(data)
    stream = BytesIO()
    csv_str = df.to_csv(index=False, encoding="utf-8-sig")
    stream.write(csv_str.encode("utf-8-sig"))
    stream.seek(0)

    return StreamingResponse(
        stream,
        media_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="afiliaciones.csv"'}
    )