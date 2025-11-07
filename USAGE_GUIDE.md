# EULA Handler API - Quick Start Guide

## 🚀 Getting Started

### 1. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 2. Start the Server
```powershell
cd api
python run.py
```

The server will start at `http://127.0.0.1:8000`

## 📖 API Documentation

Once the server is running, you can access:
- **Interactive API Docs (Swagger)**: http://127.0.0.1:8000/docs
- **Alternative Docs (ReDoc)**: http://127.0.0.1:8000/redoc

## 🎯 API Endpoints

### 1. `/eula/latest` - Get Latest EULA Document

Retrieves the most recent version of a EULA document for a domain.

#### Parameters:
- **domain** (required): Domain name in various formats
- **doc_type** (optional): "Privacy Policy" or "Terms of Service"

#### Example Requests:

**Using PowerShell:**
```powershell
# Latest document for chatgpt.com
Invoke-WebRequest "http://127.0.0.1:8000/eula/latest?domain=chatgpt.com" | Select-Object -Expand Content | ConvertFrom-Json

# Latest Privacy Policy for Google
Invoke-WebRequest "http://127.0.0.1:8000/eula/latest?domain=https://google.com&doc_type=Privacy%20Policy" | Select-Object -Expand Content | ConvertFrom-Json

# Latest Terms of Service for Amazon
Invoke-WebRequest "http://127.0.0.1:8000/eula/latest?domain=amazon.com&doc_type=Terms%20of%20Service" | Select-Object -Expand Content | ConvertFrom-Json
```

**Using Python:**
```python
import requests

# Get latest document
response = requests.get("http://127.0.0.1:8000/eula/latest", params={"domain": "chatgpt.com"})
data = response.json()

print(f"Domain: {data['metadata']['domain']}")
print(f"Document Type: {data['metadata']['document_type']}")
print(f"Version Date: {data['metadata']['file_date']}")
print(f"Total Versions: {data['metadata']['total_versions']}")
print(f"\nContent Preview:\n{data['EULA'][:500]}...")
```

**Using JavaScript/Fetch:**
```javascript
fetch('http://127.0.0.1:8000/eula/latest?domain=chatgpt.com')
  .then(response => response.json())
  .then(data => {
    console.log('Domain:', data.metadata.domain);
    console.log('Document Type:', data.metadata.document_type);
    console.log('EULA Content:', data.EULA);
  });
```

#### Response Format:
```json
{
  "EULA": "... full markdown content ...",
  "metadata": {
    "domain": "chat.openai.com",
    "document_type": "Privacy Policy",
    "file_name": "2025-11-01T00-31-13Z.md",
    "file_date": "2025-11-01T00-31-13Z",
    "total_versions": 19
  }
}
```

---

### 2. `/eula/archive` - Get All EULA Documents

Retrieves all historical versions of EULA documents, chained together chronologically.

#### Parameters:
- **domain** (required): Domain name in various formats
- **doc_type** (optional): Filter by document type or get all

#### Example Requests:

**Using PowerShell:**
```powershell
# All archived documents for chatgpt.com
Invoke-WebRequest "http://127.0.0.1:8000/eula/archive?domain=chatgpt.com" | Select-Object -Expand Content | ConvertFrom-Json

# All Privacy Policy versions for Google
Invoke-WebRequest "http://127.0.0.1:8000/eula/archive?domain=google.com&doc_type=Privacy%20Policy" | Select-Object -Expand Content | ConvertFrom-Json
```

**Using Python:**
```python
import requests

# Get all archived documents
response = requests.get("http://127.0.0.1:8000/eula/archive", params={"domain": "chatgpt.com"})
data = response.json()

print(f"Domain: {data['metadata']['domain']}")
print(f"Document Types: {data['metadata']['document_types']}")
print(f"Total Versions: {data['metadata']['total_versions']}")
print(f"Versions per Type: {data['metadata']['versions_per_type']}")
print(f"\nChained Content Length: {len(data['EULA'])} characters")
```

