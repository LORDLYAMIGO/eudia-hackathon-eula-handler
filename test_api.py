"""
Test script for EULA Handler API
Run this after starting the server to test the endpoints
"""
import requests
import json


BASE_URL = "http://localhost:8000"


def print_response(response, limit_chars=500):
    """Print API response in a readable format"""
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}\n")
    
    try:
        data = response.json()
        
        # If EULA is in response, show limited preview
        if "EULA" in data:
            eula_content = data["EULA"]
            data["EULA"] = eula_content[:limit_chars] + "..." if len(eula_content) > limit_chars else eula_content
        
        print(json.dumps(data, indent=2))
    except:
        print(response.text)
    print("\n" + "="*80 + "\n")


def test_root():
    """Test root endpoint"""
    print("Testing Root Endpoint:")
    print(f"GET {BASE_URL}/")
    response = requests.get(f"{BASE_URL}/")
    print_response(response)


def test_latest_eula():
    """Test latest EULA endpoint with various formats"""
    test_cases = [
        ("chatgpt.com", None),
        ("https://google.com", "Privacy Policy"),
        ("www.amazon.com", None),
        ("chat.openai.com", "Terms of Service"),
    ]
    
    for domain, doc_type in test_cases:
        print(f"Testing Latest EULA for: {domain}")
        params = {"domain": domain}
        if doc_type:
            params["doc_type"] = doc_type
        
        url = f"{BASE_URL}/eula/latest"
        print(f"GET {url}")
        print(f"Params: {params}")
        
        response = requests.get(url, params=params)
        print_response(response, limit_chars=300)


def test_archive_eula():
    """Test archive EULA endpoint"""
    test_cases = [
        ("chatgpt.com", None),
        ("https://google.com", "Privacy Policy"),
    ]
    
    for domain, doc_type in test_cases:
        print(f"Testing Archive EULA for: {domain}")
        params = {"domain": domain}
        if doc_type:
            params["doc_type"] = doc_type
        
        url = f"{BASE_URL}/eula/archive"
        print(f"GET {url}")
        print(f"Params: {params}")
        
        response = requests.get(url, params=params)
        print_response(response, limit_chars=500)


def test_error_cases():
    """Test error handling"""
    print("Testing Error Cases:")
    
    # Non-existent domain
    print("1. Non-existent domain:")
    response = requests.get(f"{BASE_URL}/eula/latest", params={"domain": "nonexistent-domain-xyz.com"})
    print_response(response)
    
    # Invalid doc_type
    print("2. Testing with available domain:")
    response = requests.get(f"{BASE_URL}/eula/latest", params={"domain": "github.com"})
    print_response(response, limit_chars=300)


if __name__ == "__main__":
    print("="*80)
    print("EULA Handler API - Test Suite")
    print("="*80)
    print()
    
    try:
        # Test root
        test_root()
        
        # Test latest endpoint
        test_latest_eula()
        
        # Test archive endpoint
        test_archive_eula()
        
        # Test error cases
        test_error_cases()
        
        print("="*80)
        print("All tests completed!")
        print("="*80)
        
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to the API server.")
        print("Please make sure the server is running:")
        print("  cd api")
        print("  python app.py")
    except Exception as e:
        print(f"ERROR: {str(e)}")
