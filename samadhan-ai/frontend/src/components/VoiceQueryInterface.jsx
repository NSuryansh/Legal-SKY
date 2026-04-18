import React, { useState, useRef } from 'react';
import { Mic, MicOff, Loader, Send, Volume2 } from 'lucide-react';
import axios from 'axios';

const VoiceQueryInterface = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [conversations, setConversations] = useState([]);
  const [selectedLanguage, setSelectedLanguage] = useState('hi-IN');
  
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  // API base URL - works for both local and Databricks Apps
  const API_BASE_URL = import.meta.env.VITE_API_URL || '/api';

  const languages = [
    { code: 'hi-IN', name: 'Hindi (हिंदी)' },
    { code: 'bn-IN', name: 'Bengali (বাংলা)' },
    { code: 'te-IN', name: 'Telugu (తెలుగు)' },
    { code: 'mr-IN', name: 'Marathi (मराठी)' },
    { code: 'ta-IN', name: 'Tamil (தமிழ்)' },
    { code: 'gu-IN', name: 'Gujarati (ગુજરાતી)' },
    { code: 'kn-IN', name: 'Kannada (ಕನ್ನಡ)' },
    { code: 'ml-IN', name: 'Malayalam (മലയാളം)' },
    { code: 'pa-IN', name: 'Punjabi (ਪੰਜਾਬੀ)' },
  ];

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);
      audioChunksRef.current = [];

      mediaRecorderRef.current.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorderRef.current.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
        await processAudio(audioBlob);
        
        // Stop all tracks
        stream.getTracks().forEach(track => track.stop());
      };

      mediaRecorderRef.current.start();
      setIsRecording(true);
    } catch (error) {
      console.error('Error accessing microphone:', error);
      alert('Could not access microphone. Please grant permission.');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  const processAudio = async (audioBlob) => {
    setIsProcessing(true);
    
    try {
      // Convert Blob to Base64
      const reader = new FileReader();
      reader.readAsDataURL(audioBlob);
      
      reader.onloadend = async () => {
        const base64Audio = reader.result;
        // Strip the data:audio/webm;base64, prefix
        const base64String = base64Audio.split(',')[1];
        
        // Send to backend - uses relative path for Databricks Apps
        const response = await axios.post(`${API_BASE_URL}/process-audio`, {
          audio_data: base64String,
          language_code: selectedLanguage
        });

        // Add to conversations
        const newConversation = {
          id: Date.now(),
          timestamp: new Date().toLocaleTimeString(),
          regionalInput: response.data.regional_input,
          englishQuery: response.data.english_query,
          status: response.data.status
        };
        
        setConversations(prev => [...prev, newConversation]);
      };
    } catch (error) {
      console.error('Error processing audio:', error);
      const errorMsg = error.response?.data?.detail?.message || error.message;
      alert(`Failed to process audio: ${errorMsg}`);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="h-full flex flex-col">
      {/* Language Selector */}
      <div className="mb-6">
        <label className="block text-sm font-semibold text-slate-700 mb-2">
          Select Regional Language
        </label>
        <select
          value={selectedLanguage}
          onChange={(e) => setSelectedLanguage(e.target.value)}
          className="w-full md:w-64 px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 bg-white"
        >
          {languages.map((lang) => (
            <option key={lang.code} value={lang.code}>
              {lang.name}
            </option>
          ))}
        </select>
      </div>

      {/* Recording Interface */}
      <div className="card mb-6 bg-gradient-to-br from-primary-50 to-blue-50">
        <div className="text-center">
          <h3 className="text-xl font-bold text-slate-800 mb-4">
            Voice Query Interface
          </h3>
          <p className="text-slate-600 mb-6">
            Click the microphone to record your legal query in your regional language
          </p>

          {/* Microphone Button */}
          <div className="flex flex-col items-center">
            <button
              onClick={isRecording ? stopRecording : startRecording}
              disabled={isProcessing}
              className={`w-24 h-24 rounded-full flex items-center justify-center transition-all duration-300 shadow-2xl transform hover:scale-105 ${
                isRecording
                  ? 'bg-red-500 hover:bg-red-600 animate-pulse'
                  : 'bg-gradient-to-br from-primary-500 to-primary-700 hover:from-primary-600 hover:to-primary-800'
              } ${isProcessing ? 'opacity-50 cursor-not-allowed' : ''}`}
            >
              {isProcessing ? (
                <Loader className="w-12 h-12 text-white animate-spin" />
              ) : isRecording ? (
                <MicOff className="w-12 h-12 text-white" />
              ) : (
                <Mic className="w-12 h-12 text-white" />
              )}
            </button>

            <p className="mt-4 text-sm font-medium text-slate-700">
              {isProcessing
                ? 'Processing your query...'
                : isRecording
                ? 'Recording... Click to stop'
                : 'Click to start recording'}
            </p>
          </div>
        </div>
      </div>

      {/* Conversations Display */}
      <div className="flex-1 overflow-y-auto">
        <h3 className="text-lg font-bold text-slate-800 mb-4">
          Query History
        </h3>

        {conversations.length === 0 ? (
          <div className="card text-center py-12">
            <Volume2 className="w-16 h-16 text-slate-300 mx-auto mb-4" />
            <p className="text-slate-500">
              No queries yet. Start by recording your voice query above.
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            {conversations.map((conv) => (
              <div key={conv.id} className="card hover:shadow-lg transition-shadow">
                <div className="flex items-start justify-between mb-3">
                  <span className="text-xs text-slate-500">{conv.timestamp}</span>
                  <span className={`px-2 py-1 text-xs rounded-full ${
                    conv.status === 'success' 
                      ? 'bg-green-100 text-green-700' 
                      : 'bg-red-100 text-red-700'
                  }`}>
                    {conv.status}
                  </span>
                </div>

                {/* Regional Input */}
                <div className="mb-3 p-3 bg-primary-50 rounded-lg">
                  <p className="text-xs font-semibold text-primary-700 mb-1">
                    Regional Input:
                  </p>
                  <p className="text-slate-800 text-lg">
                    {conv.regionalInput}
                  </p>
                </div>

                {/* English Translation */}
                <div className="p-3 bg-slate-50 rounded-lg">
                  <p className="text-xs font-semibold text-slate-700 mb-1">
                    English Translation:
                  </p>
                  <p className="text-slate-800">
                    {conv.englishQuery}
                  </p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default VoiceQueryInterface;