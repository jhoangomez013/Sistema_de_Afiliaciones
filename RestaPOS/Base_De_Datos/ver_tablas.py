from sqlalchemy import inspect, text
from Base_De_Datos.database import engine

def ver_tablas():
    inspector = inspect(engine)
    tablas = inspector.get_table_names()
    print("Tablas en la base de datos:")
    for tabla in tablas:
        print(f" - {tabla}")

    with engine.connect() as conn:
        result = conn.execute(text("SELECT current_database();"))
        for row in result:
            print(f"\nConectado a la base de datos: {row[0]}")

ver_tablas()
