import React, { useState, useEffect } from 'react';
import { GraduationCap } from 'lucide-react';

interface NavbarProps {
  onLogin: () => void;
  onSignup: () => void;
}

const Navbar: React.FC<NavbarProps> = ({ onLogin, onSignup }) => {
  const [prevScrollPos, setPrevScrollPos] = useState(0);
  const [visible, setVisible] = useState(true);

  const scrollToFeatures = () => {
    const featuresSection = document.getElementById('features');
    if (featuresSection) {
      featuresSection.scrollIntoView({ behavior: 'smooth' });
    }
  };

  useEffect(() => {
    const handleScroll = () => {
      const currentScrollPos = window.scrollY;
      setVisible(prevScrollPos > currentScrollPos || currentScrollPos < 10);
      setPrevScrollPos(currentScrollPos);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, [prevScrollPos]);

  return (
    <nav className={`bg-gray-900/50 backdrop-blur-md border-b border-gray-800 fixed w-full z-50 transition-transform duration-300 ${visible ? 'translate-y-0' : '-translate-y-full'}`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center cursor-pointer">
            <GraduationCap className="h-8 w-8 text-indigo-500" />
            <span className="ml-2 text-xl font-bold">Studybite</span>
          </div>
          
          <div className="hidden md:block">
            <div className="ml-10 flex items-baseline space-x-4">
              <button 
                onClick={scrollToFeatures}
                className="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium"
              >
                Features
              </button>
              <a href="#about" className="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium">About</a>
            </div>
          </div>
          
          <div className="flex items-center">
            <button 
              onClick={onLogin}
              className="bg-transparent hover:bg-gray-800 text-white px-4 py-2 rounded-lg mr-4 transition-colors"
            >
              Login
            </button>
            <button 
              onClick={onSignup}
              className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg transition-colors"
            >
              Sign Up
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;