#### Response Format:
```json
{
  "EULA": "================================================================================\nDocument Type: Privacy Policy\nVersion Date: 2023-10-16T12-30-08Z\nFile: 2023-10-16T12-30-08Z.md\n================================================================================\n\n[content]\n\n================================================================================\nDocument Type: Privacy Policy\nVersion Date: 2023-11-14T18-30-27Z\nFile: 2023-11-14T18-30-27Z.md\n================================================================================\n\n[content] ...",
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

---

## 🔍 Supported Domain Formats

The API automatically normalizes various domain formats:

✅ `chatgpt.com`
✅ `https://chatgpt.com`
✅ `http://chatgpt.com`
✅ `www.chatgpt.com`
✅ `https://www.google.com`
✅ `google.in`

All formats are matched to the corresponding folder in the EULA directory.

---

## ⚠️ Error Handling

### Domain Not Found
```json
{
  "detail": {
    "error": "Domain 'example.com' not found in EULA database",
    "domain_extracted": "example.com"
  }
}
```

### No Documents Available
```json
{
  "detail": {
    "error": "No Privacy Policy or Terms of Service found for domain 'example.com'",
    "domain_folder": "C:\\...\\EULA\\example.com"
  }
}
```

---

## 💡 Use Cases

### 1. Get the Current Privacy Policy
```python
import requests

response = requests.get(
    "http://127.0.0.1:8000/eula/latest",
    params={
        "domain": "chatgpt.com",
        "doc_type": "Privacy Policy"
    }
)
privacy_policy = response.json()['EULA']
```

### 2. Compare All Versions
```python
import requests

response = requests.get(
    "http://127.0.0.1:8000/eula/archive",
    params={"domain": "chatgpt.com"}
)
all_versions = response.json()['EULA']
# Parse the chained content to extract individual versions
```

### 3. Monitor Multiple Domains
```python
import requests

domains = ["chatgpt.com", "google.com", "amazon.com", "github.com"]

for domain in domains:
    response = requests.get(
        "http://127.0.0.1:8000/eula/latest",
        params={"domain": domain}
    )
    if response.status_code == 200:
        data = response.json()
        print(f"{domain}: {data['metadata']['total_versions']} versions available")
    else:
        print(f"{domain}: Not found")
```

### 4. Save Latest Policy to File
```python
import requests

response = requests.get(
    "http://127.0.0.1:8000/eula/latest",
    params={"domain": "chatgpt.com"}
)

if response.status_code == 200:
    data = response.json()
    filename = f"{data['metadata']['domain']}_{data['metadata']['file_date']}.md"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(data['EULA'])
    
    print(f"Saved to {filename}")
```

---

## 🧪 Testing

Run the test suite:
```powershell
python test_api.py
```

This will test:
- Root endpoint
- Latest EULA retrieval with various formats
- Archive EULA retrieval
- Error handling

---

## 📁 Project Structure

```
eudia-hackathon-eula-handler/
├── api/
│   ├── app.py              # Main FastAPI application
│   ├── run.py              # Server startup script
│   ├── routers/
│   │   ├── __init__.py
│   │   └── eula_router.py  # EULA endpoint definitions
│   └── services/
│       ├── __init__.py
│       └── eula_service.py # Business logic for EULA operations
├── EULA/                   # Document repository
│   └── [domain]/
│       ├── Privacy Policy/
│       │   └── YYYY-MM-DDTHH-MM-SSZ.md
│       └── Terms of Service/
│           └── YYYY-MM-DDTHH-MM-SSZ.md
├── requirements.txt        # Python dependencies
├── test_api.py            # API test suite
└── API_README.md          # This file
```

---

## 🛠️ Development

### Adding CORS Support
The API has CORS enabled for all origins by default. For production, update in `app.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specific domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Customizing the Response
Modify `eula_service.py` to change how documents are retrieved or formatted.

### Adding More Endpoints
Create new routers in `api/routers/` and include them in `app.py`.

---

## 📞 Support

For issues or questions about the API:
1. Check the interactive documentation at `/docs`
2. Review the test examples in `test_api.py`
3. Examine the service logic in `services/eula_service.py`

---

## 🔐 Security Notes

- The API currently allows all CORS origins (development mode)
- No authentication is implemented (add if needed for production)
- File paths are sanitized to prevent directory traversal
- All file operations use UTF-8 encoding

---

## ⚡ Performance Tips

1. **Latest API** is faster as it only reads one file
2. **Archive API** can be slow for domains with many versions
3. Consider caching frequently accessed documents
4. Use `doc_type` parameter to filter and speed up queries

---

## 📝 License

See LICENSE file for details.
