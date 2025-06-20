# API Tool using FastMCP
# This script provides a FastMCP server that allows users to upload any API call, with argument payload, and get the results
import sys
from typing import Any
import httpx
from anthropic import Anthropic
from mcp.server.fastmcp import FastMCP
import requests
import json

# Initialize FastMCP server
mcp = FastMCP("CashflowModel", description="API Testing Tool using FastMCP", version="1.0.0")

# Constants
url = "https://excel.uat.us.coherent.global/presales/api/v3/folders/Luna - Private Equity/services/Meteor - Long-range financial planning model/execute"
query_value = "[\"ClientName\",\"ModelName\",\"ProjectName\",\"Results\",\"BalanceSheet_lineitems\"]"

# Payload for the API request
# This payload is structured to match the expected input for the CashflowModel service.
payload = json.dumps({
    "request_data": {
        "inputs": {
            "Capex": 8000,
            "existing_leases": [
                {
                    "Existing leases": "Aus. 22fl",
                    "Lease expiry date": "2025-06-30",
                    "Remaining useful life(years)": 1.5,
                    "Lease renewable": "No",
                    "Average new lease life(years)": 3.24722222222222,
                    "% of Total lease liabilties": 0,
                    "Borrowing Rate pa": 0.0804
                },
                {
                    "Existing leases": "Axis",
                    "Lease expiry date": "2023-06-30",
                    "Remaining useful life(years)": 0.5,
                    "Lease renewable": "No",
                    "Average new lease life(years)": 3.24722222222222,
                    "% of Total lease liabilties": 0,
                    "Borrowing Rate pa": 0.0804
                },
                {
                    "Existing leases": "Brazil",
                    "Lease expiry date": "2024-10-31",
                    "Remaining useful life(years)": 0.833333333333333,
                    "Lease renewable": "Yes",
                    "Average new lease life(years)": 4.58333333333333,
                    "% of Total lease liabilties": 0,
                    "Borrowing Rate pa": 0.0812
                },
                {
                    "Existing leases": "HQ 3fl",
                    "Lease expiry date": "2027-10-31",
                    "Remaining useful life(years)": 3.83333333333333,
                    "Lease renewable": "Yes",
                    "Average new lease life(years)": 7.58333333333333,
                    "% of Total lease liabilties": 0.100109950443412,
                    "Borrowing Rate pa": 0.083
                },
                {
                    "Existing leases": "HQ 34fl",
                    "Lease expiry date": "2027-10-31",
                    "Remaining useful life(years)": 3.83333333333333,
                    "Lease renewable": "Yes",
                    "Average new lease life(years)": 7.58333333333333,
                    "% of Total lease liabilties": 0.096114440649257,
                    "Borrowing Rate pa": 0.083
                },
                {
                    "Existing leases": "HQ 7fl",
                    "Lease expiry date": "2025-02-28",
                    "Remaining useful life(years)": 1.16111111111111,
                    "Lease renewable": "Yes",
                    "Average new lease life(years)": 4.90833333333333,
                    "% of Total lease liabilties": 0.301845993543046,
                    "Borrowing Rate pa": 0.0812
                },
                {
                    "Existing leases": "PG",
                    "Lease expiry date": "2028-12-31",
                    "Remaining useful life(years)": 5,
                    "Lease renewable": "Yes",
                    "Average new lease life(years)": 8.75,
                    "% of Total lease liabilties": 0.256056259508767,
                    "Borrowing Rate pa": 0.08375
                },
                {
                    "Existing leases": "San Diego",
                    "Lease expiry date": "2025-02-28",
                    "Remaining useful life(years)": 1.16111111111111,
                    "Lease renewable": "Yes",
                    "Average new lease life(years)": 4.90833333333333,
                    "% of Total lease liabilties": 0.023200121771694,
                    "Borrowing Rate pa": 0.0812
                },
                {
                    "Existing leases": "Seattle Org. ",
                    "Lease expiry date": "2028-12-31",
                    "Remaining useful life(years)": 5,
                    "Lease renewable": "Yes",
                    "Average new lease life(years)": 8.75,
                    "% of Total lease liabilties": 0.067934832786294,
                    "Borrowing Rate pa": 0.08375
                },
                {
                    "Existing leases": "Seatle Adt Sp.",
                    "Lease expiry date": "2028-12-31",
                    "Remaining useful life(years)": 5,
                    "Lease renewable": "Yes",
                    "Average new lease life(years)": 8.75,
                    "% of Total lease liabilties": 0.021581900477245,
                    "Borrowing Rate pa": 0.08375
                },
                {
                    "Existing leases": "Hungary",
                    "Lease expiry date": "2027-02-14",
                    "Remaining useful life(years)": 3.12222222222222,
                    "Lease renewable": "Yes",
                    "Average new lease life(years)": 6.70277777777778,
                    "% of Total lease liabilties": 0.114694577756354,
                    "Borrowing Rate pa": 0.07896
                },
                {
                    "Existing leases": "Wakefield",
                    "Lease expiry date": "2024-03-31",
                    "Remaining useful life(years)": 0.25,
                    "Lease renewable": "Yes",
                    "Average new lease life(years)": 3.25,
                    "% of Total lease liabilties": 0.002499247722022,
                    "Borrowing Rate pa": 0.0766
                },
                {
                    "Existing leases": "Raleigh",
                    "Lease expiry date": "2024-08-31",
                    "Remaining useful life(years)": 0.666666666666667,
                    "Lease renewable": "Yes",
                    "Average new lease life(years)": 1.66666666666667,
                    "% of Total lease liabilties": 0.007181810873309,
                    "Borrowing Rate pa": 0.0790229
                },
                {
                    "Existing leases": "Greenleaf",
                    "Lease expiry date": "2026-06-30",
                    "Remaining useful life(years)": 2.5,
                    "Lease renewable": "Yes",
                    "Average new lease life(years)": 2.99722222222222,
                    "% of Total lease liabilties": 0.0087808644686,
                    "Borrowing Rate pa": 0.0785
                }
            ],
            "ExistingPPEUsefulLife": 15,
            "GA_non_personnel_expenses": [
                {
                    "Y1": 0.041299977693274,
                    "Y2": 0.041,
                    "Y3": 0.03895,
                    "Y4": 0.0370025,
                    "Y5": 0.035152375
                }
            ],
            "GA_personnel_expenses": [
                {
                    "Y1": 0.035617778642206,
                    "Y2": 0.033836889710096,
                    "Y3": 0.032145045224591,
                    "Y4": 0.028930540702132,
                    "Y5": 0.028351929888089
                }
            ],
            "GlobalSaaSCOGS": 0.843,
            "GRR": [
                {
                    "Y1": 1,
                    "Y2": 0.999,
                    "Y3": 0.999,
                    "Y4": 0.999,
                    "Y5": 0.999
                },
                {
                    "Y1": 0.91,
                    "Y2": 0.925,
                    "Y3": 0.937,
                    "Y4": 0.945,
                    "Y5": 0.95
                }
            ],
            "InterestIncome": 0.01,
            "LineItem": "Income Statement : GAAP Net Income : GAAP Net Income",
            "LongTermDebtBorrowingCosts": [
                {
                    "Y1": 0.03,
                    "Y2": 0.03,
                    "Y3": 0.03,
                    "Y4": 0.03,
                    "Y5": 0.03
                },
                {
                    "Y1": 0.06,
                    "Y2": 0.06,
                    "Y3": 0.06,
                    "Y4": 0.06,
                    "Y5": 0.06
                },
                {
                    "Y1": 0.005,
                    "Y2": 0.005,
                    "Y3": 0.005,
                    "Y4": 0.005,
                    "Y5": 0.005
                },
                {
                    "Y1": 0.005,
                    "Y2": 0.005,
                    "Y3": 0.005,
                    "Y4": 0.005,
                    "Y5": 0.005
                }
            ],
            "NewPPEUsefulLife": 15,
            "RD_non_personnel_expenses": [
                {
                    "Y1": 0.031234601083995,
                    "Y2": 0.031,
                    "Y3": 0.029,
                    "Y4": 0.029,
                    "Y5": 0.029
                }
            ],
            "RD_personnel_expenses": [
                {
                    "Y1": 0.092919233098158,
                    "Y2": 0.091,
                    "Y3": 0.089,
                    "Y4": 0.088,
                    "Y5": 0.088
                }
            ]
        }
    },
    "request_meta": {
        "version_id": "8907652e-e708-409e-971e-d0223db696a4",
        "transaction_date": None,
        "call_purpose": "Spark - MCP Claude API Tester",
        "source_system": "Anthropic Claude",
        "correlation_id": None,
        "service_category": "ALL",
        "requested_output": query_value
    }
})
headers = {
   'Content-Type': 'application/json',
   'x-tenant-name': 'presales',
   'x-synthetic-key': '46ac56eb-90ea-4570-80c3-4750ffae5874'
}

