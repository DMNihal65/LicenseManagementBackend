from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.schemas import LocationCreate, Location, ToolLocationCreate, ToolLocation
from app.database.database import get_db
from app.curd import location_operations

router = APIRouter()

@router.post("/locations/", response_model=Location)
def create_location(location: LocationCreate, db: Session = Depends(get_db)):
    return location_operations.create_location(db=db, location=location)

@router.get("/locations/", response_model=List[Location])
def read_locations(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    locations = location_operations.get_locations(db, skip=skip, limit=limit)
    return locations

@router.post("/tool-locations/", response_model=ToolLocation)
def create_tool_location(tool_location: ToolLocationCreate, db: Session = Depends(get_db)):
    return location_operations.create_tool_location(db=db, tool_location=tool_location)

@router.get("/tool-locations/", response_model=List[ToolLocation])
def read_tool_locations(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    tool_locations = location_operations.get_tool_locations(db, skip=skip, limit=limit)
    return tool_locations
