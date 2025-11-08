# API Routes

This repository exposes two HTTP endpoints to retrieve EULA documents (Privacy Policies and Terms of Service).

1) GET /eula/latest

- Purpose: Return the latest markdown file for a given domain.
- Query parameters:
	- domain (required) — domain in any format (examples: `chatgpt.com`, `https://google.com`, `www.example.com`).
	- doc_type (optional) — either `Privacy Policy` or `Terms of Service`. If omitted, returns the first available document type for the domain.
- Response: JSON with keys:
	- `EULA`: string containing the markdown contents of the latest file
	- `metadata`: object with `domain`, `document_type`, `file_name`, `file_date`, and `total_versions`

Example:

GET /eula/latest?domain=chatgpt.com

Response (abridged):
```
{
	"EULA": "# Privacy Policy\n...",
	"metadata": {
		"domain": "chat.openai.com",
		"document_type": "Privacy Policy",
		"file_name": "2025-11-01T00-31-13Z.md",
		"file_date": "2025-11-01T00-31-13Z",
		"total_versions": 19
	}
}
```

2) GET /eula/archive

- Purpose: Return all markdown files for a domain concatenated/chained together (archive).
- Query parameters:
	- domain (required) — domain in any format (examples: `chatgpt.com`, `https://google.com`, `www.example.com`).
	- doc_type (optional) — either `Privacy Policy` or `Terms of Service`. If omitted, returns all available document types for the domain.
- Response: JSON with keys:
	- `EULA`: string containing all markdown files concatenated with separators and per-version metadata
	- `metadata`: object with `domain`, `document_types`, `total_versions`, and `versions_per_type`

Example:

GET /eula/archive?domain=chatgpt.com

Response (abridged):
```
{
	"EULA": "==== Document Type: Privacy Policy - Version: 2023-10-16T12-30-08Z ====\n...\n==== Document Type: Terms of Service - Version: 2024-01-02T00-00-00Z ====\n...",
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

Notes:
- Domain input is normalized (protocols and `www.` stripped) and matched case-insensitively to folders inside the `EULA/` directory.
- If a domain or document type is not found, the endpoints return a 404 with an explanatory error object.
