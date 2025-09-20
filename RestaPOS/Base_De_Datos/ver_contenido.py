from Base_De_Datos.database import SessionLocal
from Base_De_Datos import models

db = SessionLocal()

# Solo incluimos los modelos que realmente existen
tablas = {
    "usuarios": models.UsuarioDB,
    "roles": models.RolDB,
    "permisos": models.PermisoDB,
    "roles_permisos": models.RolPermisoDB,
    "afiliaciones": models.AfiliacionDB,
}

print("Cantidad de registros en cada tabla:\n")
for nombre, modelo in tablas.items():
    try:
        total = db.query(modelo).count()
        print(f"{nombre}: {total} registros")
    except Exception as e:
        print(f"Error consultando {nombre}: {e}")

db.close()

