import axios from 'axios';
import { AnalysisResult } from '../types';

// For development, point to the local Flask server
const API_URL = 'http://localhost:5000';

/**
 * Sends text to the backend for fake news analysis
 * @param text The text to analyze
 * @returns Analysis result with prediction and confidence
 */
export const analyzeText = async (text: string): Promise<AnalysisResult> => {
  try {
    // In development mode, simulate a response for testing the UI
    // This would be replaced with the actual API call in production
    if (process.env.NODE_ENV === 'development') {
      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      // Simulate a response based on text content
      const isFakeIndicators = [
        'miracle', 'shocking', 'they don\'t want you to know', 
        'government conspiracy', 'cure for all', 'amazing discovery',
        'immortality', 'breakthrough', 'secret', 'conspiracy'
      ];
      
      const textLower = text.toLowerCase();
      const containsFakeIndicators = isFakeIndicators.some(indicator => 
        textLower.includes(indicator.toLowerCase())
      );
      
      // Calculate a "confidence" based on text length and fake indicators
      let confidence = Math.random() * 0.3 + 0.6; // Random between 0.6 and 0.9
      if (containsFakeIndicators) {
        confidence = Math.random() * 0.2 + 0.75; // Higher confidence for fake
      }
      
      // Generate some mock highlights based on content
      const words = text.split(/\s+/);
      const highlights = [];
      
      let position = 0;
      for (const word of words) {
        const start = text.indexOf(word, position);
        const end = start + word.length;
        position = end;
        
        // Highlight suspicious words with high score
        if (isFakeIndicators.some(indicator => word.toLowerCase().includes(indicator.toLowerCase()))) {
          highlights.push({
            start,
            end,
            score: Math.random() * 0.4 + 0.6 // High score for suspicious words
          });
        }
        // Randomly highlight some other words with lower scores
        else if (Math.random() < 0.05 && word.length > 4) {
          highlights.push({
            start,
            end,
            score: Math.random() * 0.5
          });
        }
      }
      
      return {
        prediction: containsFakeIndicators ? 'FAKE' : 'REAL',
        confidence,
        highlights
      };
    }
    
    // This would be the actual API call in production
    const response = await axios.post(`${API_URL}/analyze`, { text });
    return response.data;
  } catch (error) {
    console.error('Error analyzing text:', error);
    throw new Error('Failed to analyze text. Please try again.');
  }
};