import React from 'react';
import { Bot, Brain, Languages } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import FeatureCard from './FeatureCard';

const Features = () => {
  const navigate = useNavigate();

  const features = [
    {
      icon: <Bot className="w-6 h-6 text-indigo-400" />,
      title: "AI Study Assistant",
      description: "Get instant answers to your questions and personalized study recommendations powered by advanced AI."
    },
    {
      icon: <Brain className="w-6 h-6 text-indigo-400" />,
      title: "Smart Note Creation",
      description: "Transform your lecture recordings into structured notes with our AI-powered transcription and summarization."
    },
    {
      icon: <Languages className="w-6 h-6 text-indigo-400" />,
      title: "Video Translation",
      description: "Break language barriers with real-time video translations in multiple languages for global learning."
    }
  ];

  const handleStartLearning = () => {
    navigate('/auth', { state: { isLogin: false } });
  };

  return (
    <section id="features" className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 scroll-mt-16">
      <div className="text-center mb-16">
        <h2 className="text-3xl md:text-4xl font-bold mb-4">
          Supercharge Your Learning
        </h2>
        <p className="text-gray-400 max-w-2xl mx-auto">
          Our cutting-edge features are designed to transform how you learn, making education more accessible and effective than ever.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {features.map((feature, index) => (
          <FeatureCard
            key={index}
            icon={feature.icon}
            title={feature.title}
            description={feature.description}
          />
        ))}
      </div>

      <div className="mt-16 text-center">
        <button 
          onClick={handleStartLearning}
          className="bg-indigo-600 hover:bg-indigo-700 text-white px-8 py-4 rounded-lg font-semibold inline-flex items-center"
        >
          Start Learning Now
        </button>
      </div>
    </section>
  );
};

export default Features;