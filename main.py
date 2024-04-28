from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router as app_router

app = FastAPI()

# Include CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set this to your specific allowed origins if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the API routers
app.include_router(app_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="172.20.10.2", port=9999)
