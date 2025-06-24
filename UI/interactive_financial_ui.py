#!/usr/bin/env python3
"""
Interactive Financial Planning Model UI
Uses the Anthropic-UI.py connectivity as a template to create an interactive interface
for the Meteor Long-range Financial Planning Model API.
"""

import requests
import json
import os
from typing import Dict, List, Optional, Union
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

class InteractiveFinancialPlanningUI:
    """
    Interactive UI for the Financial Planning Model API.
    Accepts user input, validates parameters, makes API calls, and displays formatted results.
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
    
    def display_welcome(self):
        """Display welcome message and instructions."""
        print("=" * 80)
        print("🏦 INTERACTIVE FINANCIAL PLANNING MODEL")
        print("=" * 80)
        print("This tool helps you create financial projections using the Meteor model.")
        print("You can customize key parameters or use defaults for quick analysis.")
        print("-" * 80)
    
    def get_user_choice(self, prompt: str, options: List[str], default: str = None) -> str:
        """Get validated user choice from a list of options."""
        while True:
            if default:
                user_input = input(f"{prompt} [{default}]: ").strip()
                if not user_input:
                    return default
            else:
                user_input = input(f"{prompt}: ").strip()
            
            if user_input.lower() in [opt.lower() for opt in options]:
                return user_input.lower()
            
            print(f"❌ Invalid choice. Please select from: {', '.join(options)}")
    
    def get_numeric_input(self, prompt: str, default: float = None, min_val: float = None, max_val: float = None) -> float:
        """Get validated numeric input from user."""
        while True:
            try:
                if default is not None:
                    user_input = input(f"{prompt} [{default}]: ").strip()
                    if not user_input:
                        return default
                else:
                    user_input = input(f"{prompt}: ").strip()
                
                value = float(user_input)
                
                if min_val is not None and value < min_val:
                    print(f"❌ Value must be at least {min_val}")
                    continue
                
                if max_val is not None and value > max_val:
                    print(f"❌ Value must be at most {max_val}")
                    continue
                
                return value
            
            except ValueError:
                print("❌ Please enter a valid number")
    
    def get_yearly_rates(self, rate_type: str, defaults: List[float]) -> List[float]:
        """Get 5-year rate projections from user."""
        print(f"\n📊 {rate_type} Rates (5-year projection)")
        print("Enter rates as decimals (e.g., 0.05 for 5%)")
        
        use_defaults = self.get_user_choice(
            "Use default rates?", 
            ["yes", "no"], 
            "yes"
        )
        
        if use_defaults == "yes":
            return defaults
        
        rates = []
        years = ["Y1", "Y2", "Y3", "Y4", "Y5"]
        
        for i, year in enumerate(years):
            rate = self.get_numeric_input(
                f"  {year} rate", 
                defaults[i], 
                0.0, 
                1.0
            )
            rates.append(rate)
        
        return rates
    
    def create_lease_entry(self, lease_num: int) -> Dict:
        """Create a lease entry with user input."""
        print(f"\n🏢 Lease #{lease_num} Details")
        
        lease_name = input(f"Lease name [Lease {lease_num}]: ").strip()
        if not lease_name:
            lease_name = f"Lease {lease_num}"
        
        # Get expiry date
        while True:
            expiry_date = input("Lease expiry date (YYYY-MM-DD) [2027-12-31]: ").strip()
            if not expiry_date:
                expiry_date = "2027-12-31"
            
            try:
                datetime.strptime(expiry_date, "%Y-%m-%d")
                break
            except ValueError:
                print("❌ Please enter date in YYYY-MM-DD format")
        
        remaining_life = self.get_numeric_input("Remaining useful life (years)", 3.0, 0.1, 50.0)
        
        renewable = self.get_user_choice("Is lease renewable?", ["yes", "no"], "yes") == "yes"
        
        avg_new_lease_life = self.get_numeric_input("Average new lease life (years)", 5.0, 1.0, 20.0)
        
        lease_liability_pct = self.get_numeric_input("% of total lease liabilities", 0.10, 0.0, 1.0)
        
        borrowing_rate = self.get_numeric_input("Borrowing rate per annum", 0.08, 0.0, 1.0)
        
        return {
            "Existing leases": lease_name,
            "Lease expiry date": expiry_date,
            "Remaining useful life(years)": remaining_life,
            "Lease renewable": "Yes" if renewable else "No",
            "Average new lease life(years)": avg_new_lease_life,
            "% of Total lease liabilties": lease_liability_pct,
            "Borrowing Rate pa": borrowing_rate
        }
    
    def collect_input_parameters(self) -> Dict:
        """Collect all input parameters from user."""
        params = {}
        
        print("\n📈 FINANCIAL MODEL PARAMETERS")
        print("-" * 40)
        
        # Capital Expenditure
        params['capex'] = self.get_numeric_input("Capital Expenditure (CAPEX)", 8000, 0)
        
        # PPE Life
        params['existing_ppe_life'] = int(self.get_numeric_input("Existing PPE useful life (years)", 15, 1, 50))
        params['new_ppe_life'] = int(self.get_numeric_input("New PPE useful life (years)", 15, 1, 50))
        
        # Lease Configuration
        use_default_leases = self.get_user_choice(
            "\nUse default lease structure?", 
            ["yes", "no"], 
            "yes"
        )
        
        if use_default_leases == "no":
            num_leases = int(self.get_numeric_input("Number of leases", 2, 1, 10))
            params['existing_leases'] = []
            for i in range(num_leases):
                params['existing_leases'].append(self.create_lease_entry(i + 1))
        
        # Expense Rates
        print("\n💼 EXPENSE RATE CONFIGURATION")
        
        # GA Personnel Rates
        params['ga_personnel_rates'] = self.get_yearly_rates(
            "GA Personnel Expense", 
            [0.0356, 0.0338, 0.0321, 0.0289, 0.0284]
        )
        
        # GA Non-Personnel Rates  
        params['ga_non_personnel_rates'] = self.get_yearly_rates(
            "GA Non-Personnel Expense", 
            [0.0413, 0.041, 0.0390, 0.0370, 0.0352]
        )
        
        # R&D Personnel Rates
        params['rd_personnel_rates'] = self.get_yearly_rates(
            "R&D Personnel Expense", 
            [0.0929, 0.091, 0.089, 0.088, 0.088]
        )
        
        # R&D Non-Personnel Rates
        params['rd_non_personnel_rates'] = self.get_yearly_rates(
            "R&D Non-Personnel Expense", 
            [0.0312, 0.031, 0.029, 0.029, 0.029]
        )
        
        # Additional Parameters
        print("\n⚙️  ADDITIONAL PARAMETERS")
        params['global_saas_cogs'] = self.get_numeric_input("Global SaaS COGS rate", 0.843, 0.0, 1.0)
        params['interest_income'] = self.get_numeric_input("Interest income rate", 0.01, 0.0, 1.0)
        
        # Analysis Type
        print("\n📊 ANALYSIS CONFIGURATION")
        line_items = [
            "Income Statement : GAAP Net Income : GAAP Net Income",
            "Income Statement : Revenue : Total Revenue",
            "Balance Sheet : Total Assets : Total Assets",
            "Cash Flow : Operating Cash Flow : Operating Cash Flow"
        ]
        
        print("Available line items:")
        for i, item in enumerate(line_items, 1):
            print(f"  {i}. {item}")
        
        choice = int(self.get_numeric_input("Select line item (1-4)", 1, 1, 4))
        params['line_item'] = line_items[choice - 1]
        
        # Call Purpose
        params['call_purpose'] = input("Analysis purpose [Interactive UI Analysis]: ").strip()
        if not params['call_purpose']:
            params['call_purpose'] = "Interactive UI Analysis"
        
        return params
    
    def execute_model_api(self, params: Dict) -> Dict:
        """Execute the financial model API call."""
        print("\n🔄 Executing financial model...")
        
        # Format rates into required structure
        years = ["Y1", "Y2", "Y3", "Y4", "Y5"]
        
        def format_rates(rates):
            return [{year: rate} for year, rate in zip(years, rates)]
        
        # Default values for optional parameters
        if 'existing_leases' not in params:
            params['existing_leases'] = [
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
                    "existing_leases": params['existing_leases'],
                    "ExistingPPEUsefulLife": params['existing_ppe_life'],
                    "NewPPEUsefulLife": params['new_ppe_life'],
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
                "call_purpose": params['call_purpose'],
                "source_system": "Interactive Python UI",
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
    
    def format_and_display_results(self, response: Dict, params: Dict):
        """Format and display the API response in a user-friendly way."""
        print("\n" + "=" * 80)
        print("📊 FINANCIAL PROJECTION RESULTS")
        print("=" * 80)
        
        if "error" in response:
            print(f"❌ Error: {response['error']}")
            return
        
        # Extract response data
        if "response_data" not in response or "outputs" not in response["response_data"]:
            print("❌ Invalid response format received")
            return
        
        outputs = response["response_data"]["outputs"]
        
        # Display metadata
        print(f"Client: {outputs.get('ClientName', 'N/A')}")
        print(f"Model: {outputs.get('ModelName', 'N/A')}")
        print(f"Project: {outputs.get('ProjectName', 'N/A')}")
        print(f"Analysis: {params['line_item']}")
        print("-" * 80)
        
        # Display results
        results = outputs.get("Results", [])
        if results:
            print("💰 FINANCIAL PROJECTIONS:")
            
            if isinstance(results[0], dict):
                # Display as table
                df = pd.DataFrame(results)
                print(df.to_string(index=False))
                
                # Display key insights
                if len(df.columns) > 1:
                    print(f"\n🔍 KEY INSIGHTS:")
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    
                    for col in numeric_cols:
                        values = df[col].dropna()
                        if len(values) > 1:
                            trend = "📈 Growing" if values.iloc[-1] > values.iloc[0] else "📉 Declining"
                            change = ((values.iloc[-1] - values.iloc[0]) / values.iloc[0]) * 100
                            print(f"  {col}: {trend} ({change:+.1f}% over period)")
            else:
                # Display as list
                for i, result in enumerate(results, 1):
                    print(f"  Result {i}: {result}")
        
        # Display balance sheet items if available
        balance_sheet = outputs.get("BalanceSheet_lineitems", [])
        if balance_sheet:
            print(f"\n🏦 BALANCE SHEET ITEMS:")
            if isinstance(balance_sheet[0], dict):
                bs_df = pd.DataFrame(balance_sheet)
                print(bs_df.to_string(index=False))
            else:
                for item in balance_sheet:
                    print(f"  • {item}")
        
        print("\n" + "=" * 80)
        print("✅ Analysis completed successfully!")
        print("=" * 80)
    
    def run_interactive_session(self):
        """Run the main interactive session."""
        self.display_welcome()
        
        while True:
            try:
                # Collect parameters
                params = self.collect_input_parameters()
                
                # Execute API call
                response = self.execute_model_api(params)
                
                # Display results
                self.format_and_display_results(response, params)
                
                # Ask if user wants to run another analysis
                continue_analysis = self.get_user_choice(
                    "\nRun another analysis?", 
                    ["yes", "no"], 
                    "no"
                )
                
                if continue_analysis == "no":
                    break
                    
                print("\n" + "🔄" * 40)
            
            except KeyboardInterrupt:
                print("\n\n👋 Session cancelled by user. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Unexpected error: {str(e)}")
                continue_analysis = self.get_user_choice(
                    "Try again?", 
                    ["yes", "no"], 
                    "yes"
                )
                if continue_analysis == "no":
                    break

def main():
    """Main entry point for the interactive UI."""
    ui = InteractiveFinancialPlanningUI()
    ui.run_interactive_session()

if __name__ == "__main__":
    main()