import React from 'react';
import { motion } from 'framer-motion';
import { CheckCircle, AlertTriangle, Info } from 'lucide-react';
import { AnalysisResult } from '../types';
import HighlightedText from './HighlightedText';

interface ResultDisplayProps {
  result: AnalysisResult;
  text: string;
}

const ResultDisplay: React.FC<ResultDisplayProps> = ({ result, text }) => {
  const { prediction, confidence, highlights } = result;
  
  const isPredictionFake = prediction === 'FAKE';
  
  // Format confidence as percentage
  const confidencePercent = (confidence * 100).toFixed(1);
  
  // Determine color classes based on prediction
  const colorClasses = isPredictionFake 
    ? {
        border: 'border-red-200',
        bg: 'bg-red-50',
        icon: 'text-red-500',
        title: 'text-red-700',
        meter: 'bg-red-500'
      }
    : {
        border: 'border-green-200',
        bg: 'bg-green-50',
        icon: 'text-green-500',
        title: 'text-green-700',
        meter: 'bg-green-500'
      };
  
  return (
    <motion.div 
      className={`mt-8 border ${colorClasses.border} rounded-lg overflow-hidden`}
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      <div className={`p-4 ${colorClasses.bg} flex items-center`}>
        {isPredictionFake ? (
          <AlertTriangle className={`h-6 w-6 ${colorClasses.icon} mr-3`} />
        ) : (
          <CheckCircle className={`h-6 w-6 ${colorClasses.icon} mr-3`} />
        )}
        <h2 className={`text-xl font-bold ${colorClasses.title}`}>
          {isPredictionFake ? 'This content appears to be fake' : 'This content appears to be real'}
        </h2>
      </div>
      
      <div className="p-6 bg-white">
        <div className="mb-6">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium text-gray-700">Confidence Level</span>
            <span className="text-sm font-medium">{confidencePercent}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2.5">
            <motion.div 
              className={`h-2.5 rounded-full ${colorClasses.meter}`} 
              initial={{ width: 0 }}
              animate={{ width: `${confidencePercent}%` }}
              transition={{ duration: 0.8, ease: "easeOut" }}
            ></motion.div>
          </div>
        </div>
        
        <div className="mb-6">
          <h3 className="text-lg font-medium text-gray-800 mb-3">Analysis Details</h3>
          <div className="text-gray-600 text-sm space-y-2">
            <p>
              <strong>Model Prediction:</strong> {prediction}
            </p>
            <p>
              <strong>Confidence Score:</strong> {confidencePercent}%
            </p>
            <p>
              <strong>Analysis Date:</strong> {new Date().toLocaleString()}
            </p>
          </div>
        </div>
        
        <div className="mb-6">
          <h3 className="text-lg font-medium text-gray-800 mb-3">Analyzed Text</h3>
          <div className="p-4 bg-gray-50 rounded-md text-sm text-gray-700 max-h-60 overflow-y-auto">
            <HighlightedText text={text} highlights={highlights || []} />
          </div>
        </div>
        
        <div className="flex items-start">
          <Info className="h-5 w-5 text-blue-500 mr-2 mt-0.5 flex-shrink-0" />
          <p className="text-sm text-gray-600">
            This analysis is based on machine learning and should be used as a tool, not as definitive proof. 
            Always cross-reference information with trusted sources.
          </p>
        </div>
      </div>
    </motion.div>
  );
};

export default ResultDisplay;