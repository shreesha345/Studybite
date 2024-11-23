import React, { useState } from 'react';

interface MCQFormProps {
  formContent: string;
  answerContent: string;
}

const MCQForm: React.FC<MCQFormProps> = ({ formContent, answerContent }) => {
  const [selectedAnswer, setSelectedAnswer] = useState<string>('');
  const [showAnswer, setShowAnswer] = useState(false);

  // Extract correct answer value from answerContent
  const getCorrectAnswer = () => {
    const valueMatch = answerContent.match(/<value>(.*?)<\/value>/);
    return valueMatch ? valueMatch[1] : '';
  };

  // Parse options from form content
  const parseOptions = () => {
    const parser = new DOMParser();
    const doc = parser.parseFromString(formContent, 'text/html');
    const options: { value: string; label: string }[] = [];
    
    // Get all div elements inside the form
    const divs = doc.querySelectorAll('form div');
    divs.forEach(div => {
      const input = div.querySelector('input');
      if (input && input.hasAttribute('value')) {
        options.push({
          value: input.getAttribute('value') || '',
          label: div.textContent?.trim() || ''
        });
      }
    });

    return options;
  };

  // Get question text
  const getQuestion = () => {
    const parser = new DOMParser();
    const doc = parser.parseFromString(formContent, 'text/html');
    const form = doc.querySelector('form');
    if (form && form.previousSibling) {
      return form.previousSibling.textContent?.trim() || '';
    }
    return '';
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setShowAnswer(true);
  };

  const correctAnswer = getCorrectAnswer();
  const options = parseOptions();
  const question = getQuestion();

  return (
    <div className="bg-gray-800 rounded-lg p-4 space-y-4">
      {/* Question */}
      <div className="text-gray-100 font-medium">{question}</div>

      {/* MCQ Options */}
      <form onSubmit={handleSubmit} className="space-y-3">
        {options.map((option, index) => (
          <div key={index} className="flex items-center space-x-3">
            <input
              type="radio"
              id={`option-${index}`}
              name="mcq-option"
              value={option.value}
              onChange={(e) => setSelectedAnswer(e.target.value)}
              disabled={showAnswer}
              className="form-radio h-4 w-4 text-indigo-600 focus:ring-indigo-500"
            />
            <label
              htmlFor={`option-${index}`}
              className={`
                ${showAnswer && option.value === correctAnswer ? 'text-green-500' : ''}
                ${showAnswer && option.value === selectedAnswer && option.value !== correctAnswer ? 'text-red-500' : ''}
                ${!showAnswer ? 'text-gray-100' : ''}
                cursor-pointer
              `}
            >
              {option.label}
            </label>
          </div>
        ))}

        {/* Submit Button */}
        {!showAnswer && (
          <button
            type="submit"
            disabled={!selectedAnswer}
            className="mt-4 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            Submit Answer
          </button>
        )}

        {/* Answer Display */}
        {showAnswer && (
          <div className="mt-4">
            <div className="text-green-500">
              Correct Answer: {options.find(opt => opt.value === correctAnswer)?.label}
            </div>
          </div>
        )}
      </form>
    </div>
  );
};

export default MCQForm;
