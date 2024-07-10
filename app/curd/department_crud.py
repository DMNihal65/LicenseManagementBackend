from sqlalchemy.orm import Session
from app.models.models import Department
from app.schemas.schemas import DepartmentCreate

def get_department(db: Session, dep_id: int):
    return db.query(Department).filter(Department.DepID == dep_id).first()

def create_department(db: Session, department: DepartmentCreate):
    db_department = Department(**department.dict())
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department

# New function to fetch all departments
def get_all_departments(db: Session):
    return db.query(Department).all()