from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from models import Todos, Users
from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, HTTPException, Path
from database import SessionLocal
from .auth import get_current_user, SECRET_KEY, bcrypt_context, ALGORITHM
from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=['argon2'], deprecated='auto')



router = APIRouter(
    prefix='/users',
    tags=['users']
)

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str = Field(min_lenght=6)

def get_db():
    db = SessionLocal()
    print(type(db))
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get('/user', status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    return db.query(Users).filter(Users.id == user.get('id')).first()

@router.put('/change_password', status_code=status.HTTP_200_OK)
async def change_password(user: user_dependency, db: db_dependency, passwords: ChangePasswordRequest):
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    if not bcrypt_context.verify(passwords.old_password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail="Passwords don't match")
    user_model.hashed_password = bcrypt_context.hash(passwords.new_password)
    db.add(user_model)
    db.commit()