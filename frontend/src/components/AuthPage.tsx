import React, { useState, useEffect } from 'react';
import { Mail, Lock, User, ArrowRight } from 'lucide-react';
import { useLocation, useNavigate } from 'react-router-dom';
import AuthInput from './AuthInput';

interface UserData {
  fullName?: string;
  email: string;
  password: string;
}

const AuthPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState<UserData>({
    fullName: '',
    email: '',
    password: '',
  });
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  
  useEffect(() => {
    if (location.state?.isLogin !== undefined) {
      setIsLogin(location.state.isLogin);
    }
  }, [location]);

  const handleInputChange = (field: keyof UserData | 'confirmPassword', value: string) => {
    if (field === 'confirmPassword') {
      setConfirmPassword(value);
    } else {
      setFormData(prev => ({ ...prev, [field]: value }));
    }
    setError('');
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.email || !formData.password) {
      setError('Please fill in all required fields');
      return;
    }

    if (isLogin) {
      // Handle Login
      const users = JSON.parse(localStorage.getItem('users') || '[]');
      const user = users.find((u: UserData) => u.email === formData.email);
      
      if (!user || user.password !== formData.password) {
        setError('Invalid email or password');
        return;
      }
      
      localStorage.setItem('currentUser', JSON.stringify(user));
      navigate('/chat');
    } else {
      // Handle Sign Up
      if (!formData.fullName) {
        setError('Please enter your full name');
        return;
      }
      
      if (formData.password !== confirmPassword) {
        setError('Passwords do not match');
        return;
      }
      
      const users = JSON.parse(localStorage.getItem('users') || '[]');
      if (users.some((u: UserData) => u.email === formData.email)) {
        setError('Email already exists');
        return;
      }
      
      users.push(formData);
      localStorage.setItem('users', JSON.stringify(users));
      localStorage.setItem('currentUser', JSON.stringify(formData));
      navigate('/chat');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-white flex items-center justify-center px-4">
      <div className="absolute top-6 left-6">
        <button
          onClick={() => navigate('/')}
          className="text-gray-400 hover:text-white transition-colors"
        >
          ← Back to Home
        </button>
      </div>

      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-indigo-500/20 rounded-full blur-[120px] -z-10" />
      
      <div className="w-full max-w-md">
        <div className="bg-gray-800/50 backdrop-blur-lg rounded-2xl p-8 shadow-xl border border-gray-700/50">
          <h2 className="text-2xl font-bold text-center mb-2">
            {isLogin ? 'Welcome Back' : 'Create Account'}
          </h2>
          <p className="text-gray-400 text-center mb-8">
            {isLogin 
              ? 'Enter your credentials to access your account' 
              : 'Sign up to start your learning journey'}
          </p>
          
          {error && (
            <div className="bg-red-500/10 border border-red-500/50 text-red-500 px-4 py-2 rounded-lg mb-4">
              {error}
            </div>
          )}
          
          <form onSubmit={handleSubmit} className="space-y-4">
            {!isLogin && (
              <AuthInput
                icon={<User className="w-5 h-5 text-gray-500" />}
                type="text"
                placeholder="Full Name"
                value={formData.fullName || ''}
                onChange={(e) => handleInputChange('fullName', e.target.value)}
              />
            )}
            
            <AuthInput
              icon={<Mail className="w-5 h-5 text-gray-500" />}
              type="email"
              placeholder="Email Address"
              value={formData.email}
              onChange={(e) => handleInputChange('email', e.target.value)}
            />
            
            <AuthInput
              icon={<Lock className="w-5 h-5 text-gray-500" />}
              type="password"
              placeholder="Password"
              value={formData.password}
              onChange={(e) => handleInputChange('password', e.target.value)}
            />
            
            {!isLogin && (
              <AuthInput
                icon={<Lock className="w-5 h-5 text-gray-500" />}
                type="password"
                placeholder="Confirm Password"
                value={confirmPassword}
                onChange={(e) => handleInputChange('confirmPassword', e.target.value)}
              />
            )}
            
            <button 
              type="submit"
              className="w-full bg-indigo-600 hover:bg-indigo-700 text-white py-3 rounded-lg font-semibold transition-all flex items-center justify-center group"
            >
              {isLogin ? 'Sign In' : 'Create Account'}
              <ArrowRight className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" />
            </button>
          </form>
          
          <p className="text-gray-400 text-center mt-6">
            {isLogin ? "Don't have an account?" : "Already have an account?"}
            <button
              onClick={() => setIsLogin(!isLogin)}
              className="text-indigo-400 hover:text-indigo-300 font-semibold ml-2"
            >
              {isLogin ? 'Sign Up' : 'Sign In'}
            </button>
          </p>
        </div>
      </div>
    </div>
  );
};

export default AuthPage;