#!/usr/bin/env python3
"""
Diagnostic API Tool
Helps diagnose API connectivity issues with detailed logging and error reporting.
"""

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

class APIDiagnostic:
    """Diagnostic tool for troubleshooting API issues."""
    
    def __init__(self):
        self.base_url = "https://excel.uat.us.coherent.global/presales/api/v3"
        self.synthetic_key = os.getenv("SYNTHETIC_KEY", "46ac56eb-90ea-4570-80c3-4750ffae5874")
        self.tenant_name = "presales"
        
        self.headers = {
            "Content-Type": "application/json",
            "x-synthetic-key": self.synthetic_key,
            "x-tenant-name": self.tenant_name
        }
        
        self.endpoint = f"{self.base_url}/folders/Luna - Private Equity/services/Meteor - Long-range financial planning model/execute"
    
    def test_basic_connectivity(self):
        """Test basic network connectivity."""
        print("🔍 DIAGNOSTIC: Basic Connectivity Test")
        print("-" * 50)
        
        try:
            # Test basic HTTP connection
            response = requests.get("https://httpbin.org/get", timeout=10)
            print(f"✅ Internet connectivity: OK (Status: {response.status_code})")
        except Exception as e:
            print(f"❌ Internet connectivity: FAILED - {e}")
            return False
        
        try:
            # Test Coherent domain
            base_response = requests.get("https://excel.uat.us.coherent.global", timeout=10)
            print(f"✅ Coherent domain reachable: OK (Status: {base_response.status_code})")
        except Exception as e:
            print(f"❌ Coherent domain: FAILED - {e}")
            return False
        
        return True
    
    def test_api_endpoint(self):
        """Test the specific API endpoint with minimal payload."""
        print("\n🔍 DIAGNOSTIC: API Endpoint Test")
        print("-" * 50)
        
        print(f"Endpoint: {self.endpoint}")
        print(f"Headers: {json.dumps(self.headers, indent=2)}")
        
        # Minimal test payload
        minimal_payload = {
            "request_data": {
                "inputs": {
                    "Capex": 1000,
                    "LineItem": "Income Statement : GAAP Net Income : GAAP Net Income"
                }
            },
            "request_meta": {
                "version_id": None,
                "call_purpose": "Diagnostic Test",
                "source_system": "Diagnostic Tool",
                "service_category": "ALL",
                "requested_output": ["Results"]
            }
        }
        
        print(f"\nMinimal payload:")
        print(json.dumps(minimal_payload, indent=2))
        
        try:
            print("\n🔄 Making API request...")
            response = requests.post(
                self.endpoint,
                headers=self.headers,
                json=minimal_payload,
                timeout=30
            )
            
            print(f"Response Status Code: {response.status_code}")
            print(f"Response Headers: {dict(response.headers)}")
            
            if response.status_code == 200:
                print("✅ API call successful!")
                try:
                    json_response = response.json()
                    print("✅ Valid JSON response received")
                    print(f"Response keys: {list(json_response.keys())}")
                    return json_response
                except json.JSONDecodeError as e:
                    print(f"❌ Invalid JSON in response: {e}")
                    print(f"Raw response text: {response.text[:500]}...")
            else:
                print(f"❌ API call failed with status {response.status_code}")
                print(f"Response text: {response.text}")
                
        except requests.exceptions.Timeout:
            print("❌ Request timed out")
        except requests.exceptions.ConnectionError as e:
            print(f"❌ Connection error: {e}")
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
        
        return None
    
    def test_full_payload(self):
        """Test with a complete payload similar to the original."""
        print("\n🔍 DIAGNOSTIC: Full Payload Test")
        print("-" * 50)
        
        # Complete payload based on working example
        full_payload = {
            "request_data": {
                "inputs": {
                    "Capex": 8000,
                    "existing_leases": [
                        {
                            "Existing leases": "HQ Main",
                            "Lease expiry date": "2027-10-31",
                            "Remaining useful life(years)": 3.83,
                            "Lease renewable": "Yes",
                            "Average new lease life(years)": 7.58,
                            "% of Total lease liabilties": 0.10,
                            "Borrowing Rate pa": 0.083
                        }
                    ],
                    "ExistingPPEUsefulLife": 15,
                    "NewPPEUsefulLife": 15,
                    "GA_personnel_expenses": [
                        {"Y1": 0.0356}, {"Y2": 0.0338}, {"Y3": 0.0321}, {"Y4": 0.0289}, {"Y5": 0.0284}
                    ],
                    "GA_non_personnel_expenses": [
                        {"Y1": 0.0413}, {"Y2": 0.041}, {"Y3": 0.0390}, {"Y4": 0.0370}, {"Y5": 0.0352}
                    ],
                    "RD_personnel_expenses": [
                        {"Y1": 0.0929}, {"Y2": 0.091}, {"Y3": 0.089}, {"Y4": 0.088}, {"Y5": 0.088}
                    ],
                    "RD_non_personnel_expenses": [
                        {"Y1": 0.0312}, {"Y2": 0.031}, {"Y3": 0.029}, {"Y4": 0.029}, {"Y5": 0.029}
                    ],
                    "GlobalSaaSCOGS": 0.843,
                    "GRR": [
                        [{"Y1": 1.0}, {"Y2": 0.999}, {"Y3": 0.999}, {"Y4": 0.999}, {"Y5": 0.999}],
                        [{"Y1": 0.91}, {"Y2": 0.925}, {"Y3": 0.937}, {"Y4": 0.945}, {"Y5": 0.95}]
                    ],
                    "InterestIncome": 0.01,
                    "LongTermDebtBorrowingCosts": [
                        [{"Y1": 0.03}, {"Y2": 0.03}, {"Y3": 0.03}, {"Y4": 0.03}, {"Y5": 0.03}],
                        [{"Y1": 0.06}, {"Y2": 0.06}, {"Y3": 0.06}, {"Y4": 0.06}, {"Y5": 0.06}],
                        [{"Y1": 0.005}, {"Y2": 0.005}, {"Y3": 0.005}, {"Y4": 0.005}, {"Y5": 0.005}],
                        [{"Y1": 0.005}, {"Y2": 0.005}, {"Y3": 0.005}, {"Y4": 0.005}, {"Y5": 0.005}]
                    ],
                    "LineItem": "Income Statement : GAAP Net Income : GAAP Net Income"
                }
            },
            "request_meta": {
                "version_id": None,
                "transaction_date": None,
                "call_purpose": "Full Diagnostic Test",
                "source_system": "Diagnostic Tool",
                "correlation_id": None,
                "service_category": "ALL",
                "requested_output": [
                    "ClientName",
                    "ModelName", 
                    "ProjectName",
                    "Results",
                    "BalanceSheet_lineitems"
                ]
            }
        }
        
        try:
            print("🔄 Making full payload API request...")
            response = requests.post(
                self.endpoint,
                headers=self.headers,
                json=full_payload,
                timeout=60
            )
            
            print(f"Response Status Code: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ Full payload API call successful!")
                try:
                    json_response = response.json()
                    print("✅ Valid JSON response received")
                    
                    # Display structured response info
                    if "response_data" in json_response:
                        outputs = json_response["response_data"].get("outputs", {})
                        print(f"Client: {outputs.get('ClientName', 'N/A')}")
                        print(f"Model: {outputs.get('ModelName', 'N/A')}")
                        print(f"Project: {outputs.get('ProjectName', 'N/A')}")
                        
                        results = outputs.get("Results", [])
                        if results:
                            print(f"Results count: {len(results)}")
                            print(f"First result: {results[0] if results else 'None'}")
                        
                        balance_sheet = outputs.get("BalanceSheet_lineitems", [])
                        if balance_sheet:
                            print(f"Balance sheet items: {len(balance_sheet)}")
                    
                    return json_response
                    
                except json.JSONDecodeError as e:
                    print(f"❌ Invalid JSON in response: {e}")
                    print(f"Raw response: {response.text[:1000]}...")
            else:
                print(f"❌ API call failed with status {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Full payload test failed: {e}")
        
        return None
    
    def run_full_diagnostic(self):
        """Run complete diagnostic suite."""
        print("🩺 API CONNECTIVITY DIAGNOSTIC SUITE")
        print("=" * 60)
        
        # Test 1: Basic connectivity
        if not self.test_basic_connectivity():
            print("\n❌ Basic connectivity failed - check internet connection")
            return
        
        # Test 2: API endpoint with minimal payload
        minimal_result = self.test_api_endpoint()
        if minimal_result is None:
            print("\n❌ API endpoint test failed - check credentials and endpoint")
            return
        
        # Test 3: Full payload
        full_result = self.test_full_payload()
        if full_result is None:
            print("\n❌ Full payload test failed - check payload format")
            return
        
        print("\n" + "=" * 60)
        print("🎉 ALL DIAGNOSTIC TESTS PASSED!")
        print("The API is working correctly. UI connectivity issues may be")
        print("related to payload formatting or error handling logic.")
        print("=" * 60)

def main():
    """Run the diagnostic suite."""
    diagnostic = APIDiagnostic()
    diagnostic.run_full_diagnostic()

if __name__ == "__main__":
    main()