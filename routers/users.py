from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from models import Todos, Users
from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, HTTPException, Path
from database import SessionLocal
from .auth import get_current_user


router = APIRouter(
    prefix='/users',
    tags=['users']
)


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

