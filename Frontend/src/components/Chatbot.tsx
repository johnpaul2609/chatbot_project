import { useState, useEffect, useRef } from 'react';
import { MessageCircle, X, Send, GraduationCap, BookOpen } from 'lucide-react';

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'bot';
  timestamp: Date;
  intent?: string;
  confidence?: number;
}

type ChatMode = 'selection' | 'admission' | 'academic';

interface ChatResponse {
  response: string;
  intent: string;
  confidence: number;
  suggestions?: string[];
}

// API Configuration
const API_BASE_URL = 'http://localhost:8000';

export function Chatbot() {
  const [isOpen, setIsOpen] = useState(false);
  const [mode, setMode] = useState<ChatMode>('selection');
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      text: "Hello! Welcome to St Lourdes Engineering College. Please select how I can assist you today:",
      sender: 'bot',
      timestamp: new Date()
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [backendStatus, setBackendStatus] = useState<'online' | 'offline' | 'checking'>('checking');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Generate or retrieve user ID
  const [userId] = useState(() => {
    const stored = localStorage.getItem('chatbot_user_id');
    if (stored) return stored;
    const newId = 'user_' + Math.random().toString(36).substr(2, 9);
    localStorage.setItem('chatbot_user_id', newId);
    return newId;
  });

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Check backend health on mount
  useEffect(() => {
    checkBackendHealth();
  }, []);

  // Load chat history when opened
  useEffect(() => {
    if (isOpen && backendStatus === 'online') {
      loadChatHistory();
    }
  }, [isOpen, backendStatus]);

  const checkBackendHealth = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/health`);
      const data = await response.json();
      setBackendStatus(data.status === 'healthy' ? 'online' : 'offline');
    } catch (error) {
      console.error('Backend health check failed:', error);
      setBackendStatus('offline');
    }
  };

  const loadChatHistory = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/chat/history/${userId}?limit=5`);
      if (response.ok) {
        const data = await response.json();
        if (data.conversations && data.conversations.length > 0) {
          const formattedMessages: Message[] = data.conversations
            .reverse()
            .flatMap((conv: any) => [
              {
                id: `user-${conv._id}`,
                text: conv.message,
                sender: 'user' as const,
                timestamp: new Date(conv.timestamp),
              },
              {
                id: `bot-${conv._id}`,
                text: conv.response,
                sender: 'bot' as const,
                timestamp: new Date(conv.timestamp),
                intent: conv.intent,
                confidence: conv.confidence,
              },
            ]);
          // Keep the welcome message and add history
          setMessages(prev => [...prev, ...formattedMessages]);
        }
      }
    } catch (error) {
      console.error('Error loading chat history:', error);
    }
  };

  const handleModeSelection = (selectedMode: 'admission' | 'academic') => {
    setMode(selectedMode);
    
    const userMessage: Message = {
      id: Date.now().toString(),
      text: selectedMode === 'admission' ? 'Admission Support' : 'Academic Support',
      sender: 'user',
      timestamp: new Date()
    };
    
    setMessages(prev => [...prev, userMessage]);
    
    // Send mode selection to backend
    const modeQuery = selectedMode === 'admission' 
      ? "I need help with admission-related queries"
      : "I need help with academic support";
    
    sendMessageToBackend(modeQuery);
  };

  const sendMessageToBackend = async (messageText: string) => {
    setIsLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/api/chat/message`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: messageText,
          user_id: userId,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to send message');
      }

      const data: ChatResponse = await response.json();

      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: data.response,
        sender: 'bot',
        timestamp: new Date(),
        intent: data.intent,
        confidence: data.confidence,
      };

      setMessages(prev => [...prev, botMessage]);
      setSuggestions(data.suggestions || []);

    } catch (error) {
      console.error('Error sending message:', error);
      
      // Fallback to local responses if backend is unavailable
      const fallbackMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: backendStatus === 'offline' 
          ? "I'm currently in offline mode. For the best experience, please ensure the backend server is running. Meanwhile, I can still help with basic information!"
          : getBotResponseFallback(messageText),
        sender: 'bot',
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, fallbackMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  // Fallback function for when backend is offline
  const getBotResponseFallback = (userMessage: string): string => {
    const lowerMessage = userMessage.toLowerCase();
    
    if (lowerMessage.includes('fee') || lowerMessage.includes('cost')) {
      return "For UG programs, tuition fees range from ₹70,000 to ₹85,000 per year. PG programs cost ₹60,000 per year. For detailed information, please contact our admissions office.";
    }
    if (lowerMessage.includes('admission') || lowerMessage.includes('apply')) {
      return "Admissions are based on TNEA counseling for Tamil Nadu students. Applications typically open in May. Would you like to know about eligibility criteria?";
    }
    if (lowerMessage.includes('placement')) {
      return "We have an 85% placement rate with an average package of 4.5 LPA. Top recruiters include TCS, Infosys, Wipro, Cognizant, and Amazon.";
    }
    if (lowerMessage.includes('course') || lowerMessage.includes('program')) {
      return "We offer UG programs in Computer Science, Electronics, Mechanical, and Civil Engineering. For PG, we have M.E. in CSE and VLSI Design.";
    }
    
    return "I'm here to help! Ask me about admissions, fees, programs, facilities, or placements. For the best experience, please ensure the backend server is running.";
  };

  const handleSendMessage = () => {
    if (inputValue.trim() === '') return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputValue,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    
    // Check if user wants to change mode
    if (inputValue.toLowerCase().includes('change mode') || 
        inputValue.toLowerCase().includes('switch mode') || 
        inputValue.toLowerCase().includes('go back')) {
      setMode('selection');
      setInputValue('');
      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: "Sure! Let me help you choose a support mode. Please select from the options above.",
        sender: 'bot',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, botMessage]);
      return;
    }

    const messageToSend = inputValue;
    setInputValue('');

    // Send to backend
    sendMessageToBackend(messageToSend);
  };

  const handleSuggestionClick = (suggestion: string) => {
    const userMessage: Message = {
      id: Date.now().toString(),
      text: suggestion,
      sender: 'user',
      timestamp: new Date()
    };
    setMessages(prev => [...prev, userMessage]);
    sendMessageToBackend(suggestion);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <>
      {/* Chat Button */}
      {!isOpen && (
        <button
          onClick={() => setIsOpen(true)}
          className="fixed bottom-6 right-6 bg-blue-600 hover:bg-blue-700 text-white rounded-full p-4 shadow-lg transition-all duration-300 hover:scale-110 z-50"
          aria-label="Open chat"
        >
          <MessageCircle className="w-6 h-6" />
        </button>
      )}

      {/* Chat Window */}
      {isOpen && (
        <div className="fixed bottom-6 right-6 w-96 max-h-[calc(100vh-3rem)] h-[600px] bg-white rounded-lg shadow-2xl flex flex-col z-50 border border-gray-200">
          {/* Header */}
          <div className="bg-blue-600 text-white p-4 rounded-t-lg flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="bg-white rounded-full p-2">
                <MessageCircle className="w-5 h-5 text-blue-600" />
              </div>
              <div>
                <h3 className="font-semibold">
                  {mode === 'admission' ? 'Admission Assistant' : mode === 'academic' ? 'Academic Assistant' : 'Support Assistant'}
                </h3>
                <p className="text-xs opacity-90 flex items-center gap-1">
                  {backendStatus === 'online' ? (
                    <>
                      <span className="inline-block w-2 h-2 bg-green-400 rounded-full"></span>
                      Online - AI Powered
                    </>
                  ) : backendStatus === 'offline' ? (
                    <>
                      <span className="inline-block w-2 h-2 bg-red-400 rounded-full"></span>
                      Offline Mode
                    </>
                  ) : (
                    'Connecting...'
                  )}
                </p>
              </div>
            </div>
            <button
              onClick={() => setIsOpen(false)}
              className="hover:bg-blue-700 rounded-full p-1 transition-colors"
              aria-label="Close chat"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[80%] rounded-lg p-3 ${
                    message.sender === 'user'
                      ? 'bg-blue-600 text-white rounded-br-none'
                      : 'bg-white text-gray-800 rounded-bl-none shadow-sm border border-gray-200'
                  }`}
                >
                  <p className="text-sm whitespace-pre-line">{message.text}</p>
                  <div className="flex items-center justify-between mt-1">
                    <p className={`text-xs ${message.sender === 'user' ? 'text-blue-100' : 'text-gray-500'}`}>
                      {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </p>
                    {message.confidence && backendStatus === 'online' && (
                      <p className="text-xs text-gray-400 ml-2">
                        {(message.confidence * 100).toFixed(0)}% confident
                      </p>
                    )}
                  </div>
                </div>
              </div>
            ))}
            
            {/* Loading indicator */}
            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-white rounded-lg p-3 shadow-sm border border-gray-200">
                  <div className="flex gap-1">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  </div>
                </div>
              </div>
            )}
            
            {/* Mode Selection Buttons */}
            {mode === 'selection' && (
              <div className="flex flex-col gap-3 mt-4">
                <button
                  onClick={() => handleModeSelection('admission')}
                  className="flex items-center gap-3 bg-white border-2 border-blue-600 text-gray-800 p-4 rounded-lg hover:bg-blue-50 transition-colors"
                >
                  <div className="bg-blue-600 text-white rounded-full p-2">
                    <GraduationCap className="w-5 h-5" />
                  </div>
                  <div className="text-left">
                    <div className="font-semibold text-blue-600">Admission Support</div>
                    <div className="text-xs text-gray-600">Ask about admissions, eligibility, fees, courses</div>
                  </div>
                </button>
                <button
                  onClick={() => handleModeSelection('academic')}
                  className="flex items-center gap-3 bg-white border-2 border-green-600 text-gray-800 p-4 rounded-lg hover:bg-green-50 transition-colors"
                >
                  <div className="bg-green-600 text-white rounded-full p-2">
                    <BookOpen className="w-5 h-5" />
                  </div>
                  <div className="text-left">
                    <div className="font-semibold text-green-600">Academic Support</div>
                    <div className="text-xs text-gray-600">Ask about curriculum, faculty, placements, exams</div>
                  </div>
                </button>
              </div>
            )}
            
            <div ref={messagesEndRef} />
          </div>

          {/* Suggestions */}
          {suggestions.length > 0 && mode !== 'selection' && (
            <div className="px-4 py-2 bg-white border-t border-gray-200">
              <p className="text-xs text-gray-500 mb-2">Quick questions:</p>
              <div className="flex flex-wrap gap-2">
                {suggestions.map((suggestion, index) => (
                  <button
                    key={index}
                    onClick={() => handleSuggestionClick(suggestion)}
                    className="text-xs bg-blue-50 hover:bg-blue-100 text-blue-700 px-3 py-1 rounded-full transition border border-blue-200"
                  >
                    {suggestion}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Input */}
          <div className="p-4 border-t border-gray-200 bg-white rounded-b-lg">
            {mode !== 'selection' && (
              <button
                onClick={() => {
                  setMode('selection');
                  const botMessage: Message = {
                    id: Date.now().toString(),
                    text: "Sure! Let me help you choose a support mode. Please select from the options above.",
                    sender: 'bot',
                    timestamp: new Date()
                  };
                  setMessages(prev => [...prev, botMessage]);
                }}
                className="text-xs text-blue-600 hover:text-blue-700 mb-2 flex items-center gap-1"
              >
                ← Change Support Mode
              </button>
            )}
            <div className="flex gap-2">
              <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder={mode === 'selection' ? 'Please select a mode above...' : 'Type your question...'}
                disabled={mode === 'selection' || isLoading}
                className="flex-1 border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm disabled:bg-gray-100 disabled:cursor-not-allowed"
              />
              <button
                onClick={handleSendMessage}
                disabled={mode === 'selection' || isLoading || !inputValue.trim()}
                className="bg-blue-600 hover:bg-blue-700 text-white rounded-lg px-4 py-2 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed"
                aria-label="Send message"
              >
                <Send className="w-5 h-5" />
              </button>
            </div>
            
            {/* Backend status warning */}
            {backendStatus === 'offline' && (
              <div className="mt-2 text-xs text-amber-600 bg-amber-50 px-3 py-2 rounded-lg">
                ⚠️ Backend offline. Using limited responses. Start the backend server for AI-powered responses.
              </div>
            )}
          </div>
        </div>
      )}
    </>
  );
}