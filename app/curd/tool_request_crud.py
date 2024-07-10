from sqlalchemy.orm import Session
from app.models.models import ToolRequest, Tool, User
from app.schemas.schemas import ToolRequestCreate, ToolRequestUpdate, ToolUpdate


def get_tool_request(db: Session, request_id: int):
    return db.query(ToolRequest).filter(ToolRequest.RequestID == request_id).first()

def create_tool_request(db: Session, tool_request: ToolRequestCreate):
    db_tool_request = ToolRequest(**tool_request.dict())
    db.add(db_tool_request)
    db.commit()
    db.refresh(db_tool_request)
    return db_tool_request

# app/curd/tool_request_crud.py
def update_tool_request(db: Session, request_id: int, tool_request_update: ToolRequestUpdate):
    db_tool_request = db.query(ToolRequest).filter(ToolRequest.RequestID == request_id).first()
    for key, value in tool_request_update.dict(exclude_unset=True).items():
        setattr(db_tool_request, key, value)
    db.commit()
    db.refresh(db_tool_request)
    return db_tool_request

# app/curd/tool_crud.py
def get_tool(db: Session, tool_id: int):
    return db.query(Tool).filter(Tool.ToolID == tool_id).first()

def update_tool(db: Session, tool_id: int, tool_update: ToolUpdate):
    db_tool = db.query(Tool).filter(Tool.ToolID == tool_id).first()
    for key, value in tool_update.dict(exclude_unset=True).items():
        setattr(db_tool, key, value)
    db.commit()
    db.refresh(db_tool)
    return db_tool


def get_request_details(db: Session):
    query = db.query(
        ToolRequest.RequestID,
        ToolRequest.UserID,
        User.UserName,
        ToolRequest.ToolID,
        Tool.ToolName,
        ToolRequest.QuantityNeeded,
        ToolRequest.PurposeOfUse,
        ToolRequest.AdditionalComments,
        ToolRequest.RequestDate,
        ToolRequest.Status
    ).join(User, ToolRequest.UserID == User.UserID).join(Tool, ToolRequest.ToolID == Tool.ToolID)

    return query.all()