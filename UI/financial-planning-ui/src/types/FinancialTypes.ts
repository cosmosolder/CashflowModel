export interface LeaseEntry {
  leaseName: string;
  expiryDate: string;
  remainingLife: number;
  renewable: boolean;
  avgNewLeaseLife: number;
  leaseliabilityPct: number;
  borrowingRate: number;
}

export interface YearlyRates {
  Y1: number;
  Y2: number;
  Y3: number;
  Y4: number;
  Y5: number;
}

export interface FinancialParameters {
  capex: number;
  existingLeases: LeaseEntry[];
  existingPPELife: number;
  newPPELife: number;
  gaPersonnelRates: number[];
  gaNonPersonnelRates: number[];
  rdPersonnelRates: number[];
  rdNonPersonnelRates: number[];
  globalSaasCogs: number;
  interestIncome: number;
  lineItem: string;
  callPurpose: string;
}

export interface FinancialResults {
  [year: string]: number;
}

export interface BalanceSheetItem {
  lineItem: string;
  values?: { [year: string]: number };
}

export interface FinancialData {
  clientName?: string;
  modelName?: string;
  projectName?: string;
  results: FinancialResults[];
  balanceSheetItems: BalanceSheetItem[];
  metadata: {
    lineItem: string;
    callPurpose: string;
    timestamp: string;
  };
}

export interface ScenarioData {
  id: string;
  name: string;
  description: string;
  parameters: FinancialParameters;
  results?: FinancialData;
  createdAt: string;
}

export interface ApiResponse {
  status: string;
  response_data: {
    outputs: {
      ClientName: string;
      ModelName: string;
      ProjectName: string;
      Results: FinancialResults[];
      BalanceSheet_lineitems: any[];
    };
  };
  error?: string;
}

export const DEFAULT_SCENARIOS = [
  {
    name: 'Conservative Growth',
    description: 'Low-risk scenario with modest growth projections',
    parameters: {
      capex: 5000,
      gaPersonnelRates: [0.030, 0.028, 0.026, 0.024, 0.022],
      gaNonPersonnelRates: [0.035, 0.033, 0.031, 0.029, 0.027],
      rdPersonnelRates: [0.080, 0.075, 0.070, 0.065, 0.060],
      rdNonPersonnelRates: [0.025, 0.024, 0.023, 0.022, 0.021],
      globalSaasCogs: 0.800,
      interestIncome: 0.015,
      lineItem: 'Income Statement : GAAP Net Income : GAAP Net Income'
    }
  },
  {
    name: 'Aggressive Expansion',
    description: 'High-growth scenario with increased investments',
    parameters: {
      capex: 15000,
      gaPersonnelRates: [0.045, 0.042, 0.040, 0.038, 0.036],
      gaNonPersonnelRates: [0.050, 0.048, 0.046, 0.044, 0.042],
      rdPersonnelRates: [0.120, 0.115, 0.110, 0.105, 0.100],
      rdNonPersonnelRates: [0.040, 0.038, 0.036, 0.034, 0.032],
      globalSaasCogs: 0.900,
      interestIncome: 0.008,
      lineItem: 'Income Statement : Revenue : Total Revenue'
    }
  },
  {
    name: 'Balanced Portfolio',
    description: 'Moderate growth with balanced risk/return',
    parameters: {
      capex: 8000,
      gaPersonnelRates: [0.0356, 0.0338, 0.0321, 0.0289, 0.0284],
      gaNonPersonnelRates: [0.0413, 0.041, 0.0390, 0.0370, 0.0352],
      rdPersonnelRates: [0.0929, 0.091, 0.089, 0.088, 0.088],
      rdNonPersonnelRates: [0.0312, 0.031, 0.029, 0.029, 0.029],
      globalSaasCogs: 0.843,
      interestIncome: 0.010,
      lineItem: 'Balance Sheet : Total Assets : Total Assets'
    }
  }
];

export const LINE_ITEM_OPTIONS = [
  'Income Statement : GAAP Net Income : GAAP Net Income',
  'Income Statement : Revenue : Total Revenue',
  'Balance Sheet : Total Assets : Total Assets',
  'Cash Flow : Operating Cash Flow : Operating Cash Flow'
];