import React from 'react';
import {
  Grid,
  Typography,
  Card,
  CardContent,
  CardHeader,
  Box,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip,
  Alert,
  CircularProgress,
} from '@mui/material';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line, Bar } from 'react-chartjs-2';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import TrendingDownIcon from '@mui/icons-material/TrendingDown';
import { FinancialData } from '../types/FinancialTypes';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
);

interface ResultsDisplayProps {
  data: FinancialData | null;
  loading: boolean;
}

export const ResultsDisplay: React.FC<ResultsDisplayProps> = ({ data, loading }) => {
  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <Box textAlign="center">
          <CircularProgress size={60} />
          <Typography variant="h6" sx={{ mt: 2 }}>
            Processing Financial Model...
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Please wait while we analyze your parameters
          </Typography>
        </Box>
      </Box>
    );
  }

  if (!data) {
    return (
      <Alert severity="info">
        No results available. Please run the financial model from the Parameters tab.
      </Alert>
    );
  }

  // Transform results data for charts
  const chartData = data.results.length > 0 ? 
    Object.keys(data.results[0]).map(year => ({
      year,
      value: data.results[0][year],
      formattedValue: new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        notation: 'compact',
        maximumFractionDigits: 1
      }).format(data.results[0][year])
    })) : [];

  // Calculate trend analysis
  const values = chartData.map(d => d.value);
  const trend = values.length > 1 ? 
    (values[values.length - 1] > values[0] ? 'positive' : 'negative') : 'neutral';
  const totalChange = values.length > 1 ? 
    ((values[values.length - 1] - values[0]) / Math.abs(values[0]) * 100) : 0;

  // Key metrics calculation
  const minValue = Math.min(...values);
  const maxValue = Math.max(...values);
  const avgValue = values.reduce((a, b) => a + b, 0) / values.length;

  const formatCurrency = (value: number) => 
    new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      notation: 'compact',
      maximumFractionDigits: 1
    }).format(value);

  const formatPercentage = (value: number) => 
    `${value >= 0 ? '+' : ''}${value.toFixed(1)}%`;

  // Chart.js configuration
  const lineChartData = {
    labels: chartData.map(d => d.year),
    datasets: [
      {
        label: 'Financial Projection',
        data: chartData.map(d => d.value),
        borderColor: '#1976d2',
        backgroundColor: 'rgba(25, 118, 210, 0.1)',
        borderWidth: 3,
        fill: true,
        tension: 0.4,
        pointBackgroundColor: '#1976d2',
        pointBorderColor: '#ffffff',
        pointBorderWidth: 2,
        pointRadius: 6,
        pointHoverRadius: 8,
      },
    ],
  };

  const barChartData = {
    labels: chartData.map(d => d.year),
    datasets: [
      {
        label: 'Annual Values',
        data: chartData.map(d => d.value),
        backgroundColor: chartData.map(d => 
          d.value >= 0 ? 'rgba(46, 125, 50, 0.8)' : 'rgba(211, 47, 47, 0.8)'
        ),
        borderColor: chartData.map(d => 
          d.value >= 0 ? '#2e7d32' : '#d32f2f'
        ),
        borderWidth: 1,
        borderRadius: 4,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: data?.metadata?.lineItem || 'Financial Analysis',
      },
      tooltip: {
        callbacks: {
          label: function(context: any) {
            return formatCurrency(context.parsed.y);
          }
        }
      }
    },
    scales: {
      y: {
        beginAtZero: false,
        ticks: {
          callback: function(value: any) {
            return formatCurrency(value);
          }
        }
      }
    },
  };

  return (
    <Box>
      {/* Header Information */}
      <Card sx={{ mb: 3 }}>
        <CardHeader
          title="Financial Analysis Results"
          subheader={`${data.metadata?.callPurpose} - ${data.metadata?.timestamp || 'Recent Analysis'}`}
        />
        <CardContent>
          <Grid container spacing={2}>
            <Grid item xs={12} md={4}>
              <Typography variant="body2" color="text.secondary">Client</Typography>
              <Typography variant="body1" fontWeight="bold">{data.clientName || 'N/A'}</Typography>
            </Grid>
            <Grid item xs={12} md={4}>
              <Typography variant="body2" color="text.secondary">Model</Typography>
              <Typography variant="body1" fontWeight="bold">{data.modelName || 'N/A'}</Typography>
            </Grid>
            <Grid item xs={12} md={4}>
              <Typography variant="body2" color="text.secondary">Project</Typography>
              <Typography variant="body1" fontWeight="bold">{data.projectName || 'N/A'}</Typography>
            </Grid>
            <Grid item xs={12}>
              <Typography variant="body2" color="text.secondary">Analysis Line Item</Typography>
              <Typography variant="body1" fontWeight="bold">{data.metadata?.lineItem}</Typography>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      <Grid container spacing={3}>
        {/* Key Metrics */}
        <Grid item xs={12}>
          <Card>
            <CardHeader title="Key Financial Metrics" />
            <CardContent>
              <Grid container spacing={3}>
                <Grid item xs={12} md={3}>
                  <Box textAlign="center">
                    <Typography variant="h4" color="primary">
                      {formatCurrency(avgValue)}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Average Value
                    </Typography>
                  </Box>
                </Grid>
                <Grid item xs={12} md={3}>
                  <Box textAlign="center">
                    <Typography variant="h4" color={trend === 'positive' ? 'success.main' : 'error.main'}>
                      {formatPercentage(totalChange)}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Total Change
                    </Typography>
                    <Chip 
                      icon={trend === 'positive' ? <TrendingUpIcon /> : <TrendingDownIcon />}
                      label={trend === 'positive' ? 'Growing' : 'Declining'}
                      color={trend === 'positive' ? 'success' : 'error'}
                      size="small"
                      sx={{ mt: 1 }}
                    />
                  </Box>
                </Grid>
                <Grid item xs={12} md={3}>
                  <Box textAlign="center">
                    <Typography variant="h4" color="error.main">
                      {formatCurrency(minValue)}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Minimum Value
                    </Typography>
                  </Box>
                </Grid>
                <Grid item xs={12} md={3}>
                  <Box textAlign="center">
                    <Typography variant="h4" color="success.main">
                      {formatCurrency(maxValue)}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Maximum Value
                    </Typography>
                  </Box>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        {/* Line Chart */}
        <Grid item xs={12} lg={8}>
          <Card>
            <CardHeader title="Financial Projection Trend" />
            <CardContent>
              <Box sx={{ height: 400 }}>
                <Line data={lineChartData} options={chartOptions} />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Bar Chart */}
        <Grid item xs={12} lg={4}>
          <Card>
            <CardHeader title="Year-over-Year Comparison" />
            <CardContent>
              <Box sx={{ height: 400 }}>
                <Bar data={barChartData} options={{
                  ...chartOptions,
                  plugins: {
                    ...chartOptions.plugins,
                    title: {
                      display: true,
                      text: 'Annual Performance',
                    },
                  },
                }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Trend Analysis */}
        <Grid item xs={12}>
          <Card>
            <CardHeader title="Trend Analysis & Growth Patterns" />
            <CardContent>
              <Grid container spacing={3}>
                <Grid item xs={12} md={8}>
                  <Box sx={{ height: 300 }}>
                    <Line 
                      data={{
                        labels: chartData.slice(0, -1).map((_, index) => `${chartData[index].year} → ${chartData[index + 1].year}`),
                        datasets: [
                          {
                            label: 'Year-over-Year Change',
                            data: chartData.slice(1).map((item, index) => {
                              const prevValue = chartData[index].value;
                              const change = ((item.value - prevValue) / Math.abs(prevValue)) * 100;
                              return change;
                            }),
                            borderColor: '#ff9800',
                            backgroundColor: 'rgba(255, 152, 0, 0.1)',
                            borderWidth: 3,
                            fill: true,
                            tension: 0.4,
                            pointBackgroundColor: '#ff9800',
                            pointBorderColor: '#ffffff',
                            pointBorderWidth: 2,
                            pointRadius: 6,
                          },
                        ],
                      }}
                      options={{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                          legend: {
                            position: 'top' as const,
                          },
                          title: {
                            display: true,
                            text: 'Growth Rate Trend (%)',
                          },
                          tooltip: {
                            callbacks: {
                              label: function(context: any) {
                                return `${context.parsed.y.toFixed(1)}% change`;
                              }
                            }
                          }
                        },
                        scales: {
                          y: {
                            beginAtZero: true,
                            ticks: {
                              callback: function(value: any) {
                                return `${value}%`;
                              }
                            }
                          }
                        },
                      }}
                    />
                  </Box>
                </Grid>
                <Grid item xs={12} md={4}>
                  <Box>
                    <Typography variant="h6" gutterBottom color="primary">
                      📈 Trend Insights
                    </Typography>
                    
                    <Box sx={{ mb: 2, p: 2, bgcolor: trend === 'positive' ? 'success.light' : 'error.light', borderRadius: 1 }}>
                      <Typography variant="body2" fontWeight="bold">
                        Overall Trend: {trend === 'positive' ? '📈 Growing' : '📉 Declining'}
                      </Typography>
                      <Typography variant="body2">
                        Total Change: {formatPercentage(totalChange)}
                      </Typography>
                    </Box>

                    <Box sx={{ mb: 1 }}>
                      <Typography variant="body2" color="text.secondary">Volatility:</Typography>
                      <Typography variant="body2">
                        {values.length > 2 ? 
                          `Range: ${formatCurrency(maxValue - minValue)}` : 
                          'Insufficient data'
                        }
                      </Typography>
                    </Box>

                    <Box sx={{ mb: 1 }}>
                      <Typography variant="body2" color="text.secondary">Performance:</Typography>
                      <Typography variant="body2">
                        {avgValue >= 0 ? '✅ Positive average' : '⚠️ Negative average'}
                      </Typography>
                    </Box>

                    <Box>
                      <Typography variant="body2" color="text.secondary">Pattern:</Typography>
                      <Typography variant="body2">
                        {values[values.length - 1] > values[0] ? 
                          '🚀 Improving trajectory' : 
                          '📊 Needs attention'
                        }
                      </Typography>
                    </Box>
                  </Box>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        {/* Detailed Results Table */}
        <Grid item xs={12}>
          <Card>
            <CardHeader title="Detailed Financial Projections" />
            <CardContent>
              <TableContainer component={Paper} variant="outlined">
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell><strong>Year</strong></TableCell>
                      <TableCell align="right"><strong>Value</strong></TableCell>
                      <TableCell align="right"><strong>Change from Previous</strong></TableCell>
                      <TableCell align="right"><strong>% Change</strong></TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {chartData.map((row, index) => {
                      const previousValue = index > 0 ? chartData[index - 1].value : null;
                      const change = previousValue ? row.value - previousValue : null;
                      const percentChange = previousValue ? (change! / Math.abs(previousValue)) * 100 : null;
                      
                      return (
                        <TableRow key={row.year}>
                          <TableCell component="th" scope="row">
                            <strong>{row.year}</strong>
                          </TableCell>
                          <TableCell align="right">
                            <Typography 
                              color={row.value >= 0 ? 'success.main' : 'error.main'}
                              fontWeight="bold"
                            >
                              {formatCurrency(row.value)}
                            </Typography>
                          </TableCell>
                          <TableCell align="right">
                            {change !== null ? (
                              <Typography 
                                color={change >= 0 ? 'success.main' : 'error.main'}
                              >
                                {change >= 0 ? '+' : ''}{formatCurrency(change)}
                              </Typography>
                            ) : '-'}
                          </TableCell>
                          <TableCell align="right">
                            {percentChange !== null ? (
                              <Chip
                                label={formatPercentage(percentChange)}
                                color={percentChange >= 0 ? 'success' : 'error'}
                                size="small"
                                variant="outlined"
                              />
                            ) : '-'}
                          </TableCell>
                        </TableRow>
                      );
                    })}
                  </TableBody>
                </Table>
              </TableContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* Balance Sheet Summary */}
        {data.balanceSheetItems && data.balanceSheetItems.length > 0 && (
          <Grid item xs={12}>
            <Card>
              <CardHeader 
                title="Balance Sheet Line Items"
                subheader={`${data.balanceSheetItems.length} items available`}
              />
              <CardContent>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  Balance sheet data includes {data.balanceSheetItems.length} line items covering assets, liabilities, 
                  income statement details, and cash flow components.
                </Typography>
                <Alert severity="info">
                  Balance sheet details available in the raw API response. 
                  Consider implementing a dedicated balance sheet analysis view for detailed breakdown.
                </Alert>
              </CardContent>
            </Card>
          </Grid>
        )}
      </Grid>
    </Box>
  );
};