import React from 'react';
import { Highlight } from '../types';

interface HighlightedTextProps {
  text: string;
  highlights: Highlight[];
}

const HighlightedText: React.FC<HighlightedTextProps> = ({ text, highlights }) => {
  if (!highlights.length) {
    return <p>{text}</p>;
  }
  
  // Sort highlights by start index to process in order
  const sortedHighlights = [...highlights].sort((a, b) => a.start - b.start);
  
  // Split text into segments with highlights
  let lastIndex = 0;
  const segments = [];
  
  sortedHighlights.forEach((highlight, index) => {
    // Add text before the highlight
    if (highlight.start > lastIndex) {
      segments.push({
        text: text.substring(lastIndex, highlight.start),
        isHighlighted: false,
        score: 0,
        id: `normal-${index}`
      });
    }
    
    // Add the highlighted segment
    segments.push({
      text: text.substring(highlight.start, highlight.end),
      isHighlighted: true,
      score: highlight.score,
      id: `highlight-${index}`
    });
    
    lastIndex = highlight.end;
  });
  
  // Add any remaining text after the last highlight
  if (lastIndex < text.length) {
    segments.push({
      text: text.substring(lastIndex),
      isHighlighted: false,
      score: 0,
      id: `normal-end`
    });
  }
  
  // Render text with highlighted segments
  return (
    <p>
      {segments.map((segment) => {
        if (!segment.isHighlighted) {
          return <span key={segment.id}>{segment.text}</span>;
        }
        
        // Determine highlight color based on score
        // Higher score = more suspicious (redder)
        const opacity = Math.min(Math.max(segment.score, 0.1), 0.9).toFixed(1);
        const highlightClass = `bg-red-${Math.round(opacity * 100)} rounded px-0.5`;
        
        return (
          <span 
            key={segment.id} 
            className={highlightClass}
            title={`Suspicion score: ${(segment.score * 100).toFixed(0)}%`}
          >
            {segment.text}
          </span>
        );
      })}
    </p>
  );
};

export default HighlightedText;