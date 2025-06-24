# Financial Planning Model UI

This directory contains Python UI tools for interacting with the Meteor Long-range Financial Planning Model API.

## Available Tools

### 1. `Anthropic-UI.py` - Original API Client
- Object-oriented client class (`FinancialPlanningModelClient`)
- Direct API access with helper methods
- Basic example usage at the bottom

### 2. `interactive_financial_ui.py` - Interactive UI
- Full interactive interface for parameter input
- User-friendly prompts and validation
- Formatted output with insights
- **Note**: Requires terminal input - may not work in all environments

### 3. `demo_financial_ui.py` - Demo Scenarios
- Predefined scenarios showcase API capabilities
- Three scenarios: Conservative, Aggressive, Balanced
- Formatted output with financial projections
- **Recommended for testing and demonstration**

### 4. `diagnostic_api.py` - API Diagnostic Tool
- Tests API connectivity and authentication
- Helps troubleshoot connection issues
- Validates payload format and response handling

## Quick Start

### Run Demo Scenarios (Recommended)
```bash
python3 demo_financial_ui.py
```

### Test API Connectivity
```bash
python3 diagnostic_api.py
```

### Use Original Client
```bash
python3 Anthropic-UI.py
```

## Features Demonstrated

### Financial Scenarios
- **Conservative Growth**: Low-risk, modest projections
- **Aggressive Expansion**: High-growth with increased investment
- **Balanced Portfolio**: Moderate risk/return balance

### Output Features
- Multi-year financial projections (2022-2028)
- Key parameter summaries
- Balance sheet line items (232+ items)
- Formatted numerical displays
- Success/failure reporting

### API Integration
- Coherent Financial Planning Model connectivity
- Authentication via API keys
- Comprehensive payload construction
- Error handling and diagnostics

## Configuration

The tools use environment variables for API authentication:
- `SYNTHETIC_KEY`: API key (falls back to hardcoded default)
- Set in `.env` file or environment

## Requirements

```bash
pip install requests pandas python-dotenv
```

## Output Examples

### Financial Projections
```
💰 FINANCIAL PROJECTIONS:
    2022     2023     2024     2025     2026    2027     2028
$-17,137 $-16,997 $-16,656 $-22,448 $-15,104 $-7,718 $110,959
```

### Key Parameters
```
🔧 KEY PARAMETERS:
  CAPEX: $5,000
  Global SaaS COGS: 80.0%
  Interest Income: 1.5%
  GA Personnel Y1: 3.00%
  R&D Personnel Y1: 8.00%
```

### Success Summary
```
📋 DEMO SUMMARY
Total scenarios run: 3
Successful executions: 3
Success rate: 100.0%
🎉 All scenarios completed successfully!
```