from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.config.dependencies import checking_pwd_strength, existing_user, create_user, authenticate, create_token
from app.models.user_model import UserCreate, User as UserResp


router = APIRouter()


# POST/SIGNUP
@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=UserResp)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # check if signup details is not unique
    db_user = existing_user(db, user.email)

    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            details="username or email already exist",
        )
    # check password strength
    password_strength, reason = checking_pwd_strength(user.password)
    if not password_strength:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            details=reason,
        )
    
    # Create user is signup details is not unique/not existing in database
    created_user = create_user(db, user)

    return created_user


# POST/LOGIN
@router.post("/login", status_code=status.HTTP_200_OK)
def login_user(user_form: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    user = authenticate(db, user_form.username, user_form.password)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    
    access_token = create_token(user.user_id, user.email)

    return {
        "token": access_token,
        "type": "bearer"
    }
