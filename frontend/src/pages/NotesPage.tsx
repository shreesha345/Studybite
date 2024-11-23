import { useState, useEffect } from 'react';
import { BookOpen, Loader, ArrowLeft, MessageSquare, GraduationCap } from 'lucide-react';
import Markdown from 'markdown-to-jsx';
import { Link } from 'react-router-dom';

const MOTIVATIONAL_QUOTES = [
  "The expert in anything was once a beginner.",
  "Study hard what interests you the most in the most undisciplined, irreverent and original manner possible.",
  "The beautiful thing about learning is that no one can take it away from you.",
  "Education is not preparation for life; education is life itself.",
  "The more that you read, the more things you will know. The more that you learn, the more places you'll go."
];

// Add global styles to your CSS or Tailwind config
const globalStyles = `
  .glass-card {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
  }

  /* Custom scrollbar styles */
  ::-webkit-scrollbar {
    width: 8px;
    height: 8px;
  }

  ::-webkit-scrollbar-track {
    background: rgba(0, 0, 0, 0.1);
    border-radius: 4px;
  }

  ::-webkit-scrollbar-thumb {
    background: rgba(99, 102, 241, 0.5);
    border-radius: 4px;
  }

  ::-webkit-scrollbar-thumb:hover {
    background: rgba(99, 102, 241, 0.7);
  }
`;

const Sidebar = () => {
  return (
    <div className="w-64 bg-gray-800 p-4 flex flex-col min-h-screen">
      <div className="flex items-center space-x-2 mb-8">
        <GraduationCap className="h-8 w-8 text-indigo-500" />
        <span className="text-xl font-bold text-white">Studybite</span>
      </div>

      <nav className="flex-1">
        <Link
          to="/chat"
          className="flex items-center space-x-2 text-gray-400 hover:text-white transition-colors px-4 py-2 rounded-lg hover:bg-gray-700 mb-2"
        >
          <MessageSquare className="h-5 w-5" />
          <span>Chat</span>
        </Link>
        <Link
          to="/notes"
          className="flex items-center space-x-2 text-gray-400 hover:text-white transition-colors px-4 py-2 rounded-lg hover:bg-gray-700"
        >
          <BookOpen className="h-5 w-5" />
          <span>Create Notes</span>
        </Link>
      </nav>
    </div>
  );
};

interface MainContentProps {
  isProcessing: boolean;
  currentQuote: string;
  markdownContent: string;
  topic: string;
  error: string;
  handleBack: () => void;
  handleSubmit: (e: React.FormEvent<HTMLFormElement>) => void;
  setTopic: (topic: string) => void;
}

