from typing import List
from sqlalchemy import or_
from app.tables.user_schemas import User
from app.models.user_model import UserCreate

from datetime import datetime, timedelta
from decouple import config
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from starlette.responses import JSONResponse




JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")
EXPIRE = 60 * 24 * 2 # 2 days

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="login")
hashing_pwd = CryptContext(schemes=["bcrypt"])

# check existing user via username/email
def existing_user(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

# check password strength
def checking_pwd_strength(password:str)->List:
    SPECIAL_CHAR = ["#", ".", "@", ":", "?", ".", "~", "|", "<", ">"]

    if len(password) < 6:
        return False, "Password length should be greater than 5"
    
    if not any(char.isdigit() for char in password):
        return False, "Password should contain number(s)"
    
    if not any(char in SPECIAL_CHAR for char in password):
        return False, f"Password should contain any {SPECIAL_CHAR}"
    
    if not any(char.islower() for char in password):
        return False, "Password should contain lowercase letter(s)"

# create user not exist in database
def create_user(db:Session, user:UserCreate):
    creating_user = User(
            email = user.email,
            hash_password = hashing_pwd.hash(user.password),
            is_active = False
        )
    
    db.add(creating_user)
    db.commit()
    db.refresh(creating_user)  # Refresh the user object to get updated data after commit

    return creating_user

# Autheticate user
def create_token(id: int, email: str):
    # create access token
    expiry = datetime.utcnow() + timedelta(minutes=EXPIRE)

    payload = {
        "id": id,
        "sub": email,
        "expiry": expiry.isoformat()  # Convert datetime to an ISO 8601 string
        }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

def get_current_user(db: Session, token: str = Depends(oauth2_bearer)):
    # get current user from token
    try:
        # decode token to get the user via username
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

        email:str = payload.get("sub")
        id:int = payload.get("id")
        expiration_time: datetime = payload.get("expiry")

        if email is None or id is None or expiration_time <= datetime.utcnow():
            return None
        
        current_user = db.query(User).filter(User.user_id == id).first()
        return current_user
    except JWTError as e:
        return {"Error": e}

def authenticate(db:Session, email:str, password:str):
    # Authenticate users
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return False
    if not hashing_pwd.verify(password, user.hash_password):
        return False
    return user
