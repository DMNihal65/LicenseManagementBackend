from sqlalchemy.orm import Session
from app.models.models import Tool
from app.schemas.schemas import ToolCreate, ToolUpdate

def get_tool(db: Session, tool_id: int):
    return db.query(Tool).filter(Tool.ToolID == tool_id).first()

def create_tool(db: Session, tool: ToolCreate):
    db_tool = Tool(**tool.dict())
    db.add(db_tool)
    db.commit()
    db.refresh(db_tool)
    return db_tool

def update_tool(db: Session, tool_id: int, tool_update: ToolUpdate):
    db_tool = db.query(Tool).filter(Tool.ToolID == tool_id).first()
    for key, value in tool_update.dict(exclude_unset=True).items():
        setattr(db_tool, key, value)
    db.commit()
    db.refresh(db_tool)
    return db_tool
