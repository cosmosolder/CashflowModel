import requests
import json
from typing import Dict, List, Optional, Union
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()  # Loads variables from .env into environment

env_synthetic_key = os.getenv("SYNTHETIC_KEY")
CLAUDE_FLAG = os.getenv("CLAUDE_FLAG", "False").lower() == "true"

class FinancialPlanningModelClient:
    """
    Client for interacting with the Meteor Long-range Financial Planning Model API.
    
    This client provides methods to execute financial models and retrieve projections
    for private equity and long-range financial planning scenarios.
    """
    
    def __init__(self, base_url: str = None, synthetic_key: str = None, tenant_name: str = None):
        """
        Initialize the Financial Planning Model client.
        
        Args:
            base_url: Base URL for the API (optional, uses default if not provided)
            synthetic_key: API key for authentication (optional, uses default if not provided)
            tenant_name: Tenant name for the API (optional, uses default if not provided)
        """
        self.base_url = base_url or "https://excel.uat.us.coherent.global/presales/api/v3"
        self.synthetic_key = synthetic_key or env_synthetic_key
        self.tenant_name = tenant_name or "presales"
        
        self.headers = {
            "Content-Type": "application/json",
            "x-synthetic-key": self.synthetic_key,
            "x-tenant-name": self.tenant_name
        }
        
        
        self.endpoint = f"{self.base_url}/folders/Luna - Private Equity/services/Meteor - Long-range financial planning model/execute"
    
    def create_lease_entry(self, 
                          lease_name: str,
                          expiry_date: str,
                          remaining_life: float,
                          renewable: bool = True,
                          avg_new_lease_life: float = 5.0,
                          lease_liability_pct: float = 0.0,
                          borrowing_rate: float = 0.08) -> Dict:
        """
        Create a standardized lease entry for the model.
        
        Args:
            lease_name: Name of the lease
            expiry_date: Lease expiry date (YYYY-MM-DD format)
            remaining_life: Remaining useful life in years
            renewable: Whether the lease is renewable
            avg_new_lease_life: Average new lease life in years
            lease_liability_pct: Percentage of total lease liabilities
            borrowing_rate: Borrowing rate per annum
            
        Returns:
            Dict: Formatted lease entry for the API
        """
        return {
            "Existing leases": lease_name,
            "Lease expiry date": expiry_date,
            "Remaining useful life(years)": remaining_life,
            "Lease renewable": "Yes" if renewable else "No",
            "Average new lease life(years)": avg_new_lease_life,
            "% of Total lease liabilties": lease_liability_pct,
            "Borrowing Rate pa": borrowing_rate
        }
    
    def create_yearly_rates(self, rates: List[float]) -> List[Dict]:
        """
        Create yearly rate structure for the model.
        
        Args:
            rates: List of rates for Y1, Y2, Y3, Y4, Y5
            
        Returns:
            List[Dict]: Formatted yearly rates
        """
        years = ["Y1", "Y2", "Y3", "Y4", "Y5"]
        return [{year: rate} for year, rate in zip(years, rates)]
    
    def execute_model(self,
                     capex: float = 8000,
                     existing_leases: List[Dict] = None,
                     existing_ppe_life: int = 15,
                     new_ppe_life: int = 15,
                     ga_personnel_rates: List[float] = None,
                     ga_non_personnel_rates: List[float] = None,
                     rd_personnel_rates: List[float] = None,
                     rd_non_personnel_rates: List[float] = None,
                     global_saas_cogs: float = 0.843,
                     grr_rates: List[List[float]] = None,
                     interest_income: float = 0.01,
                     debt_borrowing_costs: List[List[float]] = None,
                     line_item: str = "Income Statement : GAAP Net Income : GAAP Net Income",
                     call_purpose: str = "Python API Client",
                     correlation_id: str = None) -> Dict:
        """
        Execute the financial planning model with specified parameters.
        
        Args:
            capex: Capital expenditure amount
            existing_leases: List of existing lease dictionaries
            existing_ppe_life: Existing PPE useful life in years
            new_ppe_life: New PPE useful life in years
            ga_personnel_rates: GA personnel expense rates for Y1-Y5
            ga_non_personnel_rates: GA non-personnel expense rates for Y1-Y5
            rd_personnel_rates: R&D personnel expense rates for Y1-Y5
            rd_non_personnel_rates: R&D non-personnel expense rates for Y1-Y5
            global_saas_cogs: Global SaaS COGS rate
            grr_rates: Gross retention rates (list of lists)
            interest_income: Interest income rate
            debt_borrowing_costs: Long-term debt borrowing costs (list of lists)
            line_item: Specific line item to analyze
            call_purpose: Purpose of the API call
            correlation_id: Optional correlation ID for tracking
            
        Returns:
            Dict: API response containing financial projections
        """
        
        # Default values
        if existing_leases is None:
            existing_leases = [
                self.create_lease_entry("HQ Main", "2027-10-31", 3.83, True, 7.58, 0.10, 0.083),
                self.create_lease_entry("Branch Office", "2025-06-30", 1.5, False, 3.25, 0.05, 0.0804)
            ]
        
        if ga_personnel_rates is None:
            ga_personnel_rates = [0.0356, 0.0338, 0.0321, 0.0289, 0.0284]
        
        if ga_non_personnel_rates is None:
            ga_non_personnel_rates = [0.0413, 0.041, 0.0390, 0.0370, 0.0352]
        
        if rd_personnel_rates is None:
            rd_personnel_rates = [0.0929, 0.091, 0.089, 0.088, 0.088]
        
        if rd_non_personnel_rates is None:
            rd_non_personnel_rates = [0.0312, 0.031, 0.029, 0.029, 0.029]
        
        if grr_rates is None:
            grr_rates = [
                [1.0, 0.999, 0.999, 0.999, 0.999],
                [0.91, 0.925, 0.937, 0.945, 0.95]
            ]
        
        if debt_borrowing_costs is None:
            debt_borrowing_costs = [
                [0.03, 0.03, 0.03, 0.03, 0.03],
                [0.06, 0.06, 0.06, 0.06, 0.06],
                [0.005, 0.005, 0.005, 0.005, 0.005],
                [0.005, 0.005, 0.005, 0.005, 0.005]
            ]
        
        # Format rates into required structure
        years = ["Y1", "Y2", "Y3", "Y4", "Y5"]
        
        def format_rates(rates):
            return [{year: rate} for year, rate in zip(years, rates)]
        
        def format_multi_rates(rate_lists):
            return [format_rates(rates) for rates in rate_lists]
        
        payload = {
            "request_data": {
                "inputs": {
                    "Capex": capex,
                    "existing_leases": existing_leases,
                    "ExistingPPEUsefulLife": existing_ppe_life,
                    "NewPPEUsefulLife": new_ppe_life,
                    "GA_personnel_expenses": format_rates(ga_personnel_rates),
                    "GA_non_personnel_expenses": format_rates(ga_non_personnel_rates),
                    "RD_personnel_expenses": format_rates(rd_personnel_rates),
                    "RD_non_personnel_expenses": format_rates(rd_non_personnel_rates),
                    "GlobalSaaSCOGS": global_saas_cogs,
                    "GRR": format_multi_rates(grr_rates),
                    "InterestIncome": interest_income,
                    "LongTermDebtBorrowingCosts": format_multi_rates(debt_borrowing_costs),
                    "LineItem": line_item
                }
            },
            "request_meta": {
                "version_id": None,
                "transaction_date": None,
                "call_purpose": call_purpose,
                "source_system": "Python UI Client",
                "correlation_id": correlation_id,
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
        
        #print("DEBUG...")
        #print("Request URL:", self.endpoint)
        #print("Request Headers:", self.headers)
        #print("Request Payload:", json.dumps(payload, indent=2))    

        try:
            response = requests.post(
                self.endpoint,
                headers=self.headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            print(response.text)
            print('+++URL RESPONSE', response.json())
            return response.json()
            
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}
    
    def get_projections_dataframe(self, response: Dict) -> pd.DataFrame:
        """
        Convert API response to a pandas DataFrame for easier analysis.
        
        Args:
            response: API response dictionary
            
        Returns:
            pd.DataFrame: Financial projections as a DataFrame
        """
        if "response_data" in response and "outputs" in response["response_data"]:
            results = response["response_data"]["outputs"].get("Results", [])
            if results:
                df = pd.DataFrame(results)
                # Add metadata
                df.attrs['client_name'] = response["response_data"]["outputs"].get("ClientName")
                df.attrs['model_name'] = response["response_data"]["outputs"].get("ModelName")
                df.attrs['project_name'] = response["response_data"]["outputs"].get("ProjectName")
                return df
        return pd.DataFrame()
    
    def analyze_scenario(self, 
                        scenario_name: str,
                        **kwargs) -> Dict:
        """
        Run a named scenario analysis.
        
        Args:
            scenario_name: Name of the scenario
            **kwargs: Parameters to pass to execute_model
            
        Returns:
            Dict: Analysis results with scenario metadata
        """
        print(f"Running scenario: {scenario_name}")
        
        # Add scenario name to call purpose
        kwargs['call_purpose'] = f"Scenario Analysis: {scenario_name}"
        
        response = self.execute_model(**kwargs)
        
        if "error" not in response:
            results = response.get("response_data", {}).get("outputs", {}).get("Results", [])
            if results:
                df = self.get_projections_dataframe(response)
                print(f"Scenario '{scenario_name}' completed successfully")
                print(f"Projections: {df.iloc[0].to_dict()}")
                return {
                    "scenario_name": scenario_name,
                    "status": "success",
                    "projections": df,
                    "raw_response": response
                }
        
        return {
            "scenario_name": scenario_name,
            "status": "error",
            "error": response.get("error", "Unknown error"),
            "raw_response": response
        }


# Example usage and helper functions
def run_example_scenarios():
    """Run example scenarios to demonstrate the API client."""
    
    client = FinancialPlanningModelClient()
    
    # Scenario 1: Conservative growth
    conservative_scenario = client.analyze_scenario(
        "Conservative Growth",
        capex=5000,
        ga_personnel_rates=[0.030, 0.028, 0.026, 0.024, 0.022],
        rd_personnel_rates=[0.080, 0.075, 0.070, 0.065, 0.060]
    )
    
    # Scenario 2: Aggressive expansion
    aggressive_scenario = client.analyze_scenario(
        "Aggressive Expansion", 
        capex=15000,
        ga_personnel_rates=[0.045, 0.042, 0.040, 0.038, 0.036],
        rd_personnel_rates=[0.120, 0.115, 0.110, 0.105, 0.100]
    )
    
    # Scenario 3: Custom lease structure
    custom_leases = [
        client.create_lease_entry("Primary HQ", "2028-12-31", 5.0, True, 8.0, 0.15, 0.085),
        client.create_lease_entry("Secondary Office", "2026-06-30", 2.0, True, 4.0, 0.08, 0.082),
        client.create_lease_entry("Warehouse", "2025-03-31", 0.75, False, 2.0, 0.03, 0.079)
    ]
    
    lease_scenario = client.analyze_scenario(
        "Custom Lease Structure",
        existing_leases=custom_leases,
        capex=10000
    )
    
    return {
        "conservative": conservative_scenario,
        "aggressive": aggressive_scenario,
        "custom_leases": lease_scenario
    }


if __name__ == "__main__":
    # Initialize client
    client = FinancialPlanningModelClient()
    
    # Run a simple example
    print("Testing Financial Planning Model API...")
    
    response = client.execute_model(
        capex=8000,
        call_purpose="Python UI Client Test"
    )
    
    if "error" not in response:
        df = client.get_projections_dataframe(response)
        print("Success! Financial projections:")
        print(df)
    else:
        print(f"Error: {response['error']}")
    
    # Uncomment to run example scenarios
    # scenarios = run_example_scenarios()
    # print("All scenarios completed!")