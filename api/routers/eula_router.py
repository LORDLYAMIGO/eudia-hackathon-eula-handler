from fastapi import APIRouter, Query, HTTPException
from typing import Optional, Dict
from pydantic import BaseModel
from services.eula_service import EULAService
import os

router = APIRouter(prefix="/eula", tags=["EULA"])

# Pydantic model for version request
class VersionFetchRequest(BaseModel):
    versions: list[str]

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


@router.get("/versions")
async def get_versions(
    domain: str = Query(
        ..., 
        description="Domain name in any format (e.g., 'chatgpt.com', 'https://google.com', 'www.example.com')",
        example="chatgpt.com"
    )
):
    """
    Get all available versions for a domain.
    
    Returns a list of version filenames (timestamps) for the domain.
    Privacy Policy takes priority over Terms of Service.
    
    **Parameters:**
    - **domain**: Domain name (supports various formats like chatgpt.com, https://google.com)
    
    **Returns:**
    - **versions**: List of version filenames (without .md extension)
    - **domain**: The clean domain name
    - **document_type**: The document type being returned ('Privacy Policy' or 'Terms of Service')
    """
    result = eula_service.get_versions(domain)
    
    if "error" in result:
        raise HTTPException(status_code=404, detail=result)
    
    return result


@router.post("/version/{domain}")
async def fetch_multiple_versions(
    domain: str,
    data: VersionFetchRequest
) -> Dict[str, str]:
    """
    Fetch multiple EULA versions for a domain.
    
    This endpoint is designed for the diff microservice to fetch multiple versions
    of EULAs at once.
    
    **Parameters:**
    - **domain**: Domain name (e.g., 'chatgpt.com', 'google.com')
    - **versions**: List of version timestamps in request body
    
    **Request Body:**
    ```json
    {
      "versions": ["2024-01-15T10-30-00Z", "2024-02-20T14-45-30Z"]
    }
    ```
    
    **Returns:**
    Dictionary mapping version timestamps to their EULA content:
    ```json
    {
      "2024-01-15T10-30-00Z": "eula content...",
      "2024-02-20T14-45-30Z": "eula content..."
    }
    ```
    """
    eula_dict = {}
    errors = []
    
    for version in data.versions:
        result = eula_service.get_version_by_filename(domain, version)
        
        if "error" in result:
            errors.append(f"Version '{version}': {result['error']}")
        else:
            eula_dict[version] = result.get("EULA", "")
    
    # If there were errors but some succeeded, include errors in response
    if errors and eula_dict:
        # Still return what we got, but log the errors
        # The microservice can handle partial responses
        pass
    elif errors and not eula_dict:
        # All failed
        raise HTTPException(
            status_code=404, 
            detail=f"Failed to fetch versions for domain '{domain}': " + "; ".join(errors)
        )
    
    return eula_dict
