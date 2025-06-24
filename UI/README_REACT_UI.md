# Financial Planning Model - React UI

A modern, responsive web interface for the Meteor Long-range Financial Planning Model built with React, TypeScript, and Material-UI.

## 🌟 Features

### ✨ Modern Web Interface
- **Professional Dashboard**: Clean, modern design with Material-UI components
- **Responsive Layout**: Works on desktop, tablet, and mobile devices
- **Tabbed Navigation**: Organized workflow with Parameters, Results, and Scenarios tabs

### 📊 Interactive Financial Modeling
- **Parameter Input Forms**: User-friendly forms with validation and real-time feedback
- **Predefined Scenarios**: Quick-start with Conservative, Aggressive, and Balanced scenarios
- **Custom Parameters**: Full control over all financial model inputs
- **Rate Projections**: 5-year expense rate planning with visual feedback

### 📈 Rich Data Visualization
- **Interactive Charts**: Professional line charts and bar charts using Chart.js
- **Trend Analysis**: Year-over-year growth rate charts with insights
- **Financial Metrics**: Key insights with trend analysis and percentage changes
- **Data Tables**: Detailed year-over-year financial projections
- **Progress Indicators**: Real-time loading states and status updates
- **Color-coded Visuals**: Green/red indicators for positive/negative performance

### 🎯 Scenario Management
- **Save Scenarios**: Store and organize multiple financial scenarios
- **Load & Compare**: Quick scenario switching and comparison tools
- **Export Functionality**: Download scenarios as JSON for backup/sharing
- **Predefined Templates**: Start with proven financial modeling scenarios

## 🏗️ Architecture

### Frontend (React + TypeScript)
```
financial-planning-ui/
├── src/
│   ├── components/
│   │   ├── ParameterInput.tsx     # Financial parameter input forms
│   │   ├── ResultsDisplay.tsx     # Charts, tables, and analysis
│   │   └── ScenarioManager.tsx    # Scenario save/load/compare
│   ├── types/
│   │   └── FinancialTypes.ts      # TypeScript type definitions
│   └── App.tsx                    # Main application component
└── package.json                   # Dependencies and scripts
```

### Backend (Flask + Python)
```
backend/
├── app.py                        # Flask API server
├── requirements.txt             # Python dependencies
└── [existing Python modules]   # Reuses demo_financial_ui.py
```

## 🚀 Quick Start

### Option 1: Automated Startup (Recommended)
```bash
# From the UI directory
./start_full_ui.sh
```

This script will:
- Install all dependencies automatically
- Start the Flask backend on port 5000
- Start the React frontend on port 3000
- Open your browser to the application

### Option 2: Manual Startup

#### Start Backend Server
```bash
cd backend
pip3 install -r requirements.txt
python3 app.py
```

#### Start Frontend Server
```bash
cd financial-planning-ui
npm install
npm start
```

### Access the Application
- **Frontend UI**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **API Health Check**: http://localhost:5000/api/health

## 📋 Usage Guide

### 1. Parameters Tab
- **Quick Start**: Select a predefined scenario (Conservative, Aggressive, Balanced)
- **Custom Analysis**: Modify parameters or start from scratch
- **Core Parameters**: Set CAPEX, PPE life, SaaS COGS rate, interest income
- **Rate Projections**: Configure 5-year expense rates for GA and R&D (both personnel and non-personnel)
- **Analysis Setup**: Choose line item and purpose for tracking

### 2. Results Tab
- **Key Metrics**: View average value, total change, min/max values with trend indicators
- **Visual Charts**: Interactive line chart showing financial projections over time
- **Data Tables**: Detailed year-over-year breakdown with change calculations
- **Export Options**: Download results or save as scenario for future reference

### 3. Scenarios Tab
- **Predefined Scenarios**: Access built-in financial modeling templates
- **Custom Scenarios**: Save your analyses with names and descriptions
- **Comparison Tools**: Select multiple scenarios for side-by-side analysis
- **Export/Import**: Backup scenarios or share with team members

## 🛠️ API Endpoints

The Flask backend provides these endpoints:

- `GET /api/health` - Health check and status
- `POST /api/financial-model` - Run financial model with custom parameters
- `GET /api/scenarios/predefined` - Get list of predefined scenarios
- `POST /api/scenarios/run-demo` - Run a specific predefined scenario
- `GET /api/test-connectivity` - Test API connectivity

## 📊 Sample Scenarios

### Conservative Growth
- CAPEX: $5,000
- Global SaaS COGS: 80%
- Lower expense growth rates
- Focus: Risk mitigation and steady growth

### Aggressive Expansion
- CAPEX: $15,000
- Global SaaS COGS: 90%
- Higher expense growth rates
- Focus: Rapid scaling and market capture

### Balanced Portfolio
- CAPEX: $8,000
- Global SaaS COGS: 84.3%
- Moderate expense growth
- Focus: Balanced risk/return optimization

## 🔧 Technical Details

### Frontend Stack
- **React 18** with TypeScript for type safety
- **Material-UI v5** for professional UI components
- **Chart.js** with react-chartjs-2 for interactive data visualization
- **Axios** for HTTP API calls

### Backend Stack
- **Flask** for lightweight REST API
- **Flask-CORS** for cross-origin requests
- **Pandas** for data processing
- **Existing Python modules** for financial modeling

### Development Features
- **Hot Reload**: Automatic refresh during development
- **Type Safety**: Full TypeScript support with interfaces
- **Error Handling**: Comprehensive error states and user feedback
- **Responsive Design**: Mobile-first approach with breakpoints

## 🎯 Key Benefits

1. **User Experience**: Intuitive interface replacing command-line tools
2. **Visual Analysis**: Charts and graphs instead of raw numbers
3. **Scenario Management**: Organized workflow for multiple analyses
4. **Professional Presentation**: Client-ready visualizations and reports
5. **Collaboration**: Easy sharing and comparison of scenarios
6. **Accessibility**: Web-based access from any device

## 🔮 Future Enhancements

- **Advanced Charting**: More visualization types (pie charts, scatter plots)
- **Real-time Collaboration**: Multi-user scenario editing
- **PDF Export**: Generate professional reports
- **Advanced Comparison**: Side-by-side scenario analysis with delta highlighting
- **Database Integration**: Persist scenarios and user preferences
- **Authentication**: User accounts and role-based access

## 🐛 Troubleshooting

### Common Issues

**"Cannot connect to backend"**
- Ensure Flask server is running on port 5000
- Check that proxy is configured in package.json

**"Module not found errors"**
- Run `npm install` in the frontend directory
- Run `pip3 install -r requirements.txt` in the backend directory

**"API call failures"**
- Verify the original Python API connectivity with `diagnostic_api.py`
- Check environment variables (SYNTHETIC_KEY)
- Test backend health endpoint: http://localhost:5000/api/health

### Development Tips
- Use browser dev tools to monitor network requests
- Check Flask console for backend error messages
- React dev tools extension helpful for debugging component state

## 📞 Support

This React UI builds upon the existing Python API infrastructure and provides a modern web interface for financial planning analysis. For issues specific to the underlying financial model API, refer to the base Python implementation documentation.