from sqlalchemy import Column, ForeignKey, Integer, String, Enum, TIMESTAMP
from sqlalchemy.orm import relationship
from app.database.database import Base


class Department(Base):
    __tablename__ = "departments"
    DepID = Column(Integer, primary_key=True, index=True)
    Name = Column(String, nullable=False)

class User(Base):
    __tablename__ = "users"
    UserID = Column(Integer, primary_key=True, index=True)
    UserName = Column(String, nullable=False)
    Email = Column(String, nullable=False)
    Phone = Column(String)
    Address = Column(String)
    DepartmentID = Column(Integer, ForeignKey("departments.DepID"))  # Foreign key relationship

    # Relationship with Department
    department = relationship("Department", backref="users")

    # Relationship with ToolRequest (assuming there's a ToolRequest model)
    requests = relationship("ToolRequest", back_populates="user")  # Make sure this matches the ToolRequest model

class ToolCategory(Base):
    __tablename__ = "tool_categories"
    CategoryID = Column(Integer, primary_key=True, index=True)
    CategoryName = Column(String, index=True)
    ParentID = Column(Integer, ForeignKey("tool_categories.CategoryID"), nullable=True)
    children = relationship("ToolCategory", backref="parent", remote_side=[CategoryID])

class Tool(Base):
    __tablename__ = "tools"
    ToolID = Column(Integer, primary_key=True, index=True)
    ToolName = Column(String, nullable=False)
    QuantityAvailable = Column(Integer, nullable=False)
    Status = Column(Enum('Available', 'In Use', name='tool_status_enum'), nullable=False)
    Location = Column(String)
    LastUpdated = Column(TIMESTAMP)
    CategoryID = Column(Integer, ForeignKey("tool_categories.CategoryID"))

    # Relationship with ToolCategory
    category = relationship("ToolCategory", backref="tools")

    # Relationship with ToolRequest
    requests = relationship("ToolRequest", back_populates="tool")


class ToolRequest(Base):
    __tablename__ = "tool_requests"
    RequestID = Column(Integer, primary_key=True, index=True)
    UserID = Column(Integer, ForeignKey("users.UserID"))  # Corrected column name
    ToolID = Column(Integer, ForeignKey("tools.ToolID"))  # Corrected column name
    QuantityNeeded = Column(Integer, nullable=False)
    PurposeOfUse = Column(String)
    AdditionalComments = Column(String)
    RequestDate = Column(TIMESTAMP)
    Status = Column(Enum('Pending', 'Approved', 'Rejected', name='request_status_enum'), default='Pending')
    AdminID = Column(Integer)
    AdminApprovalDate = Column(TIMESTAMP)

    # Relationships
    user = relationship("User", back_populates="requests")  # Make sure this matches the User model
    tool = relationship("Tool", back_populates="requests")

class InventoryAnalytics(Base):
    __tablename__ = "inventory_analytics"

    id = Column(Integer, primary_key=True)
    total_tools = Column(Integer)
    total_requests = Column(Integer)
    pending_requests = Column(Integer)
    approved_requests = Column(Integer)
    rejected_requests = Column(Integer)
    tools_in_use = Column(Integer)
    tools_available = Column(Integer)