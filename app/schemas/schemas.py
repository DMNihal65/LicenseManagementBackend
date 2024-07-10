from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class DepartmentBase(BaseModel):
    Name: str

class DepartmentCreate(DepartmentBase):
    pass

class Department(DepartmentBase):
    DepID: int

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    UserName: str
    Email: str
    Phone: str
    Address: str
    DepartmentID: int

class UserCreate(UserBase):
    pass

class User(UserBase):
    UserID: int

    class Config:
        from_attributes = True

class ToolBase(BaseModel):
    ToolName: str
    QuantityAvailable: int
    Status: str
    Location: Optional[str] = None
    CategoryID: Optional[int] = None  # Added CategoryID

class ToolCreate(ToolBase):
    pass

class ToolUpdate(BaseModel):
    QuantityAvailable: Optional[int] = None
    Status: Optional[str] = None
    Location: Optional[str] = None
    CategoryID: Optional[int] = None  # Added CategoryID

    class Config:
        from_attributes = True

class Tool(ToolBase):
    ToolID: int
    LastUpdated: Optional[datetime]

    class Config:
        from_attributes = True

class CategoryBase(BaseModel):
    CategoryName: str
    ParentID: Optional[int] = None

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    CategoryID: int

    class Config:
        from_attributes = True

class ToolRequestBase(BaseModel):
    UserID: int
    ToolID: int
    QuantityNeeded: int
    PurposeOfUse: str
    AdditionalComments: Optional[str] = None
    RequestDate: Optional[datetime] = None
    Status: Optional[str] = 'Pending'
    AdminID: Optional[int] = None
    AdminApprovalDate: Optional[datetime] = None

class ToolRequestCreate(ToolRequestBase):
    pass

class ToolRequestUpdate(BaseModel):
    QuantityNeeded: Optional[int] = None
    PurposeOfUse: Optional[str] = None
    AdditionalComments: Optional[str] = None
    Status: Optional[str] = None
    AdminID: Optional[int] = None
    AdminApprovalDate: Optional[datetime] = None

    class Config:
        from_attributes = True

class ToolRequest(ToolRequestBase):
    RequestID: int

    class Config:
        from_attributes = True

class RequestDetail(BaseModel):
    RequestID: int
    UserID: int
    UserName: str
    ToolID: int
    ToolName: str
    QuantityNeeded: int
    PurposeOfUse: str
    AdditionalComments: Optional[str]
    RequestDate: datetime
    Status: str

    class Config:
        from_attributes = True

class InventoryAnalytics(BaseModel):
    total_tools: int
    total_requests: int
    pending_requests: int
    approved_requests: int
    rejected_requests: int
    tools_in_use: int
    tools_available: int

    class Config:
        from_attributes = True

class MonthlyToolRequests(BaseModel):
    month: str
    total_requests: int

    class Config:
        from_attributes = True

class ToolRequestStatusDistribution(BaseModel):
    status: str
    count: int

    class Config:
        from_attributes = True

class ToolAvailabilityAndUsage(BaseModel):
    available: int
    in_use: int

    class Config:
        from_attributes = True

class RequestsByDepartment(BaseModel):
    department_name: str
    status: str
    count: int

    class Config:
        from_attributes = True

class MostRequestedTools(BaseModel):
    tool_name: str
    request_count: int

    class Config:
        from_attributes = True

class ToolsInUseTrends(BaseModel):
    month: str
    tools_in_use: int

    class Config:
        from_attributes = True
