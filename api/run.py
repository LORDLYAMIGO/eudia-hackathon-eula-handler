"""
Run script for EULA Handler API
"""
import sys
import os

# Add the api directory to the path
sys.path.insert(0, os.path.dirname(__file__))

if __name__ == "__main__":
    import uvicorn
    
    print("="*80)
    print("Starting EULA Handler API Server")
    print("="*80)
    print("\nServer will be available at: http://127.0.0.1:8000")
    print("\nAPI Documentation:")
    print("  - Swagger UI: http://127.0.0.1:8000/docs")
    print("  - ReDoc:      http://127.0.0.1:8000/redoc")
    print("\nExample endpoints:")
    print("  - http://127.0.0.1:8000/eula/latest?domain=chatgpt.com")
    print("  - http://127.0.0.1:8000/eula/archive?domain=chatgpt.com")
    print("\nPress CTRL+C to stop the server")
    print("="*80)
    print()
    
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
