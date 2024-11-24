import React, { useState, useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import { GraduationCap, Video, MessageSquare, BookOpen, Download } from 'lucide-react';

// TypeScript interfaces
interface Language {
  name: string;
  code: string;
}

interface FormData {
  url: string;
  topic: string;
  languageCode: string;
}

interface ProcessingResponse {
  message: string;
  files: string[];
}

// Language options array
const languages: Language[] = [
  { name: "English", code: "en" },
  { name: "Japanese", code: "ja" },
  { name: "Chinese", code: "zh" },
  { name: "German", code: "de" },
  { name: "Hindi", code: "hi" },
  { name: "French", code: "fr" },
  { name: "Korean", code: "ko" },
  { name: "Portuguese", code: "pt" },
  { name: "Italian", code: "it" },
  { name: "Spanish", code: "es" },
  { name: "Indonesian", code: "id" },
  { name: "Dutch", code: "nl" },
  { name: "Turkish", code: "tr" },
  { name: "Filipino", code: "tl" },
  { name: "Polish", code: "pl" },
  { name: "Swedish", code: "sv" },
  { name: "Bulgarian", code: "bg" },
  { name: "Romanian", code: "ro" },
  { name: "Arabic", code: "ar" },
  { name: "Czech", code: "cs" },
  { name: "Greek", code: "el" },
  { name: "Finnish", code: "fi" },
  { name: "Croatian", code: "hr" },
  { name: "Malay", code: "ms" },
  { name: "Slovak", code: "sk" },
  { name: "Danish", code: "da" },
  { name: "Tamil", code: "ta" },
  { name: "Ukrainian", code: "uk" },
  { name: "Russian", code: "ru" }
];

// Snake Game Component
const LoadingGame: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 });
  const snakePos = useRef({ x: 0, y: 0 });
  const speed = 5;

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // Update snake position
      const dx = mousePos.x - snakePos.current.x;
      const dy = mousePos.y - snakePos.current.y;
      const distance = Math.sqrt(dx * dx + dy * dy);
      
      if (distance > 0) {
        snakePos.current.x += (dx / distance) * speed;
        snakePos.current.y += (dy / distance) * speed;
      }

      // Draw snake
      ctx.beginPath();
      ctx.arc(snakePos.current.x, snakePos.current.y, 10, 0, Math.PI * 2);
      ctx.fillStyle = '#4F46E5';
      ctx.fill();

      // Draw mouse cursor target
      ctx.beginPath();
      ctx.arc(mousePos.x, mousePos.y, 5, 0, Math.PI * 2);
      ctx.fillStyle = '#EF4444';
      ctx.fill();

      requestAnimationFrame(animate);
    };

    animate();
  }, [mousePos]);

  const handleMouseMove = (e: React.MouseEvent<HTMLCanvasElement>) => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const rect = canvas.getBoundingClientRect();
    setMousePos({
      x: e.clientX - rect.left,
      y: e.clientY - rect.top,
    });
  };

  return (
    <canvas
      ref={canvasRef}
      width={400}
      height={300}
      onMouseMove={handleMouseMove}
      className="bg-gray-800 rounded-lg"
    />
  );
};

// Sidebar component
const Sidebar: React.FC = () => {
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
          className="flex items-center space-x-2 text-gray-400 hover:text-white transition-colors px-4 py-2 rounded-lg hover:bg-gray-700 mb-2"
        >
          <BookOpen className="h-5 w-5" />
          <span>Create Notes</span>
        </Link>
        <Link
          to="/video"
          className="flex items-center space-x-2 text-gray-400 hover:text-white transition-colors px-4 py-2 rounded-lg hover:bg-gray-700"
        >
          <Video className="h-5 w-5" />
          <span>Video Translate</span>
        </Link>
      </nav>
    </div>
  );
};

