
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from Base_De_Datos.database import SessionLocal, engine
from Base_De_Datos import models 
from schemas import *
from endpoints import rol_permiso, afiliacion, usuarios,  permisos, rol, login, reportes
from fastapi.middleware.cors import CORSMiddleware


# Crea las tablas en la base de datos si no existen
models.Base.metadata.create_all(bind=engine)
# Dependencia para obtener sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crear la aplicación FastAPI
app = FastAPI()
templates = Jinja2Templates(directory="templates")
# Servir archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")


# Endpoint Usuarios
app.include_router(usuarios.app)

# Endpoin Permisos
app.include_router(permisos.app)

# Endpoin Roles_Permiso
app.include_router(rol_permiso.app)

# Endpoin Roles
app.include_router(rol.app)

# Endpoin Login
app.include_router(login.app)

# Endpoin Afilación
app.include_router(afiliacion.app)

# Endpoin Reportes
app.include_router(reportes.router, tags=["Reportes"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # O especifica tu frontend: ["http://localhost:4200"]
    allow_credentials=True,
    allow_methods=["*"],  # O ["POST", "GET", "OPTIONS"]
    allow_headers=["*"]
)

