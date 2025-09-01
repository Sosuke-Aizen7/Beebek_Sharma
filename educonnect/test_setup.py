#!/usr/bin/env python3
"""
Test script to verify EduConnect setup
"""
import requests
import json
import time

def test_backend_health():
    """Test if Django backend is running"""
    try:
        response = requests.get('http://localhost:8000/api/statistics/', timeout=10)
        if response.status_code == 200:
            print("✅ Backend is running and responding")
            return True
        else:
            print(f"❌ Backend returned status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Backend connection failed: {e}")
        return False

def test_frontend_health():
    """Test if React frontend is running"""
    try:
        response = requests.get('http://localhost:3000', timeout=10)
        if response.status_code == 200:
            print("✅ Frontend is running and responding")
            return True
        else:
            print(f"❌ Frontend returned status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Frontend connection failed: {e}")
        return False

def test_database_data():
    """Test if sample data is loaded"""
    try:
        response = requests.get('http://localhost:8000/api/universities/', timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('count', 0) > 0:
                print(f"✅ Database has {data['count']} universities")
                return True
            else:
                print("❌ No universities found in database")
                return False
        else:
            print(f"❌ Database test failed with status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_api_endpoints():
    """Test key API endpoints"""
    endpoints = [
        '/courses/',
        '/universities/',
        '/popular/',
        '/featured-universities/',
        '/statistics/'
    ]
    
    passed = 0
    for endpoint in endpoints:
        try:
            response = requests.get(f'http://localhost:8000/api{endpoint}', timeout=5)
            if response.status_code == 200:
                print(f"✅ {endpoint} - OK")
                passed += 1
            else:
                print(f"❌ {endpoint} - Status {response.status_code}")
        except requests.exceptions.RequestException:
            print(f"❌ {endpoint} - Connection failed")
    
    print(f"📊 API Tests: {passed}/{len(endpoints)} passed")
    return passed == len(endpoints)

def main():
    """Run all tests"""
    print("🧪 Testing EduConnect Setup...")
    print("=" * 50)
    
    # Wait a moment for services to be ready
    print("⏳ Waiting for services to start...")
    time.sleep(5)
    
    tests = [
        ("Backend Health", test_backend_health),
        ("Frontend Health", test_frontend_health),
        ("Database Data", test_database_data),
        ("API Endpoints", test_api_endpoints),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Testing {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"   ⚠️  {test_name} failed")
    
    print("\n" + "=" * 50)
    print(f"📊 Overall Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! EduConnect is ready to use.")
        print("\n🌟 Next Steps:")
        print("1. Open http://localhost:3000 in your browser")
        print("2. Register a new account or login with admin@educonnect.com / admin123")
        print("3. Explore courses and universities")
        print("4. Try the AI assistant features")
        print("5. Configure OpenAI API key for full AI functionality")
    else:
        print("❌ Some tests failed. Check the logs above for details.")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure Docker is running")
        print("2. Check if all containers are started: docker-compose ps")
        print("3. View logs: docker-compose logs")
        print("4. Restart services: docker-compose restart")
    
    return passed == total

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)