const VideoTrans: React.FC = () => {
  // State management
  const [formData, setFormData] = useState<FormData>({
    url: '',
    topic: '',
    languageCode: 'en'
  });
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>('');
  const [videos, setVideos] = useState<string[]>([]);

  // Handle form submission
  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');
    setVideos([]);

    try {
      const response = await fetch('http://localhost:8000/process-video', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error('Video processing failed');
      }

      const data: ProcessingResponse = await response.json();
      console.log('Processing successful:', data);
      setVideos(data.files);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDownload = async (filename: string) => {
    try {
      const response = await fetch(`http://localhost:8000/download-video/${filename}`);
      if (!response.ok) throw new Error('Download failed');
      
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Download failed');
    }
  };

  // Handle input changes
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  return (
    <div className="flex min-h-screen bg-gray-900">
      <Sidebar />
      <div className="flex-1 p-8">
        <div className="max-w-4xl mx-auto">
          <div className="bg-gray-800/50 backdrop-blur-lg border border-gray-700 rounded-lg p-8">
            <div className="flex flex-col items-center justify-center space-y-4 mb-8">
              <Video className="h-16 w-16 text-indigo-500" />
              <h2 className="text-4xl font-bold text-white text-center">Video Translation</h2>
              {error && (
                <div className="w-full bg-red-500/10 border border-red-500/50 text-red-500 px-4 py-2 rounded-lg">
                  {error}
                </div>
              )}
            </div>

            <form onSubmit={handleSubmit} className="space-y-6 mb-8">
              {/* Video URL Input */}
              <div>
                <label htmlFor="url" className="block text-sm font-medium text-gray-300 mb-2">
                  Video URL
                </label>
                <input
                  type="url"
                  id="url"
                  name="url"
                  value={formData.url}
                  onChange={handleInputChange}
                  className="w-full bg-gray-700 border border-gray-600 text-white px-4 py-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
                  placeholder="Enter video URL..."
                  required
                />
              </div>

              {/* Topic Input */}
              <div>
                <label htmlFor="topic" className="block text-sm font-medium text-gray-300 mb-2">
                  Video Topic
                </label>
                <input
                  type="text"
                  id="topic"
                  name="topic"
                  value={formData.topic}
                  onChange={handleInputChange}
                  className="w-full bg-gray-700 border border-gray-600 text-white px-4 py-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
                  placeholder="What would you like to learn from this video?"
                  required
                />
              </div>

              {/* Language Selection Dropdown */}
              <div>
                <label htmlFor="languageCode" className="block text-sm font-medium text-gray-300 mb-2">
                  Target Language
                </label>
                <select
                  id="languageCode"
                  name="languageCode"
                  value={formData.languageCode}
                  onChange={handleInputChange}
                  className="w-full bg-gray-700 border border-gray-600 text-white px-4 py-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
                  required
                >
                  {languages.map((lang) => (
                    <option key={lang.code} value={lang.code}>
                      {lang.name}
                    </option>
                  ))}
                </select>
              </div>

              {/* Submit Button */}
              <button
                type="submit"
                disabled={isLoading}
                className="w-full bg-indigo-600 hover:bg-indigo-700 text-white py-3 rounded-lg font-semibold transition-colors text-lg disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isLoading ? 'Processing...' : 'Translate Video'}
              </button>
            </form>

            {/* Loading Game */}
            {isLoading && (
              <div className="flex flex-col items-center space-y-4 my-8">
                <h3 className="text-xl font-semibold text-white">Processing Your Video</h3>
                <p className="text-gray-400">Try to catch the dot while you wait!</p>
                <LoadingGame />
              </div>
            )}

            {/* Video Results */}
            {videos.length > 0 && (
              <div className="space-y-6">
                <h3 className="text-xl font-semibold text-white mb-4">Processed Videos</h3>
                <div className="grid gap-6">
                  {videos.map((filename, index) => (
                    <div key={filename} className="bg-gray-800 rounded-lg p-4">
                      <h4 className="text-white font-medium mb-4">Clip {index + 1}</h4>
                      <video 
                        controls 
                        className="w-full rounded-lg mb-4"
                        src={`http://localhost:8000/download-video/${filename}`}
                      />
                      <button
                        onClick={() => handleDownload(filename)}
                        className="flex items-center space-x-2 bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg transition-colors"
                      >
                        <Download className="h-4 w-4" />
                        <span>Download</span>
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default VideoTrans;