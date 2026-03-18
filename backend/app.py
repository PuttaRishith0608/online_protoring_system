"""
FastAPI backend for Online Proctoring System
Detects copy-paste, tab switching, and AI-generated answers
"""

import sys
import traceback
from contextlib import asynccontextmanager

try:
    from fastapi import FastAPI, Request
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse
    
    # Define lifespan context manager
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # Startup
        print("\n✓ App startup - ready to handle requests", flush=True)
        yield
        # Shutdown
        print("\n✓ App shutdown - graceful exit", flush=True)
    
    # Create FastAPI app with lifespan
    app = FastAPI(
        title="Online Proctoring System",
        description="Backend API for monitoring and detecting academic integrity violations",
        version="1.0.0",
        lifespan=lifespan
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Try to import and include routes
    try:
        from routes import activity, report
        app.include_router(activity.router)
        app.include_router(report.router)
    except ImportError as e:
        print(f"WARNING: Could not import routes: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
    
    # Global exception handler
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        
        return JSONResponse(
            status_code=500,
            content={"error": str(exc), "detail": "Internal server error"}
        )
    
    @app.get("/")
    async def root():
        """Welcome endpoint"""
        return {
            "message": "Welcome to Online Proctoring System API",
            "docs_url": "/docs",
            "status": "running"
        }
    
    @app.get("/health")
    async def health_check():
        """Simple health check endpoint"""
        return {"status": "healthy", "message": "Proctoring system backend is running"}

except Exception as e:
    print(f"ERROR: Failed to initialize FastAPI app: {e}", file=sys.stderr)
    traceback.print_exc(file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
