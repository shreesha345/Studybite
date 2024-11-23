import React from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';
import Hero from '../components/Hero';
import Features from '../components/Features';

const LandingPage = () => {
  const navigate = useNavigate();

  const handleAuthNavigation = (type: 'login' | 'signup') => {
    navigate('/auth', { state: { isLogin: type === 'login' } });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-white">
      <Navbar onLogin={() => handleAuthNavigation('login')} onSignup={() => handleAuthNavigation('signup')} />
      <div className="pt-16">
        <Hero />
        <Features />
      </div>
    </div>
  );
};

export default LandingPage;