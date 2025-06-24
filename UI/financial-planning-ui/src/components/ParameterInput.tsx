import React, { useState } from 'react';
import {
  Grid,
  TextField,
  Button,
  Typography,
  Card,
  CardContent,
  CardHeader,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Box,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  CircularProgress,
  Alert,
  Chip,
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import { FinancialParameters, DEFAULT_SCENARIOS, LINE_ITEM_OPTIONS } from '../types/FinancialTypes';

interface ParameterInputProps {
  onSubmit: (parameters: FinancialParameters) => void;
  loading: boolean;
}

export const ParameterInput: React.FC<ParameterInputProps> = ({ onSubmit, loading }) => {
  const [parameters, setParameters] = useState<FinancialParameters>({
    capex: 8000,
    existingLeases: [],
    existingPPELife: 15,
    newPPELife: 15,
    gaPersonnelRates: [0.0356, 0.0338, 0.0321, 0.0289, 0.0284],
    gaNonPersonnelRates: [0.0413, 0.041, 0.0390, 0.0370, 0.0352],
    rdPersonnelRates: [0.0929, 0.091, 0.089, 0.088, 0.088],
    rdNonPersonnelRates: [0.0312, 0.031, 0.029, 0.029, 0.029],
    globalSaasCogs: 0.843,
    interestIncome: 0.01,
    lineItem: 'Income Statement : GAAP Net Income : GAAP Net Income',
    callPurpose: 'React UI Analysis',
  });

  const [selectedScenario, setSelectedScenario] = useState<string>('');

  const handleInputChange = (field: keyof FinancialParameters, value: any) => {
    setParameters(prev => ({
      ...prev,
      [field]: value,
    }));
  };

  const handleRateChange = (rateType: 'gaPersonnelRates' | 'gaNonPersonnelRates' | 'rdPersonnelRates' | 'rdNonPersonnelRates', index: number, value: number) => {
    setParameters(prev => ({
      ...prev,
      [rateType]: prev[rateType].map((rate, i) => i === index ? value : rate),
    }));
  };

  const loadScenario = (scenarioName: string) => {
    const scenario = DEFAULT_SCENARIOS.find(s => s.name === scenarioName);
    if (scenario) {
      setParameters(prev => ({
        ...prev,
        ...scenario.parameters,
        callPurpose: `React UI - ${scenarioName}`,
      }));
      setSelectedScenario(scenarioName);
    }
  };

  const handleSubmit = () => {
    onSubmit(parameters);
  };

  const formatPercentage = (value: number) => `${(value * 100).toFixed(2)}%`;

  return (
    <Box>
      {/* Scenario Quick Select */}
      <Card sx={{ mb: 3 }}>
        <CardHeader 
          title="Quick Start - Load Predefined Scenario" 
          subheader="Choose a predefined scenario or customize parameters below"
        />
        <CardContent>
          <Grid container spacing={2} sx={{ alignItems: 'center' }}>
            <Grid item xs={12} md={8}>
              <FormControl fullWidth>
                <InputLabel>Select Scenario</InputLabel>
                <Select
                  value={selectedScenario}
                  label="Select Scenario"
                  onChange={(e) => loadScenario(e.target.value)}
                >
                  {DEFAULT_SCENARIOS.map((scenario) => (
                    <MenuItem key={scenario.name} value={scenario.name}>
                      <Box>
                        <Typography variant="body2" fontWeight="bold">
                          {scenario.name}
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          {scenario.description}
                        </Typography>
                      </Box>
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={4}>
              {selectedScenario && (
                <Chip 
                  label={`Loaded: ${selectedScenario}`} 
                  color="primary" 
                  variant="outlined"
                />
              )}
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Main Parameters */}
      <Accordion defaultExpanded>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography variant="h6">Core Financial Parameters</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Capital Expenditure (CAPEX)"
                type="number"
                value={parameters.capex}
                onChange={(e) => handleInputChange('capex', Number(e.target.value))}
                helperText="Investment in fixed assets"
                InputProps={{
                  startAdornment: '$',
                }}
              />
            </Grid>
            <Grid item xs={12} md={3}>
              <TextField
                fullWidth
                label="Existing PPE Life (years)"
                type="number"
                value={parameters.existingPPELife}
                onChange={(e) => handleInputChange('existingPPELife', Number(e.target.value))}
              />
            </Grid>
            <Grid item xs={12} md={3}>
              <TextField
                fullWidth
                label="New PPE Life (years)"
                type="number"
                value={parameters.newPPELife}
                onChange={(e) => handleInputChange('newPPELife', Number(e.target.value))}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Global SaaS COGS Rate"
                type="number"
                value={parameters.globalSaasCogs}
                onChange={(e) => handleInputChange('globalSaasCogs', Number(e.target.value))}
                helperText={`Current: ${formatPercentage(parameters.globalSaasCogs)}`}
                inputProps={{ step: 0.001, min: 0, max: 1 }}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Interest Income Rate"
                type="number"
                value={parameters.interestIncome}
                onChange={(e) => handleInputChange('interestIncome', Number(e.target.value))}
                helperText={`Current: ${formatPercentage(parameters.interestIncome)}`}
                inputProps={{ step: 0.001, min: 0, max: 1 }}
              />
            </Grid>
            <Grid item xs={12}>
              <FormControl fullWidth>
                <InputLabel>Analysis Line Item</InputLabel>
                <Select
                  value={parameters.lineItem}
                  label="Analysis Line Item"
                  onChange={(e) => handleInputChange('lineItem', e.target.value)}
                >
                  {LINE_ITEM_OPTIONS.map((item) => (
                    <MenuItem key={item} value={item}>
                      {item}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Analysis Purpose"
                value={parameters.callPurpose}
                onChange={(e) => handleInputChange('callPurpose', e.target.value)}
                helperText="Description of this analysis"
              />
            </Grid>
          </Grid>
        </AccordionDetails>
      </Accordion>

      {/* Rate Parameters */}
      <Accordion>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography variant="h6">Expense Rate Projections (5-Year)</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Grid container spacing={3}>
            {/* GA Personnel Rates */}
            <Grid item xs={12} md={6}>
              <Card variant="outlined">
                <CardHeader title="GA Personnel Expense Rates" />
                <CardContent>
                  <Grid container spacing={2}>
                    {parameters.gaPersonnelRates.map((rate, index) => (
                      <Grid item xs={12} key={`ga-personnel-${index}`}>
                        <TextField
                          fullWidth
                          label={`Year ${index + 1}`}
                          type="number"
                          value={rate}
                          onChange={(e) => handleRateChange('gaPersonnelRates', index, Number(e.target.value))}
                          helperText={formatPercentage(rate)}
                          inputProps={{ step: 0.001, min: 0, max: 1 }}
                        />
                      </Grid>
                    ))}
                  </Grid>
                </CardContent>
              </Card>
            </Grid>

            {/* GA Non-Personnel Rates */}
            <Grid item xs={12} md={6}>
              <Card variant="outlined">
                <CardHeader title="GA Non-Personnel Expense Rates" />
                <CardContent>
                  <Grid container spacing={2}>
                    {parameters.gaNonPersonnelRates.map((rate, index) => (
                      <Grid item xs={12} key={`ga-nonpersonnel-${index}`}>
                        <TextField
                          fullWidth
                          label={`Year ${index + 1}`}
                          type="number"
                          value={rate}
                          onChange={(e) => handleRateChange('gaNonPersonnelRates', index, Number(e.target.value))}
                          helperText={formatPercentage(rate)}
                          inputProps={{ step: 0.001, min: 0, max: 1 }}
                        />
                      </Grid>
                    ))}
                  </Grid>
                </CardContent>
              </Card>
            </Grid>

            {/* R&D Personnel Rates */}
            <Grid item xs={12} md={6}>
              <Card variant="outlined">
                <CardHeader title="R&D Personnel Expense Rates" />
                <CardContent>
                  <Grid container spacing={2}>
                    {parameters.rdPersonnelRates.map((rate, index) => (
                      <Grid item xs={12} key={`rd-personnel-${index}`}>
                        <TextField
                          fullWidth
                          label={`Year ${index + 1}`}
                          type="number"
                          value={rate}
                          onChange={(e) => handleRateChange('rdPersonnelRates', index, Number(e.target.value))}
                          helperText={formatPercentage(rate)}
                          inputProps={{ step: 0.001, min: 0, max: 1 }}
                        />
                      </Grid>
                    ))}
                  </Grid>
                </CardContent>
              </Card>
            </Grid>

            {/* R&D Non-Personnel Rates */}
            <Grid item xs={12} md={6}>
              <Card variant="outlined">
                <CardHeader title="R&D Non-Personnel Expense Rates" />
                <CardContent>
                  <Grid container spacing={2}>
                    {parameters.rdNonPersonnelRates.map((rate, index) => (
                      <Grid item xs={12} key={`rd-nonpersonnel-${index}`}>
                        <TextField
                          fullWidth
                          label={`Year ${index + 1}`}
                          type="number"
                          value={rate}
                          onChange={(e) => handleRateChange('rdNonPersonnelRates', index, Number(e.target.value))}
                          helperText={formatPercentage(rate)}
                          inputProps={{ step: 0.001, min: 0, max: 1 }}
                        />
                      </Grid>
                    ))}
                  </Grid>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </AccordionDetails>
      </Accordion>

      {/* Submit Button */}
      <Box sx={{ mt: 4, display: 'flex', justifyContent: 'center' }}>
        <Button
          variant="contained"
          size="large"
          onClick={handleSubmit}
          disabled={loading}
          startIcon={loading ? <CircularProgress size={20} /> : <PlayArrowIcon />}
          sx={{ minWidth: 200, py: 1.5 }}
        >
          {loading ? 'Running Analysis...' : 'Run Financial Model'}
        </Button>
      </Box>

      {loading && (
        <Alert severity="info" sx={{ mt: 2 }}>
          Processing your financial model analysis. This may take a few moments...
        </Alert>
      )}
    </Box>
  );
};