import React, { useState } from 'react';
import { Send, RefreshCw, Trash2, AlertTriangle, CheckCircle } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import ResultDisplay from './ResultDisplay';
import { analyzeText } from '../services/apiService';
import { AnalysisResult } from '../types';
import SampleArticles from './SampleArticles';

const FakeNewsForm: React.FC = () => {
  const [inputText, setInputText] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!inputText.trim()) {
      setError('Please enter some text to analyze.');
      return;
    }
    
    setIsAnalyzing(true);
    setError(null);
    
    try {
      const result = await analyzeText(inputText);
      setResult(result);
    } catch (err) {
      setError('An error occurred during analysis. Please try again.');
      console.error(err);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleClear = () => {
    setInputText('');
    setResult(null);
    setError(null);
  };

  const handleSampleSelect = (text: string) => {
    setInputText(text);
    setResult(null);
    setError(null);
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label 
            htmlFor="newsText" 
            className="block text-sm font-medium text-gray-700 mb-2"
          >
            Enter News Article or Statement
          </label>
          <textarea
            id="newsText"
            className="w-full h-48 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Paste or type your news article or statement here..."
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            disabled={isAnalyzing}
          />
        </div>
        
        <AnimatePresence>
          {error && (
            <motion.div 
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              className="mb-4 p-3 bg-red-50 text-red-700 rounded-md flex items-start"
            >
              <AlertTriangle className="h-5 w-5 mr-2 mt-0.5 flex-shrink-0" />
              <span>{error}</span>
            </motion.div>
          )}
        </AnimatePresence>
        
        <div className="flex flex-wrap gap-3 mb-6">
          <button
            type="submit"
            disabled={isAnalyzing || !inputText.trim()}
            className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors disabled:bg-blue-300 disabled:cursor-not-allowed"
          >
            {isAnalyzing ? (
              <>
                <RefreshCw className="h-5 w-5 mr-2 animate-spin" />
                Analyzing...
              </>
            ) : (
              <>
                <Send className="h-5 w-5 mr-2" />
                Analyze
              </>
            )}
          </button>
          
          <button
            type="button"
            onClick={handleClear}
            disabled={isAnalyzing || (!inputText && !result)}
            className="flex items-center px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 transition-colors disabled:bg-gray-100 disabled:text-gray-400 disabled:cursor-not-allowed"
          >
            <Trash2 className="h-5 w-5 mr-2" />
            Clear
          </button>
        </div>
      </form>
      
      <SampleArticles onSelect={handleSampleSelect} disabled={isAnalyzing} />
      
      <AnimatePresence>
        {result && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
          >
            <ResultDisplay result={result} text={inputText} />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default FakeNewsForm;