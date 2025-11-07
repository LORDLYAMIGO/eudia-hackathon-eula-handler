# EULA Handler API

A FastAPI-based service for retrieving End User License Agreements, Privacy Policies, and Terms of Service documents.

## Features

- 📄 **Latest EULA**: Retrieve the most recent version of a document
- 📚 **Archive**: Get all historical versions of documents chained together
- 🔍 **Smart Domain Matching**: Supports various URL formats (with/without https, www, etc.)
- 🎯 **Document Type Filtering**: Filter by Privacy Policy or Terms of Service

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
cd api
python -m uvicorn app:app --reload
```

Or simply:
```bash
cd api
python app.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

### 1. Get Latest EULA - `/eula/latest`

Retrieve the most recent version of a document for a domain.

**Parameters:**
- `domain` (required): Domain name in any format
  - Examples: `chatgpt.com`, `https://google.com`, `www.amazon.com`
- `doc_type` (optional): Filter by document type
  - Values: `Privacy Policy` or `Terms of Service`

**Example Requests:**

```bash
# Get latest document for chatgpt.com
curl "http://localhost:8000/eula/latest?domain=chatgpt.com"

# Get latest Privacy Policy for Google
curl "http://localhost:8000/eula/latest?domain=https://google.com&doc_type=Privacy%20Policy"

# Get latest Terms of Service
curl "http://localhost:8000/eula/latest?domain=amazon.com&doc_type=Terms%20of%20Service"
```

**Response:**
```json
{
  "EULA": "... markdown content ...",
  "metadata": {
    "domain": "chat.openai.com",
    "document_type": "Privacy Policy",
    "file_name": "2025-11-01T00-31-13Z.md",
    "file_date": "2025-11-01T00-31-13Z",
    "total_versions": 19
  }
}
```

### 2. Get Archive EULA - `/eula/archive`

Retrieve all historical versions of documents for a domain, chained together.

**Parameters:**
- `domain` (required): Domain name in any format
- `doc_type` (optional): Filter by document type or get all types

**Example Requests:**

```bash
# Get all archived documents for chatgpt.com
curl "http://localhost:8000/eula/archive?domain=chatgpt.com"

# Get all Privacy Policy versions
curl "http://localhost:8000/eula/archive?domain=https://google.com&doc_type=Privacy%20Policy"
```

**Response:**
```json
{
  "EULA": "... all documents chained with separators ...",
  "metadata": {
    "domain": "chat.openai.com",
    "document_types": ["Privacy Policy", "Terms of Service"],
    "total_versions": 43,
    "versions_per_type": {
      "Privacy Policy": 19,
      "Terms of Service": 24
    }
  }
}
```

## Interactive Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Domain Formats Supported

The API intelligently handles various domain formats:
- ✅ `chatgpt.com`
- ✅ `https://chatgpt.com`
- ✅ `http://www.chatgpt.com`
- ✅ `www.google.com`
- ✅ `https://google.in`

All formats are normalized to match the folder structure in the EULA directory.

## Error Handling

If a domain is not found or has no documents:
```json
{
  "detail": {
    "error": "Domain 'example.com' not found in EULA database",
    "domain_extracted": "example.com"
  }
}
```

## Project Structure

```
api/
├── app.py                 # Main FastAPI application
├── routers/
│   ├── __init__.py
│   └── eula_router.py    # EULA endpoints
└── services/
    └── eula_service.py   # Business logic for EULA retrieval

EULA/                     # Document storage
└── [domain]/
    ├── Privacy Policy/
    │   └── YYYY-MM-DDTHH-MM-SSZ.md
    └── Terms of Service/
        └── YYYY-MM-DDTHH-MM-SSZ.md
```

## Development

The API uses:
- **FastAPI**: Modern web framework
- **Pydantic**: Data validation
- **Uvicorn**: ASGI server

## License

See LICENSE file for details.
