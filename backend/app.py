"""
FastAPI backend for Online Proctoring System
Detects copy-paste, tab switching, and AI-generated answers
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import activity, report

# Create FastAPI app
app = FastAPI(
    title="Online Proctoring System",
    description="Backend API for monitoring and detecting academic integrity violations",
    version="1.0.0"
)

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(activity.router)
app.include_router(report.router)


@app.get("/")
async def root():
    """Welcome endpoint"""
    return {
        "message": "Welcome to Online Proctoring System API",
        "docs_url": "/docs",
        "available_endpoints": {
            "POST": "/log-event - Log a user activity event",
            "GET": "/report/{user_id} - Get integrity report for user",
            "GET": "/events/{user_id} - Get all events for user (debug)",
            "GET": "/health - Health check"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
