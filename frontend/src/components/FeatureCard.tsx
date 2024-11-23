import React from 'react';

interface FeatureCardProps {
  icon: React.ReactNode;
  title: string;
  description: string;
}

const FeatureCard: React.FC<FeatureCardProps> = ({ icon, title, description }) => {
  return (
    <div className="bg-gray-800/50 backdrop-blur-lg rounded-xl p-8 hover:bg-gray-800/70 transition-all duration-300 border border-gray-700/50">
      <div className="bg-indigo-600/20 rounded-lg p-3 w-fit mb-6">
        {icon}
      </div>
      <h3 className="text-xl font-semibold mb-4">{title}</h3>
      <p className="text-gray-400">{description}</p>
    </div>
  );
};

export default FeatureCard;