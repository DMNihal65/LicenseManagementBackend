from http.client import HTTPException
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import SessionLocal, get_db
from app.schemas.schemas import UserCreate, User
from ..curd.department_crud import get_department
from ..curd.user_crud import get_user, create_user
from app.schemas.schemas import User as UserSchema  # Pydantic schema
from app.models.models import User as UserModel  # SQLAlchemy model

router = APIRouter()

@router.get("/users", response_model=List[UserSchema])
async def get_all_users(db: Session = Depends(get_db)):
    users = db.query(UserModel).all()
    return users

@router.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/users/", response_model=User)
def create_new_user(user: UserCreate, department_id: int, db: Session = Depends(get_db)):
    department = get_department(db, dep_id=department_id)
    if department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    user.DepartmentID = department.DepID  # Assign DepartmentID to the user
    return create_user(db=db, user=user)
