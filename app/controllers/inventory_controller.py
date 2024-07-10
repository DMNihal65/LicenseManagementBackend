from http.client import HTTPException
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.curd.inventory_crud import get_inventory_analytics, get_monthly_tool_request_trends, \
    get_tool_request_status_distribution, fetch_tool_availability_and_usage, fetch_requests_by_department, \
    fetch_most_requested_tools
from app.database.database import get_db
from app.schemas.schemas import InventoryAnalytics, MonthlyToolRequests, ToolRequestStatusDistribution, ToolAvailabilityAndUsage, RequestsByDepartment, MostRequestedTools, ToolsInUseTrends

router = APIRouter()

@router.get("/inventory/analytics", response_model=InventoryAnalytics)
def get_inventory_stats(db: Session = Depends(get_db)):
    return get_inventory_analytics(db)

@router.get("/analytics/monthly_request_trends", response_model=List[MonthlyToolRequests])
def get_monthly_request_trends(db: Session = Depends(get_db)):
    return get_monthly_tool_request_trends(db)

@router.get("/analytics/request_status_distribution", response_model=List[ToolRequestStatusDistribution])
def get_request_status_distribution(db: Session = Depends(get_db)):
    return get_tool_request_status_distribution(db)

@router.get("/analytics/tool_availability_and_usage", response_model=ToolAvailabilityAndUsage)
def get_tool_availability_and_usage(db: Session = Depends(get_db)):
    return fetch_tool_availability_and_usage(db)

@router.get("/analytics/requests_by_department", response_model=List[RequestsByDepartment])
def get_requests_by_department(db: Session = Depends(get_db)):
    return fetch_requests_by_department(db)

@router.get("/analytics/most_requested_tools", response_model=List[MostRequestedTools])
def get_most_requested_tools(db: Session = Depends(get_db)):
    return fetch_most_requested_tools(db)

# @router.get("/tools_in_use_trends")
# async def get_tools_in_use_trends(db: Session = Depends(get_db)):
#     try:
#         trends = fetch_tools_in_use_trends(db)
#         return trends
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))