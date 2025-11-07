from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from services.eula_service import EULAService
import os

router = APIRouter(prefix="/eula", tags=["EULA"])

# Initialize EULA service with the path to EULA folder
EULA_BASE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "EULA")
eula_service = EULAService(EULA_BASE_PATH)


@router.get("/latest")
async def get_latest_eula(
    domain: str = Query(
        ..., 
        description="Domain name in any format (e.g., 'chatgpt.com', 'https://google.com', 'www.example.com')",
        example="chatgpt.com"
    ),
    doc_type: Optional[str] = Query(
        None,
        description="Document type: 'Privacy Policy' or 'Terms of Service'. If not specified, returns the first available.",
        example="Privacy Policy"
    )
):
    """
    Get the latest EULA document for a specific domain.
    
    Returns the most recent version of the Privacy Policy or Terms of Service
    for the specified domain.
    
    **Parameters:**
    - **domain**: Domain name (supports various formats like chatgpt.com, https://google.com)
    - **doc_type**: Optional - specify 'Privacy Policy' or 'Terms of Service'
    
    **Returns:**
    - **EULA**: The markdown content of the latest document
    - **metadata**: Information about the document including domain, type, date, and version count
    """
    result = eula_service.get_latest_eula(domain, doc_type)
    
    if "error" in result:
        raise HTTPException(status_code=404, detail=result)
    
    return result


@router.get("/archive")
async def get_archive_eula(
    domain: str = Query(
        ..., 
        description="Domain name in any format (e.g., 'chatgpt.com', 'https://google.com', 'www.example.com')",
        example="chatgpt.com"
    ),
    doc_type: Optional[str] = Query(
        None,
        description="Document type: 'Privacy Policy' or 'Terms of Service'. If not specified, returns all available.",
        example="Privacy Policy"
    )
):
    """
    Get all archived EULA documents for a specific domain, chained together.
    
    Returns all versions of the Privacy Policy and/or Terms of Service
    for the specified domain, concatenated in chronological order.
    
    **Parameters:**
    - **domain**: Domain name (supports various formats like chatgpt.com, https://google.com)
    - **doc_type**: Optional - specify 'Privacy Policy' or 'Terms of Service' to filter, or omit for all
    
    **Returns:**
    - **EULA**: All markdown contents chained together with separators and metadata for each version
    - **metadata**: Summary information including domain, document types, and version counts
    """
    result = eula_service.get_archive_eula(domain, doc_type)
    
    if "error" in result:
        raise HTTPException(status_code=404, detail=result)
    
    return result
