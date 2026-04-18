import React, { useState } from 'react';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import VoiceQueryInterface from './components/VoiceQueryInterface';
import { FileText, Home, Settings, HelpCircle, Shield } from 'lucide-react';

function App() {
  const [activeTab, setActiveTab] = useState('voice');

  const renderContent = () => {
    switch (activeTab) {
      case 'voice':
        return <VoiceQueryInterface />;
      
      case 'home':
        return (
          <div className="text-center py-16">
            <Home className="w-20 h-20 text-primary-500 mx-auto mb-6" />
            <h2 className="text-3xl font-bold text-slate-800 mb-4">
              Welcome to Samadhan AI
            </h2>
            <p className="text-slate-600 max-w-2xl mx-auto mb-8">
              Your sovereign AI-powered portal for accessing legal and government services 
              in your regional language. Get started by clicking "Voice Query" in the sidebar.
            </p>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto">
              <div className="card text-center">
                <Shield className="w-12 h-12 text-primary-600 mx-auto mb-3" />
                <h3 className="font-bold text-slate-800 mb-2">Legal Services</h3>
                <p className="text-sm text-slate-600">
                  Access government legal services and documentation
                </p>
              </div>
              <div className="card text-center">
                <FileText className="w-12 h-12 text-primary-600 mx-auto mb-3" />
                <h3 className="font-bold text-slate-800 mb-2">Document Support</h3>
                <p className="text-sm text-slate-600">
                  Manage and access your legal documents easily
                </p>
              </div>
              <div className="card text-center">
                <HelpCircle className="w-12 h-12 text-primary-600 mx-auto mb-3" />
                <h3 className="font-bold text-slate-800 mb-2">24/7 Assistance</h3>
                <p className="text-sm text-slate-600">
                  Get help anytime in your preferred language
                </p>
              </div>
            </div>
          </div>
        );
      
      case 'documents':
        return (
          <div className="text-center py-16">
            <FileText className="w-20 h-20 text-slate-400 mx-auto mb-6" />
            <h2 className="text-2xl font-bold text-slate-800 mb-4">Documents</h2>
            <p className="text-slate-600">Document management coming soon...</p>
          </div>
        );
      
      case 'legal':
        return (
          <div className="text-center py-16">
            <Shield className="w-20 h-20 text-slate-400 mx-auto mb-6" />
            <h2 className="text-2xl font-bold text-slate-800 mb-4">Legal Services</h2>
            <p className="text-slate-600">Legal services portal coming soon...</p>
          </div>
        );
      
      case 'help':
        return (
          <div className="text-center py-16">
            <HelpCircle className="w-20 h-20 text-slate-400 mx-auto mb-6" />
            <h2 className="text-2xl font-bold text-slate-800 mb-4">Help Center</h2>
            <p className="text-slate-600">Help and support coming soon...</p>
          </div>
        );
      
      case 'settings':
        return (
          <div className="text-center py-16">
            <Settings className="w-20 h-20 text-slate-400 mx-auto mb-6" />
            <h2 className="text-2xl font-bold text-slate-800 mb-4">Settings</h2>
            <p className="text-slate-600">Settings panel coming soon...</p>
          </div>
        );
      
      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Sidebar */}
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
      
      {/* Header */}
      <Header />
      
      {/* Main Content */}
      <main className="ml-64 pt-16 min-h-screen">
        <div className="p-8">
          {renderContent()}
        </div>
      </main>
    </div>
  );
}

export default App;
