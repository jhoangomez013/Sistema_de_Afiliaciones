# crear_tablas.py
from Base_De_Datos.database import engine
from Base_De_Datos.models import Base

def crear_tablas():
    Base.metadata.create_all(engine)
    print("Tablas creadas con éxito")

if __name__ == "__main__":
    crear_tablas()
