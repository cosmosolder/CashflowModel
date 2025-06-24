#!/usr/bin/env python3
"""
Demo script to test the React UI backend connectivity
"""

import requests
import json
import time

def test_backend_health():
    """Test backend health endpoint"""
    try:
        response = requests.get('http://localhost:5001/api/health', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Backend Health Check Passed")
            print(f"   Status: {data['status']}")
            print(f"   Service: {data['service']}")
            print(f"   Timestamp: {data['timestamp']}")
            return True
        else:
            print(f"❌ Backend Health Check Failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend - ensure server is running on port 5001")
        return False
    except Exception as e:
        print(f"❌ Backend Health Check Error: {e}")
        return False

def test_financial_model_api():
    """Test financial model endpoint with sample data"""
    print("\n🧪 Testing Financial Model API...")
    
    sample_params = {
        "capex": 8000,
        "gaPersonnelRates": [0.0356, 0.0338, 0.0321, 0.0289, 0.0284],
        "gaNonPersonnelRates": [0.0413, 0.041, 0.0390, 0.0370, 0.0352],
        "rdPersonnelRates": [0.0929, 0.091, 0.089, 0.088, 0.088],
        "rdNonPersonnelRates": [0.0312, 0.031, 0.029, 0.029, 0.029],
        "globalSaasCogs": 0.843,
        "interestIncome": 0.01,
        "lineItem": "Income Statement : GAAP Net Income : GAAP Net Income",
        "callPurpose": "React UI Demo Test"
    }
    
    try:
        print("📤 Sending request to backend...")
        response = requests.post(
            'http://localhost:5001/api/financial-model',
            json=sample_params,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Financial Model API Test Passed")
            print(f"   Client: {data.get('clientName', 'N/A')}")
            print(f"   Model: {data.get('modelName', 'N/A')}")
            print(f"   Project: {data.get('projectName', 'N/A')}")
            
            results = data.get('results', [])
            if results and len(results) > 0:
                print(f"   Results Count: {len(results)}")
                first_result = results[0]
                if isinstance(first_result, dict):
                    years = list(first_result.keys())
                    print(f"   Years: {years}")
                    print(f"   Sample Values: {list(first_result.values())[:3]}...")
            
            balance_sheet = data.get('balanceSheetItems', [])
            print(f"   Balance Sheet Items: {len(balance_sheet)}")
            
            return True
        else:
            print(f"❌ Financial Model API Test Failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Financial Model API Test Error: {e}")
        return False

def test_predefined_scenarios():
    """Test predefined scenarios endpoint"""
    print("\n📋 Testing Predefined Scenarios API...")
    
    try:
        response = requests.get('http://localhost:5001/api/scenarios/predefined', timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            scenarios = data.get('scenarios', [])
            print("✅ Predefined Scenarios API Test Passed")
            print(f"   Scenarios Available: {len(scenarios)}")
            
            for scenario in scenarios:
                print(f"   • {scenario['name']}: {scenario['description']}")
            
            return True
        else:
            print(f"❌ Predefined Scenarios API Test Failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Predefined Scenarios API Test Error: {e}")
        return False

def main():
    """Run all backend tests"""
    print("🏦 Financial Planning Model - React UI Backend Tests")
    print("=" * 60)
    
    # Test 1: Health check
    health_ok = test_backend_health()
    
    if not health_ok:
        print("\n💡 To start the backend server:")
        print("   cd backend && python3 app.py")
        return
    
    # Test 2: Financial model API
    model_ok = test_financial_model_api()
    
    # Test 3: Predefined scenarios
    scenarios_ok = test_predefined_scenarios()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    tests = [
        ("Backend Health Check", health_ok),
        ("Financial Model API", model_ok),
        ("Predefined Scenarios API", scenarios_ok)
    ]
    
    passed = sum(1 for _, ok in tests if ok)
    total = len(tests)
    
    for test_name, ok in tests:
        status = "✅ PASS" if ok else "❌ FAIL"
        print(f"{test_name:<25} {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All backend tests passed! React UI is ready to use.")
        print("\n🚀 To start the full application:")
        print("   ./start_full_ui.sh")
        print("\n🌐 Frontend will be available at: http://localhost:3000")
    else:
        print("⚠️  Some tests failed. Check the error messages above.")

if __name__ == "__main__":
    main()