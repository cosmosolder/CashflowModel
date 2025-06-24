#!/usr/bin/env python3
"""
Demo Financial Planning Model UI
Demonstrates the API connectivity and formatted output using predefined scenarios.
"""

import requests
import json
import os
from typing import Dict, List
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

class DemoFinancialPlanningUI:
    """
    Demo version of the Financial Planning Model UI.
    Uses predefined scenarios to demonstrate API connectivity and formatted output.
    """
    
    def __init__(self):
        """Initialize the UI with API connection details."""
        self.base_url = "https://excel.uat.us.coherent.global/presales/api/v3"
        self.synthetic_key = os.getenv("SYNTHETIC_KEY", "46ac56eb-90ea-4570-80c3-4750ffae5874")
        self.tenant_name = "presales"
        
        self.headers = {
            "Content-Type": "application/json",
            "x-synthetic-key": self.synthetic_key,
            "x-tenant-name": self.tenant_name
        }
        
        self.endpoint = f"{self.base_url}/folders/Luna - Private Equity/services/Meteor - Long-range financial planning model/execute"
    
    def get_demo_scenarios(self) -> List[Dict]:
        """Get predefined demo scenarios."""
        return [
            {
                "name": "Conservative Growth",
                "description": "Low-risk scenario with modest growth projections",
                "params": {
                    "capex": 5000,
                    "ga_personnel_rates": [0.030, 0.028, 0.026, 0.024, 0.022],
                    "ga_non_personnel_rates": [0.035, 0.033, 0.031, 0.029, 0.027],
                    "rd_personnel_rates": [0.080, 0.075, 0.070, 0.065, 0.060],
                    "rd_non_personnel_rates": [0.025, 0.024, 0.023, 0.022, 0.021],
                    "global_saas_cogs": 0.800,
                    "interest_income": 0.015,
                    "line_item": "Income Statement : GAAP Net Income : GAAP Net Income"
                }
            },
            {
                "name": "Aggressive Expansion",
                "description": "High-growth scenario with increased investments",
                "params": {
                    "capex": 15000,
                    "ga_personnel_rates": [0.045, 0.042, 0.040, 0.038, 0.036],
                    "ga_non_personnel_rates": [0.050, 0.048, 0.046, 0.044, 0.042],
                    "rd_personnel_rates": [0.120, 0.115, 0.110, 0.105, 0.100],
                    "rd_non_personnel_rates": [0.040, 0.038, 0.036, 0.034, 0.032],
                    "global_saas_cogs": 0.900,
                    "interest_income": 0.008,
                    "line_item": "Income Statement : Revenue : Total Revenue"
                }
            },
            {
                "name": "Balanced Portfolio",
                "description": "Moderate growth with balanced risk/return",
                "params": {
                    "capex": 8000,
                    "ga_personnel_rates": [0.0356, 0.0338, 0.0321, 0.0289, 0.0284],
                    "ga_non_personnel_rates": [0.0413, 0.041, 0.0390, 0.0370, 0.0352],
                    "rd_personnel_rates": [0.0929, 0.091, 0.089, 0.088, 0.088],
                    "rd_non_personnel_rates": [0.0312, 0.031, 0.029, 0.029, 0.029],
                    "global_saas_cogs": 0.843,
                    "interest_income": 0.010,
                    "line_item": "Balance Sheet : Total Assets : Total Assets"
                }
            }
        ]
    
    def execute_model_api(self, params: Dict, scenario_name: str) -> Dict:
        """Execute the financial model API call."""
        print(f"🔄 Executing '{scenario_name}' scenario...")
        
        # Format rates into required structure
        years = ["Y1", "Y2", "Y3", "Y4", "Y5"]
        
        def format_rates(rates):
            return [{year: rate} for year, rate in zip(years, rates)]
        
        # Default lease structure
        existing_leases = [
            {
                "Existing leases": "HQ Main",
                "Lease expiry date": "2027-10-31",
                "Remaining useful life(years)": 3.83,
                "Lease renewable": "Yes",
                "Average new lease life(years)": 7.58,
                "% of Total lease liabilties": 0.10,
                "Borrowing Rate pa": 0.083
            },
            {
                "Existing leases": "Branch Office",
                "Lease expiry date": "2025-06-30",
                "Remaining useful life(years)": 1.5,
                "Lease renewable": "No",
                "Average new lease life(years)": 3.25,
                "% of Total lease liabilties": 0.05,
                "Borrowing Rate pa": 0.0804
            }
        ]
        
        # Default GRR and debt borrowing costs
        grr_rates = [
            [1.0, 0.999, 0.999, 0.999, 0.999],
            [0.91, 0.925, 0.937, 0.945, 0.95]
        ]
        
        debt_borrowing_costs = [
            [0.03, 0.03, 0.03, 0.03, 0.03],
            [0.06, 0.06, 0.06, 0.06, 0.06],
            [0.005, 0.005, 0.005, 0.005, 0.005],
            [0.005, 0.005, 0.005, 0.005, 0.005]
        ]
        
        def format_multi_rates(rate_lists):
            return [format_rates(rates) for rates in rate_lists]
        
        payload = {
            "request_data": {
                "inputs": {
                    "Capex": params['capex'],
                    "existing_leases": existing_leases,
                    "ExistingPPEUsefulLife": 15,
                    "NewPPEUsefulLife": 15,
                    "GA_personnel_expenses": format_rates(params['ga_personnel_rates']),
                    "GA_non_personnel_expenses": format_rates(params['ga_non_personnel_rates']),
                    "RD_personnel_expenses": format_rates(params['rd_personnel_rates']),
                    "RD_non_personnel_expenses": format_rates(params['rd_non_personnel_rates']),
                    "GlobalSaaSCOGS": params['global_saas_cogs'],
                    "GRR": format_multi_rates(grr_rates),
                    "InterestIncome": params['interest_income'],
                    "LongTermDebtBorrowingCosts": format_multi_rates(debt_borrowing_costs),
                    "LineItem": params['line_item']
                }
            },
            "request_meta": {
                "version_id": None,
                "transaction_date": None,
                "call_purpose": f"Demo UI - {scenario_name}",
                "source_system": "Demo Python UI",
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
            response = requests.post(
                self.endpoint,
                headers=self.headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}
    
    def format_and_display_results(self, response: Dict, scenario: Dict):
        """Format and display the API response in a user-friendly way."""
        print("\n" + "=" * 80)
        print(f"📊 RESULTS: {scenario['name'].upper()}")
        print("=" * 80)
        print(f"📝 {scenario['description']}")
        print("-" * 80)
        
        # Check for actual errors (not just presence of error field)
        if "error" in response and response["error"] is not None and response["error"] != "":
            print(f"❌ Error: {response['error']}")
            return False
        
        # Check response status
        if response.get("status") == "error":
            error_msg = response.get("error", "Unknown API error")
            print(f"❌ API Error: {error_msg}")
            return False
        
        # Extract response data
        if "response_data" not in response or "outputs" not in response["response_data"]:
            print("❌ Invalid response format received")
            return False
        
        outputs = response["response_data"]["outputs"]
        
        # Display metadata
        print(f"Client: {outputs.get('ClientName', 'N/A')}")
        print(f"Model: {outputs.get('ModelName', 'N/A')}")
        print(f"Project: {outputs.get('ProjectName', 'N/A')}")
        print(f"Analysis: {scenario['params']['line_item']}")
        print("-" * 80)
        
        # Display key parameters
        print("🔧 KEY PARAMETERS:")
        print(f"  CAPEX: ${scenario['params']['capex']:,}")
        print(f"  Global SaaS COGS: {scenario['params']['global_saas_cogs']:.1%}")
        print(f"  Interest Income: {scenario['params']['interest_income']:.1%}")
        print(f"  GA Personnel Y1: {scenario['params']['ga_personnel_rates'][0]:.2%}")
        print(f"  R&D Personnel Y1: {scenario['params']['rd_personnel_rates'][0]:.2%}")
        
        # Display results
        results = outputs.get("Results", [])
        if results:
            print("\n💰 FINANCIAL PROJECTIONS:")
            
            try:
                if isinstance(results[0], dict):
                    # Display as formatted table
                    df = pd.DataFrame(results)
                    
                    # Format numeric columns for better display
                    for col in df.columns:
                        if df[col].dtype in ['float64', 'int64']:
                            df[col] = df[col].apply(lambda x: f"${x:,.0f}" if not pd.isna(x) else "N/A")
                    
                    print(df.to_string(index=False, max_colwidth=20))
                    
                    # Calculate and display insights if numeric data available
                    numeric_df = pd.DataFrame(results)
                    numeric_cols = numeric_df.select_dtypes(include=['number']).columns
                    
                    if len(numeric_cols) > 0:
                        print(f"\n🔍 KEY INSIGHTS:")
                        for col in numeric_cols[:3]:  # Show top 3 numeric columns
                            values = numeric_df[col].dropna()
                            if len(values) > 1:
                                trend = "📈 Growing" if values.iloc[-1] > values.iloc[0] else "📉 Declining"
                                change = ((values.iloc[-1] - values.iloc[0]) / abs(values.iloc[0])) * 100
                                print(f"  {col}: {trend} ({change:+.1f}% over period)")
                else:
                    # Display as simple list
                    for i, result in enumerate(results, 1):
                        print(f"  Result {i}: {result}")
                        
            except Exception as e:
                print(f"  Raw results: {results}")
                print(f"  (Display formatting error: {e})")
        
        # Display balance sheet items if available
        balance_sheet = outputs.get("BalanceSheet_lineitems", [])
        if balance_sheet:
            print(f"\n🏦 BALANCE SHEET ITEMS:")
            try:
                if isinstance(balance_sheet[0], dict):
                    bs_df = pd.DataFrame(balance_sheet)
                    print(bs_df.to_string(index=False, max_colwidth=30))
                else:
                    for item in balance_sheet[:5]:  # Show first 5 items
                        print(f"  • {item}")
                    if len(balance_sheet) > 5:
                        print(f"  ... and {len(balance_sheet) - 5} more items")
            except Exception as e:
                print(f"  Raw balance sheet: {balance_sheet}")
                print(f"  (Display formatting error: {e})")
        
        print("\n✅ Scenario analysis completed!")
        return True
    
    def run_demo_scenarios(self):
        """Run all demo scenarios."""
        print("=" * 80)
        print("🏦 FINANCIAL PLANNING MODEL - DEMO SCENARIOS")
        print("=" * 80)
        print("This demo runs predefined scenarios to showcase the API connectivity")
        print("and formatted output capabilities.")
        print("=" * 80)
        
        scenarios = self.get_demo_scenarios()
        successful_runs = 0
        
        for i, scenario in enumerate(scenarios, 1):
            print(f"\n🚀 Running Scenario {i}/{len(scenarios)}: {scenario['name']}")
            
            # Execute API call
            response = self.execute_model_api(scenario['params'], scenario['name'])
            
            # Display results
            success = self.format_and_display_results(response, scenario)
            if success:
                successful_runs += 1
            
            # Add separator between scenarios
            if i < len(scenarios):
                print("\n" + "🔄" * 40)
        
        # Summary
        print("\n" + "=" * 80)
        print("📋 DEMO SUMMARY")
        print("=" * 80)
        print(f"Total scenarios run: {len(scenarios)}")
        print(f"Successful executions: {successful_runs}")
        print(f"Success rate: {(successful_runs/len(scenarios)*100):.1f}%")
        
        if successful_runs == len(scenarios):
            print("🎉 All scenarios completed successfully!")
        elif successful_runs > 0:
            print("⚠️  Some scenarios had issues - check API connectivity")
        else:
            print("❌ No scenarios completed - check API configuration")
        
        print("=" * 80)

def main():
    """Main entry point for the demo UI."""
    ui = DemoFinancialPlanningUI()
    ui.run_demo_scenarios()

if __name__ == "__main__":
    main()