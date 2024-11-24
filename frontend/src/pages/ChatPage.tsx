import React, { useState, useEffect, useRef } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { GraduationCap, Send, Trash2, BookOpen, MessageSquare, Video } from 'lucide-react';
import { parseMessage } from '../utils/messageParser';

interface Message {
  content: string;
  isUser: boolean;
}

const ChatPage = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const navigate = useNavigate();
  const userRef = useRef(JSON.parse(localStorage.getItem('currentUser') || '{}'));

  useEffect(() => {
    if (!userRef.current?.email) {
      navigate('/auth');
      return;
    }
    
    setMessages([{
      content: "Hello! I'm your AI study assistant. How can I help you today?",
      isUser: false
    }]);
  }, [navigate]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return;

    const newMessage = {
      content: inputMessage,
      isUser: true
    };

    setMessages(prev => [...prev, newMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await fetch(
        `http://localhost:8001/chat/${userRef.current.email}`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'accept': 'application/json'
          },
          body: JSON.stringify({ message: inputMessage })
        }
      );

      const data = await response.json();
      
      setMessages(prev => [...prev, {
        content: data.response,
        isUser: false
      }]);
    } catch (error) {
      setMessages(prev => [...prev, {
        content: "Sorry, I'm having trouble connecting. Please try again.",
        isUser: false
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleClearChat = async () => {
    try {
      await fetch(
        `http://localhost:8001/clear_history/${userRef.current.email}`,
        {
          method: 'POST',
          headers: {
            'accept': 'application/json'
          }
        }
      );
      
      setMessages([{
        content: "Chat history cleared. How can I help you?",
        isUser: false
      }]);
    } catch (error) {
      console.error('Error clearing chat:', error);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="flex h-screen bg-gray-900">
      {/* Sidebar */}
      <div className="w-64 bg-gray-800 p-4 flex flex-col">
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

        <button
          onClick={handleClearChat}
          className="mt-auto flex items-center space-x-2 text-gray-400 hover:text-white transition-colors px-4 py-2 rounded-lg hover:bg-gray-700"
        >
          <Trash2 className="h-5 w-5" />
          <span>Clear Chat</span>
        </button>
      </div>

      {/* Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`flex ${message.isUser ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[80%] p-4 rounded-lg ${
                  message.isUser
                    ? 'bg-indigo-600 text-white'
                    : 'bg-gray-800 text-gray-100'
                }`}
              >
                {message.isUser ? message.content : parseMessage(message.content)}
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="flex justify-start">
              <div className="bg-gray-800 text-gray-100 p-4 rounded-lg">
                Thinking...
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="border-t border-gray-800 p-4">
          <div className="flex space-x-4">
            <textarea
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your message..."
              className="flex-1 bg-gray-800 text-white rounded-lg p-3 resize-none focus:ring-2 focus:ring-indigo-500 focus:outline-none"
              rows={1}
            />
            <button
              onClick={handleSendMessage}
              disabled={isLoading || !inputMessage.trim()}
              className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg flex items-center justify-center disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <Send className="h-5 w-5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatPage;
