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
mcp = FastMCP("api-test", description="API Testing Tool using FastMCP", version="1.0.0")

# Constants
url = "https://excel.uat.us.coherent.global/presales/api/v3/folders/Solder-Test/services/mortgage-amort-calculator/execute"
query_value = "[\"MonthlyPmt\",\"ScheduledNoPayments\",\"ActualNoPmts\",\"YrsSavedOffOrigLoanTerm\",\"TotEarlyPmts\",\"TotalIntPaid\"]"

# Payload for the API request
# This payload is structured to match the expected input for the mortgage amortization calculator service.
payload = json.dumps({
   "request_data": {
      "inputs": {
         "ExtraPrincPmt": 100,
         "InterestRate": 0.05,
         "Lender": "Wells Fargo",
         "LoanStartDate": "2025-05-28",
         "LoanTermYrs": 30,
         "OrigLoanAmt": 200000,
         "PaymentsPerYear": 12
      }
   },
   "request_meta": {
      "version_id": "aeffe1e2-529b-4c2f-9755-5473a391aa83",
      "transaction_date": None,
      "call_purpose": None,
      "source_system": None,
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


#response = requests.request("POST", url, headers=headers, data=payload, allow_redirects=False)

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
    