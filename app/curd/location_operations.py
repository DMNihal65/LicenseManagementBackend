from sqlalchemy.orm import Session
from app.models.models import Location, ToolLocation
from app.schemas.schemas import LocationCreate, ToolLocationCreate

def create_location(db: Session, location: LocationCreate) -> Location:
    db_location = Location(**location.dict())
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location

def create_tool_location(db: Session, tool_location: ToolLocationCreate) -> ToolLocation:
    db_tool_location = ToolLocation(**tool_location.dict())
    db.add(db_tool_location)
    db.commit()
    db.refresh(db_tool_location)
    return db_tool_location

def get_locations(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Location).offset(skip).limit(limit).all()

# def create_tool_location(db: Session, tool_location: ToolLocationCreate):
#     db_tool_location = ToolLocation(**tool_location.dict())
#     db.add(db_tool_location)
#     db.commit()
#     db.refresh(db_tool_location)
#     return db_tool_location

def get_tool_locations(db: Session, skip: int = 0, limit: int = 10):
    return db.query(ToolLocation).offset(skip).limit(limit).all()