const MainContent: React.FC<MainContentProps> = ({
  isProcessing,
  currentQuote,
  markdownContent,
  topic,
  error,
  handleBack,
  handleSubmit,
  setTopic,
}) => {
  if (isProcessing) {
    return (
      <div className="flex-1 flex items-center justify-center p-8">
        <div className="max-w-2xl w-full text-center">
          <div className="animate-spin mb-8">
            <Loader className="h-12 w-12 text-indigo-500 mx-auto" />
          </div>
          <h2 className="text-2xl font-bold text-white mb-4">Generating Your Notes</h2>
          <p className="text-gray-400 text-lg italic">&ldquo;{currentQuote}&rdquo;</p>
        </div>
      </div>
    );
  }

  if (markdownContent) {
    return (
      <div className="flex-1 p-8 overflow-y-auto">
        <div className="max-w-4xl mx-auto">
          <button
            onClick={handleBack}
            className="flex items-center gap-2 text-gray-400 hover:text-white mb-6 transition-colors"
          >
            <ArrowLeft className="h-5 w-5" />
            Back to Search
          </button>
          <div className="glass-card rounded-lg p-8">
            <div className="mb-8">
              <h1 className="text-3xl font-bold text-white mb-4">Notes on: {topic}</h1>
              <div className="flex gap-4">
                <button
                  onClick={() => {
                    navigator.clipboard.writeText(markdownContent);
                  }}
                  className="text-sm bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg transition-colors"
                >
                  Copy to Clipboard
                </button>
                <button
                  onClick={() => {
                    const blob = new Blob([markdownContent], { type: 'text/markdown' });
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = `${topic.replace(/\s+/g, '-').toLowerCase()}-notes.md`;
                    document.body.appendChild(a);
                    a.click();
                    document.body.removeChild(a);
                    URL.revokeObjectURL(url);
                  }}
                  className="text-sm bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg transition-colors"
                >
                  Download Markdown
                </button>
              </div>
            </div>
            <div className="prose prose-invert max-w-none">
            <Markdown
                options={{
                  overrides: {
                    h1: { props: { className: 'text-3xl font-bold text-white mb-4 mt-8' } },
                    h2: { props: { className: 'text-2xl font-bold text-white mb-3 mt-6' } },
                    h3: { props: { className: 'text-xl font-bold text-white mb-2 mt-4' } },
                    p: { props: { className: 'text-gray-300 mb-4 leading-relaxed' } },
                    ul: { 
                      props: { 
                        className: 'text-gray-300 mb-4 space-y-2 list-none pl-0' 
                      } 
                    },
                    ol: { 
                      props: { 
                        className: 'text-gray-300 mb-4 space-y-2 list-none pl-0' 
                      } 
                    },
                    li: { 
                      props: { 
                        className: 'flex items-start gap-2 mb-1'
                      },
                      component: ({ children, ...props }) => (
                        <li {...props}>
                          <span className="text-gray-300 mt-1.5">•</span>
                          <span className="flex-1">{children}</span>
                        </li>
                      )
                    },
                    code: { props: { className: 'bg-gray-800 text-gray-300 px-1 rounded' } },
                    pre: { props: { className: 'bg-gray-800 p-4 rounded-lg mb-4 overflow-x-auto' } },
                    blockquote: { props: { className: 'border-l-4 border-indigo-500 pl-4 italic text-gray-400 mb-4' } },
                  },
                }}
              >
                {markdownContent}
              </Markdown>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 flex items-center justify-center p-8">
      <div className="w-full max-w-md glass-card rounded-lg p-8">
        <div className="flex flex-col items-center justify-center space-y-4 mb-8">
          <BookOpen className="h-16 w-16 text-indigo-500" />
          <h2 className="text-4xl font-bold text-white text-center">Create Study Notes</h2>
        </div>
        {error && (
          <div className="bg-red-500/10 border border-red-500/50 text-red-500 px-4 py-2 rounded-lg mb-4">
            {error}
          </div>
        )}
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            placeholder="Enter your topic..."
            className="w-full bg-gray-800/50 border border-gray-700 text-white px-4 py-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all placeholder-gray-500 mb-6"
            autoFocus
          />
          <button
            type="submit"
            className="w-full bg-indigo-600 hover:bg-indigo-700 text-white py-3 rounded-lg font-semibold transition-colors text-lg"
          >
            Generate Notes
          </button>
        </form>
      </div>
    </div>
  );
};

const NotesPage = () => {
  const [topic, setTopic] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [currentQuote, setCurrentQuote] = useState('');
  const [markdownContent, setMarkdownContent] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    // Add global styles
    const styleSheet = document.createElement('style');
    styleSheet.textContent = globalStyles;
    document.head.appendChild(styleSheet);

    return () => {
      document.head.removeChild(styleSheet);
    };
  }, []);

  useEffect(() => {
    if (isProcessing) {
      const interval = setInterval(() => {
        setCurrentQuote(MOTIVATIONAL_QUOTES[Math.floor(Math.random() * MOTIVATIONAL_QUOTES.length)]);
      }, 5000);
      return () => clearInterval(interval);
    }
  }, [isProcessing]);

  const handleBack = () => {
    setMarkdownContent('');
    setTopic('');
  };

  const checkStatus = async () => {
    try {
      const response = await fetch('https://4b9f-103-89-235-73.ngrok-free.app/status', {
        headers: { 'accept': 'application/json' }
      });
      const data = await response.json();
      
      if (data.status === 'completed') {
        const outputResponse = await fetch('https://4b9f-103-89-235-73.ngrok-free.app/output', {
          headers: { 'accept': 'application/json' }
        });
        const outputData = await outputResponse.json();
        setMarkdownContent(outputData.output);
        setIsProcessing(false);
      } else if (data.status === 'running') {
        setTimeout(checkStatus, 30000);
      }
    } catch (error) {
      setError('Failed to check status. Please try again.');
      setIsProcessing(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!topic.trim()) return;

    setIsProcessing(true);
    setError('');
    setCurrentQuote(MOTIVATIONAL_QUOTES[0]);
    setMarkdownContent('');

    try {
      const response = await fetch('https://4b9f-103-89-235-73.ngrok-free.app/process', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'accept': 'application/json'
        },
        body: JSON.stringify({ topic })
      });

      const data = await response.json();
      if (data.status === 'started') {
        setTimeout(checkStatus, 30000);
      }
    } catch (error) {
      setError('Failed to start processing. Please try again.');
      setIsProcessing(false);
    }
  };

  return (
    <div className="flex min-h-screen bg-gray-900">
      <Sidebar />
      <MainContent
        isProcessing={isProcessing}
        currentQuote={currentQuote}
        markdownContent={markdownContent}
        topic={topic}
        error={error}
        handleBack={handleBack}
        handleSubmit={handleSubmit}
        setTopic={setTopic}
      />
    </div>
  );
};

export default NotesPage;