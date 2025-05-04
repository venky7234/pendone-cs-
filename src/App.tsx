import React from 'react';
import { Verified as NewsMagnifier } from 'lucide-react';
import { motion } from 'framer-motion';
import Header from './components/Header';
import FakeNewsForm from './components/FakeNewsForm';
import Footer from './components/Footer';

function App() {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <Header />
      
      <main className="flex-grow container mx-auto px-4 py-8">
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="max-w-4xl mx-auto"
        >
          <div className="flex items-center justify-center mb-8">
            <NewsMagnifier size={40} className="text-blue-600 mr-3" />
            <h1 className="text-3xl md:text-4xl font-bold text-gray-800">
              Fake News Detector
            </h1>
          </div>
          
          <p className="text-center text-gray-600 mb-8 max-w-2xl mx-auto">
            Paste a news article or statement below to analyze its credibility using our advanced 
            Natural Language Processing technology.
          </p>
          
          <FakeNewsForm />
        </motion.div>
      </main>
      
      <Footer />
    </div>
  );
}

export default App;