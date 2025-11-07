# Quick API Examples - PowerShell & Python

## 🚀 Start Server

```powershell
cd api
python run.py
```

Server runs at: `http://127.0.0.1:8000`

---

## 📝 PowerShell Examples

### 1. Get Latest EULA (any domain)
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/eula/latest?domain=chatgpt.com"
```

### 2. Get Latest Privacy Policy
```powershell
$response = Invoke-RestMethod "http://127.0.0.1:8000/eula/latest?domain=chatgpt.com&doc_type=Privacy Policy"
$response.metadata
$response.EULA
```

### 3. Get Latest Terms of Service
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/eula/latest?domain=amazon.com&doc_type=Terms of Service"
```

### 4. Get All Archives
```powershell
$response = Invoke-RestMethod "http://127.0.0.1:8000/eula/archive?domain=chatgpt.com"
Write-Host "Total Versions:" $response.metadata.total_versions
```

### 5. Test Multiple Domain Formats
```powershell
$domains = @("chatgpt.com", "https://google.com", "www.amazon.com")
foreach ($domain in $domains) {
    $response = Invoke-RestMethod "http://127.0.0.1:8000/eula/latest?domain=$domain"
    Write-Host "$domain -> $($response.metadata.domain)"
}
```

### 6. Save EULA to File
```powershell
$response = Invoke-RestMethod "http://127.0.0.1:8000/eula/latest?domain=chatgpt.com"
$filename = "$($response.metadata.domain)_$($response.metadata.file_date).md"
$response.EULA | Out-File -FilePath $filename -Encoding UTF8
Write-Host "Saved to $filename"
```

### 7. Get Metadata Only
```powershell
$response = Invoke-RestMethod "http://127.0.0.1:8000/eula/latest?domain=chatgpt.com"
$response.metadata | ConvertTo-Json
```

### 8. Pretty Print JSON
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/eula/latest?domain=chatgpt.com" | ConvertTo-Json -Depth 10
```

---

## 🐍 Python Examples

### 1. Basic Latest Request
```python
import requests

response = requests.get(
    "http://127.0.0.1:8000/eula/latest",
    params={"domain": "chatgpt.com"}
)

data = response.json()
print(f"Domain: {data['metadata']['domain']}")
print(f"Version: {data['metadata']['file_date']}")
print(f"Content length: {len(data['EULA'])} characters")
```

### 2. Get Specific Document Type
```python
import requests

response = requests.get(
    "http://127.0.0.1:8000/eula/latest",
    params={
        "domain": "chatgpt.com",
        "doc_type": "Privacy Policy"
    }
)

if response.status_code == 200:
    data = response.json()
    print(data['EULA'][:500])  # First 500 chars
else:
    print(f"Error: {response.status_code}")
```

### 3. Get Archive
```python
import requests

response = requests.get(
    "http://127.0.0.1:8000/eula/archive",
    params={"domain": "chatgpt.com"}
)

data = response.json()
print(f"Total versions: {data['metadata']['total_versions']}")
print(f"Document types: {data['metadata']['document_types']}")
print(f"Content length: {len(data['EULA'])} characters")
```

### 4. Test Multiple Domains
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
        print(f"✓ {domain}: {data['metadata']['total_versions']} versions")
    else:
        print(f"✗ {domain}: Not found")
```

### 5. Save to File
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

### 6. Error Handling
```python
import requests

def get_latest_eula(domain, doc_type=None):
    try:
        params = {"domain": domain}
        if doc_type:
            params["doc_type"] = doc_type
        
        response = requests.get(
            "http://127.0.0.1:8000/eula/latest",
            params=params,
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            print(f"Domain {domain} not found")
            return None
        else:
            print(f"Error: {response.status_code}")
            return None
    
    except requests.exceptions.ConnectionError:
        print("Cannot connect to API server")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

# Use it
data = get_latest_eula("chatgpt.com")
if data:
    print(data['metadata'])
```

### 7. Compare Two Versions
```python
import requests

# Get archive
response = requests.get(
    "http://127.0.0.1:8000/eula/archive",
    params={
        "domain": "chatgpt.com",
        "doc_type": "Privacy Policy"
    }
)

archive = response.json()
print(f"Total versions: {archive['metadata']['versions_per_type']['Privacy Policy']}")

# Get latest
response = requests.get(
    "http://127.0.0.1:8000/eula/latest",
    params={
        "domain": "chatgpt.com",
        "doc_type": "Privacy Policy"
    }
)

latest = response.json()
print(f"Latest version: {latest['metadata']['file_date']}")
```

### 8. Monitor Changes
```python
import requests
import time
import hashlib

def get_eula_hash(domain):
    response = requests.get(
        "http://127.0.0.1:8000/eula/latest",
        params={"domain": domain}
    )
    
    if response.status_code == 200:
        content = response.json()['EULA']
        return hashlib.md5(content.encode()).hexdigest()
    return None

# Monitor for changes
domain = "chatgpt.com"
last_hash = get_eula_hash(domain)

while True:
    time.sleep(3600)  # Check every hour
    current_hash = get_eula_hash(domain)
    
    if current_hash != last_hash:
        print(f"⚠️ EULA changed for {domain}!")
        last_hash = current_hash
```

---

## 🌐 Browser Examples

Just paste these URLs in your browser:

**Latest EULA:**
```
http://127.0.0.1:8000/eula/latest?domain=chatgpt.com
```

**Latest Privacy Policy:**
```
http://127.0.0.1:8000/eula/latest?domain=google.com&doc_type=Privacy%20Policy
```

**All Archives:**
```
http://127.0.0.1:8000/eula/archive?domain=chatgpt.com
```

**API Documentation (Interactive):**
```
http://127.0.0.1:8000/docs
```

---

## 📋 Common Use Cases

### Use Case 1: Check if domain has EULA
```python
import requests

def has_eula(domain):
    response = requests.get(
        "http://127.0.0.1:8000/eula/latest",
        params={"domain": domain}
    )
    return response.status_code == 200

print(has_eula("chatgpt.com"))  # True
print(has_eula("nonexistent.com"))  # False
```

### Use Case 2: Get version count
```python
import requests

response = requests.get(
    "http://127.0.0.1:8000/eula/latest",
    params={"domain": "chatgpt.com"}
)

if response.status_code == 200:
    count = response.json()['metadata']['total_versions']
    print(f"Total versions: {count}")
```

### Use Case 3: Bulk download
```python
import requests
import os

domains = ["chatgpt.com", "google.com", "amazon.com"]
output_dir = "eula_downloads"

os.makedirs(output_dir, exist_ok=True)

for domain in domains:
    response = requests.get(
        "http://127.0.0.1:8000/eula/latest",
        params={"domain": domain}
    )
    
    if response.status_code == 200:
        data = response.json()
        filename = os.path.join(output_dir, f"{domain}.md")
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(data['EULA'])
        
        print(f"✓ Downloaded {domain}")
    else:
        print(f"✗ Failed {domain}")
```

---

## 🎯 Quick Reference

| Endpoint | Purpose | Required Params | Optional Params |
|----------|---------|-----------------|-----------------|
| `/eula/latest` | Get newest version | `domain` | `doc_type` |
| `/eula/archive` | Get all versions | `domain` | `doc_type` |

**Document Types:**
- `Privacy Policy`
- `Terms of Service`

**Domain Formats:**
- ✅ `chatgpt.com`
- ✅ `https://google.com`
- ✅ `www.amazon.com`
- ✅ `http://example.in`

---

**🚀 Ready to use! Visit http://127.0.0.1:8000/docs for interactive testing!**
