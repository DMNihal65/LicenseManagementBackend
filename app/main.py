from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controllers import user_controller, tool_controller, tool_request_controller, department_controller, \
    inventory_controller, tool_category_controller
from app.database.database import engine
from app.models.models import Base

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Drop existing tables if needed
# Base.metadata.drop_all(bind=engine)
# Create tables
Base.metadata.create_all(bind=engine)

app.include_router(user_controller.router)
app.include_router(tool_controller.router)
app.include_router(tool_request_controller.router)
app.include_router(inventory_controller.router)
app.include_router(tool_category_controller.router, prefix="/api/v1")
app.include_router(department_controller.router)  # Include the department controller

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="172.18.7.27", port=8000)
