from fastapi import FastAPI
# Import your APIRouter from the new routes file
from app.routes import comment_routes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Code Comment Generator API",
    description="API for generating comments and extracting AST from code.",
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174"],  # Allow requests from your frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# You can keep this print for initial debugging
print("FastAPI app instance created! (Main Application)")

# Include your routes from the separate router
app.include_router(comment_routes.router, prefix="/api/v1", tags=["Comments"])

# The print for routes is now more meaningful as all routers are included
print("Available routes after including router:", app.routes)

# Optional: You can keep a root endpoint directly in main.py if it's app-specific
# @app.get("/")
# def app_root():
#     return {"message": "Welcome to the Code Comment Generator API!"}1