import React from 'react';
import { Sparkles } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const Hero = () => {
  const navigate = useNavigate();

  const handleGetStarted = () => {
    navigate('/auth', { state: { isLogin: false } });
  };

  return (
    <div className="relative overflow-hidden">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
        <div className="text-center">
          <h1 className="text-5xl md:text-6xl font-bold mb-8 bg-clip-text text-transparent bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500">
            Learn Smarter, Not Harder
          </h1>
          <p className="text-xl text-gray-400 mb-12 max-w-2xl mx-auto">
            Transform your study experience with AI-powered tools, smart note-taking, and instant video translations.
          </p>
          <div className="flex justify-center space-x-4">
            <button 
              onClick={handleGetStarted}
              className="bg-indigo-600 hover:bg-indigo-700 text-white px-8 py-4 rounded-lg font-semibold flex items-center transition-colors"
            >
              <Sparkles className="w-5 h-5 mr-2" />
              Get Started Free
            </button>
            <button className="bg-gray-800 hover:bg-gray-700 text-white px-8 py-4 rounded-lg font-semibold transition-colors">
              Watch Demo
            </button>
          </div>
        </div>
      </div>
      
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-indigo-500/30 rounded-full blur-[128px] -z-10" />
    </div>
  );
};

export default Hero;