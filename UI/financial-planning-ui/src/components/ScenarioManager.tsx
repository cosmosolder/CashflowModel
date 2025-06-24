import React, { useState } from 'react';
import {
  Grid,
  Typography,
  Card,
  CardContent,
  CardHeader,
  CardActions,
  Button,
  Box,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  Chip,
  Alert,
  Divider,
} from '@mui/material';
import {
  Save as SaveIcon,
  PlayArrow as PlayIcon,
  Delete as DeleteIcon,
  Compare as CompareIcon,
  Download as DownloadIcon,
} from '@mui/icons-material';
import { FinancialData, ScenarioData, DEFAULT_SCENARIOS } from '../types/FinancialTypes';

interface ScenarioManagerProps {
  scenarios: ScenarioData[];
  onSave: (scenario: ScenarioData) => void;
  onLoad: (scenario: ScenarioData) => void;
  currentResults: FinancialData | null;
}

export const ScenarioManager: React.FC<ScenarioManagerProps> = ({
  scenarios,
  onSave,
  onLoad,
  currentResults,
}) => {
  const [saveDialogOpen, setSaveDialogOpen] = useState(false);
  const [scenarioName, setScenarioName] = useState('');
  const [scenarioDescription, setScenarioDescription] = useState('');
  const [compareMode, setCompareMode] = useState(false);
  const [selectedScenarios, setSelectedScenarios] = useState<string[]>([]);

  const handleSaveScenario = () => {
    if (scenarioName.trim() && currentResults) {
      const newScenario: ScenarioData = {
        id: Date.now().toString(),
        name: scenarioName.trim(),
        description: scenarioDescription.trim(),
        parameters: {
          capex: 0, // These would be populated from current form state
          existingLeases: [],
          existingPPELife: 15,
          newPPELife: 15,
          gaPersonnelRates: [],
          gaNonPersonnelRates: [],
          rdPersonnelRates: [],
          rdNonPersonnelRates: [],
          globalSaasCogs: 0,
          interestIncome: 0,
          lineItem: '',
          callPurpose: scenarioName,
        },
        results: currentResults,
        createdAt: new Date().toISOString(),
      };

      onSave(newScenario);
      setSaveDialogOpen(false);
      setScenarioName('');
      setScenarioDescription('');
    }
  };

  const handleScenarioSelect = (scenarioId: string) => {
    if (compareMode) {
      setSelectedScenarios(prev => 
        prev.includes(scenarioId) 
          ? prev.filter(id => id !== scenarioId)
          : [...prev, scenarioId].slice(0, 3) // Max 3 scenarios for comparison
      );
    }
  };

  const exportScenarios = () => {
    const dataStr = JSON.stringify(scenarios, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `financial-scenarios-${new Date().toISOString().split('T')[0]}.json`;
    link.click();
    URL.revokeObjectURL(url);
  };

  const getScenarioSummary = (scenario: ScenarioData) => {
    if (!scenario.results || !scenario.results.results.length) return null;
    
    const values = Object.values(scenario.results.results[0]);
    const total = values.reduce((a, b) => a + b, 0);
    const trend = values[values.length - 1] > values[0] ? '📈' : '📉';
    
    return {
      total: new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        notation: 'compact'
      }).format(total),
      trend
    };
  };

  return (
    <Box>
      {/* Header Actions */}
      <Card sx={{ mb: 3 }}>
        <CardHeader title="Scenario Management" />
        <CardContent>
          <Grid container spacing={2} alignItems="center">
            <Grid item>
              <Button
                variant="contained"
                startIcon={<SaveIcon />}
                onClick={() => setSaveDialogOpen(true)}
                disabled={!currentResults}
              >
                Save Current Analysis
              </Button>
            </Grid>
            <Grid item>
              <Button
                variant="outlined"
                startIcon={<CompareIcon />}
                onClick={() => setCompareMode(!compareMode)}
                color={compareMode ? 'secondary' : 'primary'}
              >
                {compareMode ? 'Exit Compare' : 'Compare Scenarios'}
              </Button>
            </Grid>
            <Grid item>
              <Button
                variant="outlined"
                startIcon={<DownloadIcon />}
                onClick={exportScenarios}
                disabled={scenarios.length === 0}
              >
                Export All
              </Button>
            </Grid>
          </Grid>

          {compareMode && (
            <Alert severity="info" sx={{ mt: 2 }}>
              Select up to 3 scenarios to compare. Selected: {selectedScenarios.length}/3
            </Alert>
          )}
        </CardContent>
      </Card>

      <Grid container spacing={3}>
        {/* Predefined Scenarios */}
        <Grid item xs={12} lg={6}>
          <Card>
            <CardHeader 
              title="Predefined Scenarios"
              subheader="Standard financial modeling scenarios"
            />
            <CardContent>
              <List>
                {DEFAULT_SCENARIOS.map((scenario, index) => (
                  <ListItem
                    key={index}
                    divider={index < DEFAULT_SCENARIOS.length - 1}
                    sx={{
                      border: selectedScenarios.includes(scenario.name) ? 2 : 0,
                      borderColor: 'primary.main',
                      borderRadius: 1,
                      mb: selectedScenarios.includes(scenario.name) ? 1 : 0,
                      cursor: compareMode ? 'pointer' : 'default',
                    }}
                    onClick={() => compareMode && handleScenarioSelect(scenario.name)}
                  >
                    <ListItemText
                      primary={
                        <Box display="flex" alignItems="center" gap={1}>
                          <Typography variant="subtitle1" fontWeight="bold">
                            {scenario.name}
                          </Typography>
                          <Chip 
                            label="Predefined" 
                            size="small" 
                            color="primary" 
                            variant="outlined" 
                          />
                        </Box>
                      }
                      secondary={scenario.description}
                    />
                    <ListItemSecondaryAction>
                      <IconButton
                        edge="end"
                        onClick={() => onLoad({
                          id: scenario.name,
                          name: scenario.name,
                          description: scenario.description,
                          parameters: scenario.parameters as any,
                          createdAt: new Date().toISOString(),
                        })}
                      >
                        <PlayIcon />
                      </IconButton>
                    </ListItemSecondaryAction>
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>

        {/* Saved Scenarios */}
        <Grid item xs={12} lg={6}>
          <Card>
            <CardHeader 
              title="Saved Scenarios"
              subheader={`${scenarios.length} custom scenarios`}
            />
            <CardContent>
              {scenarios.length === 0 ? (
                <Alert severity="info">
                  No saved scenarios yet. Run an analysis and save it to create your first scenario.
                </Alert>
              ) : (
                <List>
                  {scenarios.map((scenario, index) => {
                    const summary = getScenarioSummary(scenario);
                    
                    return (
                      <ListItem
                        key={scenario.id}
                        divider={index < scenarios.length - 1}
                        sx={{
                          border: selectedScenarios.includes(scenario.id) ? 2 : 0,
                          borderColor: 'primary.main',
                          borderRadius: 1,
                          mb: selectedScenarios.includes(scenario.id) ? 1 : 0,
                          cursor: compareMode ? 'pointer' : 'default',
                        }}
                        onClick={() => compareMode && handleScenarioSelect(scenario.id)}
                      >
                        <ListItemText
                          primary={
                            <Box display="flex" alignItems="center" gap={1}>
                              <Typography variant="subtitle1" fontWeight="bold">
                                {scenario.name}
                              </Typography>
                              {summary && (
                                <>
                                  <Chip 
                                    label={summary.total} 
                                    size="small" 
                                    color="success" 
                                    variant="outlined" 
                                  />
                                  <Typography variant="body2">
                                    {summary.trend}
                                  </Typography>
                                </>
                              )}
                            </Box>
                          }
                          secondary={
                            <Box>
                              <Typography variant="body2" color="text.secondary">
                                {scenario.description}
                              </Typography>
                              <Typography variant="caption" color="text.secondary">
                                Created: {new Date(scenario.createdAt).toLocaleDateString()}
                              </Typography>
                            </Box>
                          }
                        />
                        <ListItemSecondaryAction>
                          <Box>
                            <IconButton
                              size="small"
                              onClick={() => onLoad(scenario)}
                            >
                              <PlayIcon />
                            </IconButton>
                            <IconButton
                              size="small"
                              color="error"
                              onClick={() => {
                                // Handle delete - would need to add delete handler to props
                                console.log('Delete scenario:', scenario.id);
                              }}
                            >
                              <DeleteIcon />
                            </IconButton>
                          </Box>
                        </ListItemSecondaryAction>
                      </ListItem>
                    );
                  })}
                </List>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Scenario Comparison */}
        {compareMode && selectedScenarios.length > 1 && (
          <Grid item xs={12}>
            <Card>
              <CardHeader title="Scenario Comparison" />
              <CardContent>
                <Alert severity="success">
                  Comparing {selectedScenarios.length} scenarios. 
                  This would show a side-by-side comparison chart and key differences.
                </Alert>
                <Box sx={{ mt: 2 }}>
                  <Typography variant="h6" gutterBottom>Selected Scenarios:</Typography>
                  <Box display="flex" gap={1} flexWrap="wrap">
                    {selectedScenarios.map(id => (
                      <Chip
                        key={id}
                        label={scenarios.find(s => s.id === id)?.name || id}
                        onDelete={() => handleScenarioSelect(id)}
                        color="primary"
                      />
                    ))}
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        )}
      </Grid>

      {/* Save Scenario Dialog */}
      <Dialog open={saveDialogOpen} onClose={() => setSaveDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Save Current Analysis as Scenario</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Scenario Name"
            fullWidth
            variant="outlined"
            value={scenarioName}
            onChange={(e) => setScenarioName(e.target.value)}
            sx={{ mb: 2 }}
          />
          <TextField
            margin="dense"
            label="Description"
            fullWidth
            multiline
            rows={3}
            variant="outlined"
            value={scenarioDescription}
            onChange={(e) => setScenarioDescription(e.target.value)}
            helperText="Describe the key assumptions or purpose of this scenario"
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setSaveDialogOpen(false)}>Cancel</Button>
          <Button 
            onClick={handleSaveScenario} 
            variant="contained"
            disabled={!scenarioName.trim()}
          >
            Save Scenario
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};