from http.client import HTTPException
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.schemas import Department, DepartmentCreate
from ..curd.department_crud import get_department, create_department, get_all_departments

router = APIRouter()

@router.get("/departments/{dep_id}", response_model=Department)
def read_department(dep_id: int, db: Session = Depends(get_db)):
    department = get_department(db, dep_id=dep_id)
    if department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return department

@router.post("/departments/", response_model=Department)
def create_new_department(department: DepartmentCreate, db: Session = Depends(get_db)):
    return create_department(db=db, department=department)

# New endpoint to fetch all departments with their IDs
@router.get("/departments/", response_model=List[Department])
def read_all_departments(db: Session = Depends(get_db)):
    return get_all_departments(db)
