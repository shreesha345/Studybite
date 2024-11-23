import React, { useState } from 'react';

interface MCQFormProps {
  formContent: string;
  answerContent: string;
}

const MCQForm: React.FC<MCQFormProps> = ({ formContent, answerContent }) => {
  const [selectedAnswers, setSelectedAnswers] = useState<{ [key: string]: string }>({});
  const [showAnswers, setShowAnswers] = useState(false);
  
  // Extract correct answers from the answer content
  const getCorrectAnswer = (answerText: string) => {
    const match = answerText.match(/Correct Answer: ([A-D])/);
    return match ? match[1] : null;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setShowAnswers(true);
  };

  // Create a temporary div to parse HTML content
  const tempDiv = document.createElement('div');
  tempDiv.innerHTML = formContent;
  const forms = tempDiv.getElementsByTagName('form');
  
  return (
    <div className="space-y-4">
      {Array.from(forms).map((form, formIndex) => {
        const name = `mcq-${formIndex}`;
        const correctAnswer = getCorrectAnswer(answerContent);
        
        return (
          <form key={formIndex} onSubmit={handleSubmit} className="space-y-2">
            {Array.from(form.getElementsByTagName('div')).map((div, index) => {
              const value = div.textContent?.trim().charAt(0) || '';
              const text = div.textContent?.trim() || '';
              
              return (
                <div key={index} className="flex items-center space-x-2">
                  <input
                    type="radio"
                    id={`${name}-${index}`}
                    name={name}
                    value={value}
                    onChange={(e) => setSelectedAnswers(prev => ({
                      ...prev,
                      [name]: e.target.value
                    }))}
                    disabled={showAnswers}
                    className="form-radio h-4 w-4 text-indigo-600"
                  />
                  <label
                    htmlFor={`${name}-${index}`}
                    className={`${
                      showAnswers
                        ? value === correctAnswer
                          ? 'text-green-500'
                          : selectedAnswers[name] === value
                          ? 'text-red-500'
                          : 'text-gray-100'
                        : 'text-gray-100'
                    }`}
                  >
                    {text}
                  </label>
                </div>
              );
            })}
            {!showAnswers && (
              <button
                type="submit"
                className="mt-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
              >
                Submit
              </button>
            )}
            {showAnswers && (
              <div className="mt-2 text-green-500 font-medium">
                Correct Answer: {correctAnswer}
              </div>
            )}
          </form>
        );
      })}
    </div>
  );
};

export default MCQForm;