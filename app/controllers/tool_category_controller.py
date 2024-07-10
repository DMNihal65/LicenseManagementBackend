from http.client import HTTPException
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.curd.tool_category_crud import get_category, create_category, get_all_categories as fetch_all_categories
from app.database.database import get_db

from app.schemas.schemas import Category, CategoryCreate

router = APIRouter()

@router.get("/categories/{category_id}", response_model=Category)
def read_category(category_id: int, db: Session = Depends(get_db)):
    category = get_category(db, category_id=category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.post("/categories/", response_model=Category)
def create_new_category(category: CategoryCreate, db: Session = Depends(get_db)):
    try:
        return create_category(db=db, category=category)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/categories/", response_model=List[Category])
def get_all_categories(db: Session = Depends(get_db)):
    categories = fetch_all_categories(db)
    return categories
