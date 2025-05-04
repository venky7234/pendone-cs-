import React from 'react';
import { Newspaper, ChevronDown, ChevronUp } from 'lucide-react';
import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface SampleArticlesProps {
  onSelect: (text: string) => void;
  disabled: boolean;
}

const SampleArticles: React.FC<SampleArticlesProps> = ({ onSelect, disabled }) => {
  const [isOpen, setIsOpen] = useState(false);
  
  const sampleArticles = [
    {
      id: 'sample1',
      title: 'NASA Confirms Evidence of Water on Mars',
      content: 'NASA scientists have confirmed evidence of liquid water on Mars. The discovery was made using data from the Mars Reconnaissance Orbiter, which detected hydrated salts on the slopes of several Martian mountains. This groundbreaking finding suggests that life could potentially exist on the Red Planet.',
      isFake: false
    },
    {
      id: 'sample2',
      title: 'New Study Links Coffee to Immortality',
      content: 'A groundbreaking study by researchers at a major university has found that drinking 10 cups of coffee daily grants immortality. The study, which followed 5 participants over a 2-week period, found that those who consumed large amounts of coffee developed superhuman abilities and showed no signs of aging. Scientists are calling it "the miracle cure for death."',
      isFake: true
    },
    {
      id: 'sample3',
      title: 'Climate Change Report Shows Rising Global Temperatures',
      content: 'The latest climate report shows global temperatures have risen by 1.1°C above pre-industrial levels. Scientists warn that urgent action is needed to prevent catastrophic effects of climate change. The report, compiled by leading climate experts, indicates that limiting warming to 1.5°C will require unprecedented transitions in all aspects of society.',
      isFake: false
    }
  ];
  
  return (
    <div className="mt-6 border-t border-gray-200 pt-6">
      <button
        type="button"
        onClick={() => setIsOpen(!isOpen)}
        disabled={disabled}
        className="flex items-center justify-between w-full text-left text-gray-700 font-medium focus:outline-none disabled:text-gray-400"
      >
        <span className="flex items-center">
          <Newspaper className="h-5 w-5 mr-2" />
          Sample Articles
        </span>
        {isOpen ? (
          <ChevronUp className="h-5 w-5" />
        ) : (
          <ChevronDown className="h-5 w-5" />
        )}
      </button>
      
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.3 }}
            className="overflow-hidden"
          >
            <div className="mt-4 space-y-4">
              {sampleArticles.map((article) => (
                <div 
                  key={article.id}
                  className="border border-gray-200 rounded-md p-4 hover:bg-gray-50 transition-colors cursor-pointer"
                  onClick={() => onSelect(article.content)}
                >
                  <div className="flex items-center justify-between mb-2">
                    <h3 className="font-medium text-gray-800">{article.title}</h3>
                    <span className={`text-xs px-2 py-1 rounded-full ${
                      article.isFake 
                        ? 'bg-red-100 text-red-800' 
                        : 'bg-green-100 text-green-800'
                    }`}>
                      {article.isFake ? 'Fake' : 'Real'}
                    </span>
                  </div>
                  <p className="text-sm text-gray-600 line-clamp-2">{article.content}</p>
                </div>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default SampleArticles;