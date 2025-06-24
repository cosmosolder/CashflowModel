import React, { useState } from 'react';
import {
  Container,
  Paper,
  Typography,
  Box,
  Tabs,
  Tab,
  ThemeProvider,
  createTheme,
  CssBaseline,
  AppBar,
  Toolbar,
} from '@mui/material';
import AccountBalanceIcon from '@mui/icons-material/AccountBalance';
import { ParameterInput } from './components/ParameterInput';
import { ResultsDisplay } from './components/ResultsDisplay';
import { ScenarioManager } from './components/ScenarioManager';
import { FinancialData, ScenarioData } from './types/FinancialTypes';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
    background: {
      default: '#f5f5f5',
    },
  },
});

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

function App() {
  const [tabValue, setTabValue] = useState(0);
  const [results, setResults] = useState<FinancialData | null>(null);
  const [loading, setLoading] = useState(false);
  const [scenarios, setScenarios] = useState<ScenarioData[]>([]);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const handleParameterSubmit = async (parameters: any) => {
    setLoading(true);
    try {
      // Call the backend API here
      const response = await fetch('/api/financial-model', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(parameters),
      });
      
      if (response.ok) {
        const data = await response.json();
        setResults(data);
        setTabValue(1); // Switch to results tab
      } else {
        console.error('API call failed');
      }
    } catch (error) {
      console.error('Error calling API:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleScenarioSave = (scenario: ScenarioData) => {
    setScenarios(prev => [...prev, scenario]);
  };

  const handleScenarioLoad = (scenario: ScenarioData) => {
    // Load scenario parameters and switch to input tab
    setTabValue(0);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AppBar position="static" elevation={1}>
        <Toolbar>
          <AccountBalanceIcon sx={{ mr: 2 }} />
          <Typography variant="h6" component="div">
            Financial Planning Model - Interactive Dashboard
          </Typography>
        </Toolbar>
      </AppBar>

      <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
        <Paper elevation={2}>
          <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
            <Tabs value={tabValue} onChange={handleTabChange} aria-label="financial planning tabs">
              <Tab label="Model Parameters" />
              <Tab label="Results & Analysis" />
              <Tab label="Scenario Management" />
            </Tabs>
          </Box>

          <TabPanel value={tabValue} index={0}>
            <ParameterInput
              onSubmit={handleParameterSubmit}
              loading={loading}
            />
          </TabPanel>

          <TabPanel value={tabValue} index={1}>
            <ResultsDisplay
              data={results}
              loading={loading}
            />
          </TabPanel>

          <TabPanel value={tabValue} index={2}>
            <ScenarioManager
              scenarios={scenarios}
              onSave={handleScenarioSave}
              onLoad={handleScenarioLoad}
              currentResults={results}
            />
          </TabPanel>
        </Paper>
      </Container>
    </ThemeProvider>
  );
}

export default App;
