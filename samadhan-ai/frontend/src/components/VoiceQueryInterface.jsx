import React, { useState, useRef } from 'react';
import { Mic, MicOff, Loader, Volume2, FileText, AlertCircle, CheckCircle } from 'lucide-react';
import axios from 'axios';

const VoiceQueryInterface = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [conversations, setConversations] = useState([]);
  const [selectedLanguage, setSelectedLanguage] = useState('hi-IN');
  const [currentStep, setCurrentStep] = useState('');
  const [textQuery, setTextQuery] = useState('');

  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  // API base URL - works for both local and Databricks Apps
  const API_BASE_URL = import.meta.env.VITE_API_URL || '/api';

  // Configure axios for Databricks Apps authentication
  React.useEffect(() => {
    axios.defaults.withCredentials = true;
  }, []);

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
      const reader = new FileReader();
      reader.readAsDataURL(audioBlob);

      reader.onloadend = async () => {
        try {
          const base64Audio = reader.result;
          const base64String = base64Audio.split(',')[1];

          setCurrentStep('Processing your legal query...');

          const response = await axios.post(
            `${API_BASE_URL}/legal-query`,
            { audio_data: base64String },
            { withCredentials: true }
          );

          console.log('Legal query response:', response.data);

          if (response.data.success) {
            const newConversation = {
              id: Date.now(),
              timestamp: new Date().toLocaleTimeString(),
              detectedLanguage: response.data.detected_language,
              regionalInput: response.data.regional_input,
              englishQuery: response.data.english_query,
              legalAnswer: response.data.legal_answer,
              intents: response.data.intents || [],
              intentScores: response.data.intent_scores || {},
              sources: response.data.sources || [],
              actionPack: response.data.action_pack,
              status: response.data.status
            };

            setConversations(prev => [newConversation, ...prev]);
          } else {
            const errorConversation = {
              id: Date.now(),
              timestamp: new Date().toLocaleTimeString(),
              regionalInput: response.data.regional_input || 'N/A',
              englishQuery: response.data.english_query || 'N/A',
              error: response.data.error || response.data.message || 'Unknown error',
              status: 'error'
            };

            setConversations(prev => [errorConversation, ...prev]);
          }
        } catch (error) {
          console.error('Error processing audio:', error);

          const errorMsg =
            error.response?.data?.message ||
            error.response?.data?.error ||
            error.message;

          const errorConversation = {
            id: Date.now(),
            timestamp: new Date().toLocaleTimeString(),
            error: `Failed to process: ${errorMsg}`,
            status: 'error'
          };

          setConversations(prev => [errorConversation, ...prev]);
        } finally {
          setCurrentStep('');
          setIsProcessing(false);
        }
      };
    } catch (error) {
      console.error('Error preparing audio:', error);
      setCurrentStep('');
      setIsProcessing(false);
    }
  };

  const handleTextSubmit = async () => {
    if (!textQuery.trim()) return;

    setIsProcessing(true);
    setCurrentStep('Processing your text query...');

    try {
      const response = await axios.post(
        `${API_BASE_URL}/legal-query`,
        {
          query: textQuery,
          language: selectedLanguage
        },
        { withCredentials: true }
      );

      console.log('Legal text query response:', response.data);

      if (response.data.success) {
        const newConversation = {
          id: Date.now(),
          timestamp: new Date().toLocaleTimeString(),
          detectedLanguage: response.data.detected_language,
          regionalInput: response.data.regional_input || textQuery,
          englishQuery: response.data.english_query,
          legalAnswer: response.data.legal_answer,
          intents: response.data.intents || [],
          intentScores: response.data.intent_scores || {},
          sources: response.data.sources || [],
          actionPack: response.data.action_pack,
          status: response.data.status
        };

        setConversations(prev => [newConversation, ...prev]);
        setTextQuery('');
      } else {
        const errorConversation = {
          id: Date.now(),
          timestamp: new Date().toLocaleTimeString(),
          regionalInput: textQuery,
          englishQuery: response.data.english_query || 'N/A',
          error: response.data.error || response.data.message || 'Unknown error',
          status: 'error'
        };

        setConversations(prev => [errorConversation, ...prev]);
      }
    } catch (error) {
      console.error('Error processing text query:', error);

      const errorMsg =
        error.response?.data?.message ||
        error.response?.data?.error ||
        error.message;

      const errorConversation = {
        id: Date.now(),
        timestamp: new Date().toLocaleTimeString(),
        regionalInput: textQuery,
        englishQuery: 'N/A',
        error: `Failed to process: ${errorMsg}`,
        status: 'error'
      };

      setConversations(prev => [errorConversation, ...prev]);
    } finally {
      setIsProcessing(false);
      setCurrentStep('');
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

      {/* Text Query Input */}
      <div className="card mb-6">
        <div className="text-center">
          <h3 className="text-xl font-bold text-slate-800 mb-4">
            Text Query Interface
          </h3>
          <p className="text-slate-600 mb-6">
            Type your legal query here instead of recording
          </p>

          <div className="flex flex-col md:flex-row gap-3">
            <input
              type="text"
              value={textQuery}
              onChange={(e) => setTextQuery(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter') handleTextSubmit();
              }}
              placeholder="Type your legal query..."
              disabled={isProcessing}
              className="flex-1 px-4 py-3 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 bg-white"
            />

            <button
              onClick={handleTextSubmit}
              disabled={isProcessing || !textQuery.trim()}
              className="px-6 py-3 bg-gradient-to-br from-primary-500 to-primary-700 hover:from-primary-600 hover:to-primary-800 text-white font-semibold rounded-lg disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isProcessing ? 'Processing...' : 'Send'}
            </button>
          </div>
        </div>
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
              {currentStep || (isProcessing
                ? 'Processing your query...'
                : isRecording
                ? 'Recording... Click to stop'
                : 'Click to start recording')}
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
          <div className="space-y-6">
            {conversations.map((conv) => (
              <div key={conv.id} className="card hover:shadow-lg transition-shadow">
                {/* Header */}
                <div className="flex items-start justify-between mb-4 pb-3 border-b border-slate-200">
                  <span className="text-xs text-slate-500">{conv.timestamp}</span>
                  <span className={`px-3 py-1 text-xs font-semibold rounded-full ${
                    conv.status === 'complete'
                      ? 'bg-green-100 text-green-700'
                      : conv.status === 'error'
                      ? 'bg-red-100 text-red-700'
                      : 'bg-blue-100 text-blue-700'
                  }`}>
                    {conv.status === 'complete' ? '✓ Complete' : conv.status === 'error' ? '✗ Error' : conv.status}
                  </span>
                </div>

                {/* Error Display */}
                {conv.error && (
                  <div className="mb-3 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start gap-3">
                    <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
                    <div>
                      <p className="text-sm font-semibold text-red-800 mb-1">Error:</p>
                      <p className="text-sm text-red-700">{conv.error}</p>
                    </div>
                  </div>
                )}

                {/* Regional Input */}
                {conv.regionalInput && (
                  <div className="mb-3 p-3 bg-primary-50 rounded-lg">
                    <p className="text-xs font-semibold text-primary-700 mb-1 flex items-center gap-1">
                      <Volume2 className="w-3 h-3" />
                      Your Query ({conv.detectedLanguage || 'Regional'}):
                    </p>
                    <p className="text-slate-800 text-lg font-medium">
                      {conv.regionalInput}
                    </p>
                  </div>
                )}

                {/* English Translation */}
                {conv.englishQuery && (
                  <div className="mb-3 p-3 bg-slate-50 rounded-lg">
                    <p className="text-xs font-semibold text-slate-700 mb-1">
                      English Translation:
                    </p>
                    <p className="text-slate-700">
                      {conv.englishQuery}
                    </p>
                  </div>
                )}

                {/* Legal Answer */}
                {conv.legalAnswer && (
                  <div className="mb-3 p-4 bg-gradient-to-br from-green-50 to-emerald-50 border border-green-200 rounded-lg">
                    <div className="flex items-center gap-2 mb-3">
                      <CheckCircle className="w-5 h-5 text-green-600" />
                      <p className="text-sm font-bold text-green-800">
                        Legal Answer:
                      </p>
                    </div>
                    <div className="prose prose-sm max-w-none">
                      <p className="text-slate-800 whitespace-pre-wrap leading-relaxed">
                        {conv.legalAnswer}
                      </p>
                    </div>
                  </div>
                )}

                {/* Intent Scores */}
                {conv.intents && conv.intents.length > 0 && (
                  <div className="mb-3 p-3 bg-blue-50 rounded-lg">
                    <p className="text-xs font-semibold text-blue-700 mb-2">
                      Detected Intents:
                    </p>
                    <div className="flex flex-wrap gap-2">
                      {conv.intents.map((intent, idx) => (
                        <span key={idx} className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">
                          {intent}: {(conv.intentScores[intent] * 100).toFixed(0)}%
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {/* Sources */}
                {conv.sources && conv.sources.length > 0 && (
                  <div className="mb-3 p-3 bg-amber-50 rounded-lg">
                    <p className="text-xs font-semibold text-amber-700 mb-2 flex items-center gap-1">
                      <FileText className="w-3 h-3" />
                      Sources ({conv.sources.length}):
                    </p>
                    <div className="space-y-1">
                      {conv.sources.map((source, idx) => (
                        <div key={idx} className="text-xs text-amber-800">
                          • {source.title} (Page {source.page})
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Action Pack */}
                {conv.actionPack && (
                  <div className="p-3 bg-purple-50 rounded-lg">
                    <p className="text-xs font-semibold text-purple-700 mb-2">
                      Action Plan:
                    </p>
                    <div className="text-sm text-purple-800 whitespace-pre-wrap">
                      {conv.actionPack}
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default VoiceQueryInterface;