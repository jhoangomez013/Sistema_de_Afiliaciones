from pydantic import BaseModel, EmailStr, Field, constr
from typing import Optional
from datetime import datetime
from enum import Enum


class TipoDatafonoEnum(str, Enum):
    fijo = "Fijo"
    inalambrico_papel = "Inalámbrico de papel"
    inalambrico_sin_papel = "Inalámbrico sin papel"
    minidatafono = "Minidatafono"
    solo_qr = "Solo QR"
    link_pagos = "Link de Pagos"
    
class RedInstaladoraEnum(str, Enum):
    redeban = "Redeban"
    credibanco = "Credibanco"

# ---------- USUARIOS ----------

class UsuarioInformador(BaseModel):
    id: int
    nombre: str
    apellido: str
    email: EmailStr
    oficina: str
    
    class Config:
        from_attributes = True

class UsuarioCreate(BaseModel):
    nombre: str
    apellido: str
    email: EmailStr
    password: str
    rol_id: int
    oficina: str

class Usuario(BaseModel):
    id: int
    nombre: str
    apellido: str
    email: EmailStr
    rol_id: int
    oficina: str

    class Config:
        from_attributes = True

# ---------- ROLES ----------

class RolCreate(BaseModel):
    nombre: str
    descripcion: str

class Rol(BaseModel):
    id: int
    nombre: str
    descripcion: str

    class Config:
        from_attributes = True

# ---------- PERMISOS ----------

class PermisoCreate(BaseModel):
    nombre: str
    descripcion: str

class Permiso(BaseModel):
    id: int
    nombre: str
    descripcion: str

    class Config:
        from_attributes = True

# ---------- RELACIÓN ROLES / PERMISOS ----------

class RolPermisoCreate(BaseModel):
    rol_id: int
    permiso_id: int

class RolPermiso(BaseModel):
    id: int
    rol_id: int
    permiso_id: int

    class Config:
        from_attributes = True

# ---------- AFILIACIONES ----------

class AfiliacionCreate(BaseModel):
    codigo_unico: Optional[str] = Field(
        None,
        description="Código único asignado externamente (si no se envía, se puede generar automáticamente)"
    )
    nit: str = Field(
        ...,
        min_length=9,
        max_length=15,
        pattern=r'^\d{9,15}$',
        description="NIT numérico (9-15 dígitos)"
    )
    nombre_comercio: str = Field(..., min_length=3, max_length=100)
    direccion: str = Field(..., min_length=5, max_length=200)
    ciudad: str = Field(..., min_length=2, max_length=50)
    red_instaladora: RedInstaladoraEnum
    tipo_datafono: TipoDatafonoEnum 
    email: Optional[EmailStr] = Field(None, description="Correo del comercio (opcional)")
    telefono: str = Field(
        ...,
        pattern=r'^\d{7,10}$',
        description="Teléfono: 7 a 10 dígitos (solo números)"
    )


class Afiliacion(BaseModel):
    id: int
    codigo_unico: str
    nit: str
    nombre_comercio: str
    direccion: str
    ciudad: str
    red_instaladora: RedInstaladoraEnum
    tipo_datafono: TipoDatafonoEnum 
    email: Optional[EmailStr]
    telefono: str
    fecha_afiliacion: datetime

    usuario: "UsuarioInformador"

    class Config:
        from_attributes = True

# (Opcional) Para respuesta sin mostrar usuario_id ni usuario
class AfiliacionOut(BaseModel):
    id: int
    codigo_unico: str
    nit: str
    nombre_comercio: str
    direccion: str
    ciudad: str
    red_instaladora: RedInstaladoraEnum
    tipo_datafono: TipoDatafonoEnum 
    email: EmailStr
    telefono: str
    fecha_afiliacion: datetime


    class Config:
        from_attributes = True


class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    rol_id: Optional[int] = None
    oficina: Optional[str] = None

class AfiliacionUpdate(BaseModel):
    nit: Optional[str] = None
    nombre_comercio: Optional[str] = None
    direccion: Optional[str] = None
    ciudad: Optional[str] = None
    red_instaladora: Optional[str] = None
    tipo_datafono: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None