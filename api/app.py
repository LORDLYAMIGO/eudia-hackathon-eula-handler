from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import eula_router
import uvicorn, os
from dotenv import load_dotenv

load_dotenv()

HOST: str = os.getenv("HOST", "127.0.0.1")
PORT: int = int(os.getenv("PORT", 5001))

# Create FastAPI app
app = FastAPI(
    title="EULA Handler API",
    description="API for retrieving End User License Agreements, Privacy Policies, and Terms of Service",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(eula_router.router)


@app.get("/")
async def health_check():
    return "The health check is successful!"

if __name__ == "__main__":
    uvicorn.run("app:app", host=HOST, port=PORT, reload=True)
