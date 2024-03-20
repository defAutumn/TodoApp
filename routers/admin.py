from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from models import Todos
from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, HTTPException, Path
from database import SessionLocal
from .auth import get_current_user


router = APIRouter(
    prefix='/admin',
    tags=['admin']
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

@router.get('/todo', status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None or user.get('role').lower() != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failel.')
    return db.query(Todos).all()