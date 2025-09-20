from sqlalchemy import text
from Base_De_Datos.database import engine

def eliminar_tablas():
    with engine.connect() as connection:
        connection.execute(text("DROP SCHEMA public CASCADE"))
        connection.execute(text("CREATE SCHEMA public"))
    print("Esquema eliminado y recreado con éxito")

eliminar_tablas()

