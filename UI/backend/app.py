#!/usr/bin/env python3
"""
Flask Backend for Financial Planning Model React UI
Bridges the React frontend with the existing Python API client.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
import logging
from datetime import datetime

# Add the parent directory to the path to import our existing modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from demo_financial_ui import DemoFinancialPlanningUI

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the financial planning client
financial_client = DemoFinancialPlanningUI()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'Financial Planning Model API'
    })

@app.route('/api/financial-model', methods=['POST'])
def run_financial_model():
    """
    Run the financial model with provided parameters.
    Accepts React frontend parameters and returns formatted results.
    """
    try:
        # Get parameters from request
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        logger.info(f"Received financial model request: {data.get('callPurpose', 'Unknown purpose')}")
        
        # Extract parameters with defaults
        params = {
            'capex': data.get('capex', 8000),
            'ga_personnel_rates': data.get('gaPersonnelRates', [0.0356, 0.0338, 0.0321, 0.0289, 0.0284]),
            'ga_non_personnel_rates': data.get('gaNonPersonnelRates', [0.0413, 0.041, 0.0390, 0.0370, 0.0352]),
            'rd_personnel_rates': data.get('rdPersonnelRates', [0.0929, 0.091, 0.089, 0.088, 0.088]),
            'rd_non_personnel_rates': data.get('rdNonPersonnelRates', [0.0312, 0.031, 0.029, 0.029, 0.029]),
            'global_saas_cogs': data.get('globalSaasCogs', 0.843),
            'interest_income': data.get('interestIncome', 0.01),
            'line_item': data.get('lineItem', 'Income Statement : GAAP Net Income : GAAP Net Income')
        }
        
        # Set call purpose for tracking
        scenario_name = data.get('callPurpose', 'React UI Analysis')
        
        # Execute the model
        response = financial_client.execute_model_api(params, scenario_name)
        
        # Check for API errors
        if "error" in response and response["error"] is not None and response["error"] != "":
            logger.error(f"API Error: {response['error']}")
            return jsonify({'error': response['error']}), 500
        
        if response.get("status") == "error":
            error_msg = response.get("error", "Unknown API error")
            logger.error(f"API Status Error: {error_msg}")
            return jsonify({'error': error_msg}), 500
        
        # Validate response structure
        if "response_data" not in response or "outputs" not in response["response_data"]:
            logger.error("Invalid response format from API")
            return jsonify({'error': 'Invalid response format from financial model API'}), 500
        
        # Extract and format results
        outputs = response["response_data"]["outputs"]
        results = outputs.get("Results", [])
        balance_sheet = outputs.get("BalanceSheet_lineitems", [])
        
        # Format the response for React frontend
        formatted_response = {
            'clientName': outputs.get('ClientName', 'N/A'),
            'modelName': outputs.get('ModelName', 'N/A'),
            'projectName': outputs.get('ProjectName', 'N/A'),
            'results': results,
            'balanceSheetItems': balance_sheet,
            'metadata': {
                'lineItem': params['line_item'],
                'callPurpose': scenario_name,
                'timestamp': datetime.now().isoformat(),
                'parameters': params
            }
        }
        
        logger.info(f"Successfully processed financial model for: {scenario_name}")
        return jsonify(formatted_response)
        
    except Exception as e:
        logger.error(f"Unexpected error in financial model API: {str(e)}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/api/scenarios/predefined', methods=['GET'])
def get_predefined_scenarios():
    """Get list of predefined scenarios."""
    try:
        scenarios = financial_client.get_demo_scenarios()
        
        # Format scenarios for frontend
        formatted_scenarios = []
        for scenario in scenarios:
            formatted_scenarios.append({
                'id': scenario['name'].lower().replace(' ', '_'),
                'name': scenario['name'],
                'description': scenario['description'],
                'parameters': scenario['params']
            })
        
        return jsonify({'scenarios': formatted_scenarios})
        
    except Exception as e:
        logger.error(f"Error fetching predefined scenarios: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/scenarios/run-demo', methods=['POST'])
def run_demo_scenario():
    """Run a specific predefined demo scenario."""
    try:
        data = request.get_json()
        scenario_name = data.get('scenarioName')
        
        if not scenario_name:
            return jsonify({'error': 'Scenario name is required'}), 400
        
        scenarios = financial_client.get_demo_scenarios()
        scenario = next((s for s in scenarios if s['name'] == scenario_name), None)
        
        if not scenario:
            return jsonify({'error': f'Scenario "{scenario_name}" not found'}), 404
        
        # Execute the scenario
        response = financial_client.execute_model_api(scenario['params'], scenario['name'])
        
        # Format response similar to main endpoint
        if "error" in response and response["error"] is not None:
            return jsonify({'error': response['error']}), 500
        
        outputs = response["response_data"]["outputs"]
        
        formatted_response = {
            'scenarioName': scenario['name'],
            'scenarioDescription': scenario['description'],
            'clientName': outputs.get('ClientName', 'N/A'),
            'modelName': outputs.get('ModelName', 'N/A'),
            'projectName': outputs.get('ProjectName', 'N/A'),
            'results': outputs.get("Results", []),
            'balanceSheetItems': outputs.get("BalanceSheet_lineitems", []),
            'metadata': {
                'lineItem': scenario['params']['line_item'],
                'callPurpose': scenario['name'],
                'timestamp': datetime.now().isoformat(),
                'parameters': scenario['params']
            }
        }
        
        return jsonify(formatted_response)
        
    except Exception as e:
        logger.error(f"Error running demo scenario: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/test-connectivity', methods=['GET'])
def test_api_connectivity():
    """Test the underlying API connectivity."""
    try:
        # Use a simple test scenario
        test_params = {
            'capex': 1000,
            'ga_personnel_rates': [0.03, 0.03, 0.03, 0.03, 0.03],
            'ga_non_personnel_rates': [0.04, 0.04, 0.04, 0.04, 0.04],
            'rd_personnel_rates': [0.08, 0.08, 0.08, 0.08, 0.08],
            'rd_non_personnel_rates': [0.03, 0.03, 0.03, 0.03, 0.03],
            'global_saas_cogs': 0.8,
            'interest_income': 0.01,
            'line_item': 'Income Statement : GAAP Net Income : GAAP Net Income'
        }
        
        response = financial_client.execute_model_api(test_params, "Connectivity Test")
        
        if "error" in response:
            return jsonify({
                'status': 'error',
                'message': response['error']
            }), 500
        
        return jsonify({
            'status': 'success',
            'message': 'API connectivity test successful',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Connectivity test failed: {str(e)}'
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("🚀 Starting Financial Planning Model Backend Server...")
    print("📊 API Endpoints:")
    print("   GET  /api/health - Health check")
    print("   POST /api/financial-model - Run financial model")
    print("   GET  /api/scenarios/predefined - Get predefined scenarios")
    print("   POST /api/scenarios/run-demo - Run demo scenario")
    print("   GET  /api/test-connectivity - Test API connectivity")
    print("\n🌐 Server will be available at: http://localhost:5001")
    print("🔧 React frontend should proxy requests to this server")
    print("-" * 60)
    
    app.run(debug=True, port=5001, host='0.0.0.0')