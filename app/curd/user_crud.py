from sqlalchemy.orm import Session
from app.models.models import User
from app.schemas.schemas import UserCreate

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.UserID == user_id).first()

def create_user(db: Session, user: UserCreate):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
