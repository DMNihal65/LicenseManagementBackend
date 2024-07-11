from sqlalchemy.orm import Session
from app.models.models import Batch as BatchModel
from app.schemas.schemas import BatchCreate
# from app.schemas.schemas import BatchCreate as BatchModel, BatchCreate


def create_batch(db: Session, batch: BatchCreate):
    db_batch = BatchModel(
        ToolID=batch.ToolID,
        BatchNumber=batch.BatchNumber,
        ManufactureDate=batch.ManufactureDate,
        ExpiryDate=batch.ExpiryDate,
    )
    db.add(db_batch)
    db.commit()
    db.refresh(db_batch)
    return db_batch

def get_batch(db: Session, batch_id: int):
    return db.query(BatchModel).filter(BatchModel.BatchID == batch_id).first()

def get_batches(db: Session):
    return db.query(BatchModel)