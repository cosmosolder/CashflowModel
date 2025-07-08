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
url = "https://excel.uat.us.coherent.global/presales/api/v3/folders/ALLVUE/services/FundManagerA_Deal123/execute"
query_value = "[\"ActualAdvanceRate\",\"AvailabilityLESSAdvancesOutstanding\",\"AvailableCapital\",\"AvailabletoBorrow\",\"ExpressionApprovedForeignCurrencyReserve\",\"ExpressionBorrowingBase\",\"ExpressionUnhedgedForeignCurrency\",\"FacilityUtilization\",\"PortfolioDataAggregateHaircut\",\"PortfolioDataAssetOutstandingRC\",\"PortfolioDataDefaultBasisAmountRC\",\"PortfolioDataForeignCurrencyACV\",\"PortfolioDataLiabilityOutstandingRC\",\"PortfolioDataMinimumEquityAmount\",\"PortfolioDataPortfolioWeightedAverageAdvanceRAte\",\"PortfolioDataRevolverFundingAccount\",\"PortfolioDataUnfundedExposureAmount\",\"PortfolioDataUnfundedExposureEquityAmount\",\"TestMaximumAdvanceRateTest\",\"TestMinimumCreditEnhancementTest\",\"OBLIGOR_OUTSTANDINGS\",\"EXCESS_CONCENTRATION_AMOUNT\",\"Portfolio\"]"

# Payload for the API request
# This payload is structured to match the expected input for the CashflowModel service.
payload = json.dumps({
    "request_data": {
        "inputs": {
            "AddlTests_i_UnrestrictedCash": 28881265.91,
            "AddlTests_ii_DrawAmt": 33400664.121186,
            "AddlTests_iii_CapitalCommittments": 227750550,
            "AddlTests_iv_UnencumberedAssets": 33755698.78,
            "AdvanceDate": None,
            "AdvancesRepaid": 0,
            "AdvancesRequested": 0,
            "Borrower": "Deal 123 Partners LLC",
            "CurrentAdvancesOutstanding": 132802183.31,
            "DetminationDate": "2023-09-30",
            "EffectiveDate": "2023-01-11",
            "MeasurementDate": "2023-09-30",
            "PaymentDate": "2023-10-20",
            "PortfolioDataFacilityAmount": 250000000,
            "PortfolioDataHedgedandAssignedtoAdmin": 0,
            "PortfolioDataHedgedandAssignedtoBorrower": 0,
            "PortfolioDataHedgedbyBorrower": 0,
            "PortfolioDataPrincipalCollectionAccount": 1848801.32,
            "ReportingDate": "2023-10-20",
            "SchedRevPerEndDate": "2026-01-11",
            "TerminationDate": "2028-01-11",
            "VAE_RecurringRevenue": [
                {
                    "Borrower": "Company A",
                    "Event Type": "(a) Credit Quality Deterioration Event",
                    "Effective Date": "2023-04-28",
                    "Date of TTM Financials": "2022-12-31",
                    "TTM EBITDA": 17157376.6674577,
                    "Liquidity": 18621844.87,
                    "Recurring Revenue": None
                },
                {
                    "Borrower": "Company AC",
                    "Event Type": "(d) Material Modification",
                    "Effective Date": "2023-05-15",
                    "Date of TTM Financials": None,
                    "TTM EBITDA": None,
                    "Liquidity": None,
                    "Recurring Revenue": None
                },
                {
                    "Borrower": "Company C",
                    "Event Type": "(a) Credit Quality Deterioration Event",
                    "Effective Date": "2023-05-26",
                    "Date of TTM Financials": "2023-03-31",
                    "TTM EBITDA": 12928111,
                    "Liquidity": None,
                    "Recurring Revenue": None
                },
                {
                    "Borrower": "Company AE",
                    "Event Type": "(a) Credit Quality Deterioration Event",
                    "Effective Date": "2023-05-23",
                    "Date of TTM Financials": "2023-03-31",
                    "TTM EBITDA": 8298747.63,
                    "Liquidity": None,
                    "Recurring Revenue": None
                },
                {
                    "Borrower": "Company N",
                    "Event Type": "(b) Payment Default",
                    "Effective Date": "2023-01-31",
                    "Date of TTM Financials": None,
                    "TTM EBITDA": None,
                    "Liquidity": None,
                    "Recurring Revenue": None
                }
            ]
        }
    },
    "request_meta": {
        "version_id": None,
        "transaction_date": None,
        "call_purpose": "Spark - AllVue API API Tester",
        "source_system": "AllVue",
        "correlation_id": None,
        "service_category": "ALL",
        "requested_output": query_value
    }
})
#TODO: set synthetic key in env variable
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
    #mcp.run(transport='stdio')

 
    #print('API',url,'\n','Headers',headers,'\n','Payload',payload, file=sys.stderr)
    # Test the non-server function call
    #asyncio.run(call_url_func())  # type: ignore # Call the API to test it asynchronously
    call_url()  # Call the API to test it synchronously
    