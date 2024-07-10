from sqlalchemy.orm import Session
from app.models.models import ToolCategory
from app.schemas.schemas import CategoryCreate


def get_category_by_id(db: Session, category_id: int):
    return db.query(ToolCategory).filter(ToolCategory.CategoryID == category_id).first()


def create_category(db: Session, category: CategoryCreate):
    if category.ParentID:
        parent_category = get_category_by_id(db, category.ParentID)
        if not parent_category:
            raise ValueError(f"ParentID {category.ParentID} does not exist.")

    db_category = ToolCategory(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def get_all_categories(db: Session):
    return db.query(ToolCategory).all()


def get_category(db: Session, category_id: int):
    return db.query(ToolCategory).filter(ToolCategory.CategoryID == category_id).first()
