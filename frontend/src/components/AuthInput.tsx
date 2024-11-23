import React from 'react';

interface AuthInputProps {
  icon: React.ReactNode;
  type: string;
  placeholder: string;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
}

const AuthInput: React.FC<AuthInputProps> = ({ icon, type, placeholder, value, onChange }) => {
  return (
    <div className="relative">
      <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
        {icon}
      </div>
      <input
        type={type}
        className="w-full bg-gray-900/50 border border-gray-700 text-white pl-10 pr-4 py-3 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all placeholder-gray-500"
        placeholder={placeholder}
        value={value}
        onChange={onChange}
        required
      />
    </div>
  );
};

export default AuthInput;