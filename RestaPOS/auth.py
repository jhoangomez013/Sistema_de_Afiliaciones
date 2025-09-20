from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt
from sqlalchemy.orm import Session
from Base_De_Datos import models
from Base_De_Datos.database import get_db
from passlib.context import CryptContext
import os
from dotenv import load_dotenv

# Seguridad de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


load_dotenv()

# Configuración JWT
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))


# Dependencia global
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Modelo para el token
class Token(BaseModel):
    access_token: str
    token_type: str

# Función para crear JWT
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Obtener usuario actual desde el token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise credentials_exception

    user = db.query(models.UsuarioDB).filter(models.UsuarioDB.email == email).first()
    if user is None:
        raise credentials_exception
    return user

# Login de usuario
def login(form_data: OAuth2PasswordRequestForm, db: Session):
    user = db.query(models.UsuarioDB).filter(models.UsuarioDB.email == form_data.username).first()
    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    access_token = create_access_token(data={"sub": user.email})
    return Token(access_token=access_token, token_type="bearer")
