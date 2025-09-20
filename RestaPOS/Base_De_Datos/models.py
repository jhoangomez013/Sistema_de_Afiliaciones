from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from Base_De_Datos.database import Base


class UsuarioDB(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)
    apellido = Column(String)
    email = Column(String)
    password = Column(String)
    rol_id = Column(Integer, ForeignKey("roles.id"))
    oficina = Column(String, nullable=True)  # 👈 agregado aquí

    rol = relationship("RolDB", backref="usuarios")

class RolDB(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)
    descripcion = Column(String)

class PermisoDB(Base):
    __tablename__ = "permisos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)
    descripcion = Column(String)

class RolPermisoDB(Base):
    __tablename__ = "roles_permisos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    rol_id = Column(Integer, ForeignKey("roles.id"))
    permiso_id = Column(Integer, ForeignKey("permisos.id"))

    rol = relationship("RolDB", backref="roles_permisos")
    permiso = relationship("PermisoDB", backref="roles_permisos")

class AfiliacionDB(Base):
    __tablename__ = "afiliaciones"

    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo_unico = Column(String, unique=True, nullable=False)
    nit = Column(String, nullable=False)
    nombre_comercio = Column(String, nullable=False)
    direccion = Column(String, nullable=False)
    ciudad = Column(String, nullable=False)
    red_instaladora = Column(String, nullable=False)
    tipo_datafono = Column(String, nullable=False)
    email = Column(String, nullable=False)
    telefono = Column(String, nullable=False)
    fecha_afiliacion = Column(DateTime, default=datetime.utcnow)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    
    usuario = relationship("UsuarioDB", backref="afiliaciones")


