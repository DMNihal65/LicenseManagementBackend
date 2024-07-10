from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from app.models.models import Department, Tool, ToolRequest, InventoryAnalytics
from app.schemas.schemas import ToolRequestStatusDistribution, MonthlyToolRequests, ToolAvailabilityAndUsage, RequestsByDepartment, MostRequestedTools, ToolsInUseTrends

def get_inventory_analytics(db: Session) -> InventoryAnalytics:
    total_tools = db.query(func.count(Tool.ToolID)).scalar()
    total_requests = db.query(func.count(ToolRequest.RequestID)).scalar()
    pending_requests = db.query(func.count(ToolRequest.RequestID)).filter(ToolRequest.Status == 'Pending').scalar()
    approved_requests = db.query(func.count(ToolRequest.RequestID)).filter(ToolRequest.Status == 'Approved').scalar()
    rejected_requests = db.query(func.count(ToolRequest.RequestID)).filter(ToolRequest.Status == 'Rejected').scalar()
    tools_in_use = db.query(func.sum(Tool.QuantityAvailable)).filter(Tool.Status == 'In Use').scalar() or 0
    tools_available = db.query(func.sum(Tool.QuantityAvailable)).filter(Tool.Status == 'Available').scalar() or 0

    return InventoryAnalytics(
        total_tools=total_tools,
        total_requests=total_requests,
        pending_requests=pending_requests,
        approved_requests=approved_requests,
        rejected_requests=rejected_requests,
        tools_in_use=tools_in_use,
        tools_available=tools_available
    )

def get_monthly_tool_request_trends(db: Session) -> List[MonthlyToolRequests]:
    monthly_requests = db.query(func.date_trunc('month', ToolRequest.RequestDate).label("month"), func.count(ToolRequest.RequestID)).group_by("month").all()
    monthly_tool_requests = [{"month": month.strftime("%Y-%m"), "total_requests": count} for month, count in monthly_requests]
    return monthly_tool_requests

def get_tool_request_status_distribution(db: Session) -> List[ToolRequestStatusDistribution]:
    status_distribution = db.query(ToolRequest.Status, func.count(ToolRequest.RequestID)).group_by(ToolRequest.Status).all()
    return [{"status": status, "count": count} for status, count in status_distribution]

def fetch_tool_availability_and_usage(db: Session) -> ToolAvailabilityAndUsage:
    tools_available = db.query(func.sum(Tool.QuantityAvailable)).filter(Tool.Status == 'Available').scalar() or 0
    tools_in_use = db.query(func.sum(Tool.QuantityAvailable)).filter(Tool.Status == 'In Use').scalar() or 0
    return {"available": tools_available, "in_use": tools_in_use}

def fetch_requests_by_department(db: Session) -> List[RequestsByDepartment]:
    requests_by_department = db.query(Department.Name, ToolRequest.Status, func.count(ToolRequest.RequestID)).join(Department, Department.DepID == ToolRequest.UserID).group_by(Department.Name, ToolRequest.Status).all()
    result = []
    for department_name, status, count in requests_by_department:
        result.append({"department_name": department_name, "status": status, "count": count})
    return result

def fetch_most_requested_tools(db: Session) -> List[MostRequestedTools]:
    most_requested_tools = db.query(Tool.ToolName, func.count(ToolRequest.RequestID).label("request_count")).join(Tool, Tool.ToolID == ToolRequest.ToolID).group_by(Tool.ToolName).order_by(func.count(ToolRequest.RequestID).desc()).limit(10).all()
    return [{"tool_name": tool_name, "request_count": request_count} for tool_name, request_count in most_requested_tools]




# def fetch_tools_in_use_trends(db: Session):
#     tools_in_use_trends = db.query(
#         extract('month', InventoryInUse.date).label('month'),
#         func.count(InventoryInUse.id).label('tools_in_use')
#     ).group_by('month').all()
#
#     trends = []
#     for month, tools_in_use in tools_in_use_trends:
#         if month is not None:
#             trends.append({"month": month.strftime("%Y-%m"), "tools_in_use": tools_in_use})
#         else:
#             trends.append({"month": "Unknown", "tools_in_use": tools_in_use})
#
#     return trends
