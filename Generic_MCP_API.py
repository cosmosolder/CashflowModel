# API Tool using FastMCP
# This script provides a FastMCP server that allows users to upload any API call, with argument payload, and get the results
import sys
from typing import Any
import httpx
from anthropic import Anthropic
from mcp.server.fastmcp import FastMCP
import requests
import json
from dotenv import load_dotenv
import os

# Initialize FastMCP server
mcp = FastMCP("GenericMCPApi", description="Generic API Testing Tool using FastMCP", version="1.0.0")
global payload
payload = {}  # Placeholder for the payload, to be loaded from the API JSON file

load_dotenv()  # Loads variables from .env into environment.  Acts wierd if running in Claude due to "uv" not inhereting environment variables from parent process
def check_env_variables():
    """
    Check if the required environment variables are set.
    Raises an error if any variable is missing.
    """
    required_vars = ["SYNTHETIC_KEY", "CLAUDE_FLAG", "API_URL", "API_JSON"]
    for var in required_vars:
        if not os.getenv(var):
            raise ValueError(f"Environment variable {var} is not set.")

check_env_variables()  # Check if all required environment variables are set
synthetic_key = os.getenv("SYNTHETIC_KEY") # value for synthetic key, set in environment variable
CLAUDE_FLAG = os.getenv("CLAUDE_FLAG", "False").lower() == "true" #flag to indicate if Claude is enabled
API_URL = os.getenv("API_URL","") # API endpoint URL

headers = {
    'Content-Type': 'application/json',
    'x-tenant-name': 'presales',
    'x-synthetic-key': synthetic_key
}

# Function to make a synchronous request to the API endpoint
def call_url():
    """
    Function to call the API endpoint with the specified payload and headers.
    This is a placeholder for direct API calls.
    """
    response = requests.post(url=API_URL, headers=headers, data=payload,json={'key': 'value'})  # Replace with actual payload if needed
    return response.json()

def load_api_json():
    """
    Load the API JSON from the specified file.
    Returns the JSON data as a dictionary.
    """
    global api_json_results_file
    api_json_file = os.getenv("API_JSON")
    if not api_json_file:
        raise ValueError("API_JSON environment variable is not set.")
    
    api_json_results_file = api_json_file.replace('.json', '_results.json')  # output results to json file
    
    with open(api_json_file, 'r') as file:
        return json.load(file)
        

async def call_url_func():
    data = await make_url_request(API_URL)  # Call the API to test it asynchronously
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

# Register the API call function as a tool in FastMCP
# This function can be called from the MCP server or directly
#--------------------------------------------------------------
@mcp.tool()
async def call_api(
    endpoint: str = API_URL,
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
 
    payload = load_api_json()  # Load the API JSON input from the specified file 

    if CLAUDE_FLAG: mcp.run(transport='stdio')
    else:

        # Test the non-server function call
        #asyncio.run(call_url_func())  # type: ignore # Call the API to test it asynchronously

        response = call_url()  # Call the API to test it synchronously

        pretty_json = json.dumps(response, indent=4, sort_keys=True)  # Format the JSON response
    
        # print(pretty_json, file=sys.stderr)  # Print to stderr for visibility

        # Write the JSON response to the output file
        with open(api_json_results_file, 'w') as f:
            f.write(pretty_json)
