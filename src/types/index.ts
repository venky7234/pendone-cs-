export interface Highlight {
  start: number;
  end: number;
  score: number;
}

export interface AnalysisResult {
  prediction: 'FAKE' | 'REAL';
  confidence: number;
  highlights?: Highlight[];
}