# Function to make a synchronous request to the API endpoint
def call_url():
    """
    Function to call the API endpoint with the specified payload and headers.
    This is a placeholder for direct API calls.
    """
    response = requests.post(url, headers=headers, data=payload)
    print(response.text)
    print('+++URL RESPONSE', response.json(), file=sys.stderr)
    return response.json()

async def call_url_func():
    data = await make_url_request(url)  # Call the API to test it asynchronously
    print('+++DATA', data, file=sys.stderr)

async def make_url_request(url: str) -> Any:
    """
    Asynchronous function to make a request to the specified URL.
    Returns the JSON response or text.
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                url=url,
                headers=headers,
                data=payload,
                timeout=60.0
            )
            response.raise_for_status()  # Raise an error for bad responses
            return response.json()
        
        except Exception as e:
            return {"error": str(e)}    

@mcp.tool()
async def call_api(
    endpoint: str = url,
    method: str = "POST",
    params: dict = None,
    data: dict = payload,
    headers: dict = headers
) -> dict:
    """
    Calls an arbitrary API endpoint with the specified method and arguments.
    Returns the JSON response or text.
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                url=endpoint,
                params=params,
                json=data,
                headers=headers,
                timeout=60.0
            )
            response.raise_for_status()  # Raise an error for bad responses
            return response.json()
        
        except Exception as e:
            return {"error": str(e)}
            
if __name__ == "__main__":
    import asyncio
    # Initialize and run the server
    # This will start the FastMCP server and listen for incoming requests.
    mcp.run(transport='stdio')

 
    #print('API',url,'\n','Headers',headers,'\n','Payload',payload, file=sys.stderr)
    # Test the non-server function call
    #asyncio.run(call_url_func())  # type: ignore # Call the API to test it asynchronously
    #call_url()  # Call the API to test it synchronously
    