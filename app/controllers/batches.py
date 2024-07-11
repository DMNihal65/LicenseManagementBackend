from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.schemas import Batch, BatchCreate
from app.database.database import get_db
from app.curd import batch_operations

router = APIRouter()

@router.post("/", response_model=Batch)
def create_batch(batch: BatchCreate, db: Session = Depends(get_db)):
    return batch_operations.create_batch(db, batch)

@router.get("/{batch_id}", response_model=Batch)
def read_batch(batch_id: int, db: Session = Depends(get_db)):
    db_batch = batch_operations.get_batch(db, batch_id)
    if db_batch is None:
        raise HTTPException(status_code=404, detail="Batch not found")
    return db_batch

@router.get("/", response_model=List[Batch])
def read_batches(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    batches = batch_operations.get_batches(db).offset(skip).limit(limit).all()
    return batches