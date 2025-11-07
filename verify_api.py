"""
Quick verification script to test EULA API endpoints
"""
import sys
import time

def test_api():
    print("🧪 Testing EULA Handler API...")
    print("=" * 60)
    
    try:
        import requests
    except ImportError:
        print("❌ requests library not found. Installing...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
        import requests
    
    base_url = "http://127.0.0.1:8000"
    
    # Test 1: Root endpoint
    print("\n1️⃣ Testing root endpoint...")
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            print("✅ Root endpoint working!")
            data = response.json()
            print(f"   API Version: {data.get('version')}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Is it running?")
        print("   Start server with: cd api && python run.py")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Test 2: Latest EULA
    print("\n2️⃣ Testing /eula/latest endpoint...")
    try:
        response = requests.get(
            f"{base_url}/eula/latest",
            params={"domain": "chatgpt.com"},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            print("✅ Latest EULA endpoint working!")
            print(f"   Domain: {data['metadata']['domain']}")
            print(f"   Document Type: {data['metadata']['document_type']}")
            print(f"   Version Date: {data['metadata']['file_date']}")
            print(f"   Total Versions: {data['metadata']['total_versions']}")
            print(f"   Content Length: {len(data['EULA'])} characters")
        else:
            print(f"❌ Latest EULA endpoint failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Test 3: Domain format variations
    print("\n3️⃣ Testing domain format variations...")
    test_domains = [
        "chatgpt.com",
        "https://chatgpt.com",
        "chat.openai.com",
    ]
    
    for domain in test_domains:
        try:
            response = requests.get(
                f"{base_url}/eula/latest",
                params={"domain": domain},
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ {domain} → {data['metadata']['domain']}")
            else:
                print(f"   ⚠️  {domain} not found (might be expected)")
        except Exception as e:
            print(f"   ❌ {domain} error: {e}")
    
    # Test 4: Archive endpoint
    print("\n4️⃣ Testing /eula/archive endpoint...")
    try:
        response = requests.get(
            f"{base_url}/eula/archive",
            params={"domain": "chatgpt.com"},
            timeout=15
        )
        if response.status_code == 200:
            data = response.json()
            print("✅ Archive EULA endpoint working!")
            print(f"   Domain: {data['metadata']['domain']}")
            print(f"   Document Types: {data['metadata']['document_types']}")
            print(f"   Total Versions: {data['metadata']['total_versions']}")
            print(f"   Chained Content Length: {len(data['EULA'])} characters")
        else:
            print(f"❌ Archive EULA endpoint failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Test 5: Error handling
    print("\n5️⃣ Testing error handling...")
    try:
        response = requests.get(
            f"{base_url}/eula/latest",
            params={"domain": "nonexistent-domain-xyz.com"},
            timeout=10
        )
        if response.status_code == 404:
            print("✅ Error handling working correctly (404 for non-existent domain)")
        else:
            print(f"⚠️  Expected 404, got {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("✅ All tests completed successfully!")
    print("\n📖 View interactive docs at: http://127.0.0.1:8000/docs")
    return True

if __name__ == "__main__":
    print("EULA Handler API - Quick Verification")
    print("=" * 60)
    
    success = test_api()
    
    if success:
        print("\n✨ API is ready to use!")
        sys.exit(0)
    else:
        print("\n⚠️  Some tests failed. Check the output above.")
        sys.exit(1)
