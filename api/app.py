from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import eula_router
import uvicorn

# Create FastAPI app
app = FastAPI(
    title="EULA Handler API",
    description="API for retrieving End User License Agreements, Privacy Policies, and Terms of Service",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(eula_router.router)


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to EULA Handler API",
        "version": "1.0.0",
        "endpoints": {
            "/eula/latest": "Get the latest EULA document for a domain",
            "/eula/archive": "Get all archived EULA documents for a domain",
            "/docs": "Interactive API documentation (Swagger UI)",
            "/redoc": "Alternative API documentation (ReDoc)"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=5001, reload=True)
