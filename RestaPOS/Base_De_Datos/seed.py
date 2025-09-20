# seed.py
from Base_De_Datos.database import SessionLocal
from Base_De_Datos import models
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def seed():
    db = SessionLocal()

    # Crear rol admin si no existe
    rol_admin = db.query(models.RolDB).filter_by(nombre="admin").first()
    if not rol_admin:
        rol_admin = models.RolDB(nombre="admin")
        db.add(rol_admin)
        db.commit()
        db.refresh(rol_admin)

    # Crear usuario admin si no existe
    admin = db.query(models.UsuarioDB).filter_by(email="admin@admin.com").first()
    if not admin:
        hashed_password = pwd_context.hash("admin123")
        admin = models.UsuarioDB(
            email="admin@admin.com",
            nombre="Administrador",
            password=hashed_password,
            rol_id=rol_admin.id
        )
        db.add(admin)
        db.commit()

    db.close()
    print("Datos iniciales creados con éxito")

if __name__ == "__main__":
    seed()
