import React from 'react';
import { Home, Mic, FileText, Settings, HelpCircle, Shield } from 'lucide-react';

const Sidebar = ({ activeTab, setActiveTab }) => {
  const menuItems = [
    { id: 'home', label: 'Dashboard', icon: Home },
    { id: 'documents', label: 'Documents', icon: FileText },
    { id: 'legal', label: 'Legal Services', icon: Shield },
    { id: 'help', label: 'Help', icon: HelpCircle },
    { id: 'settings', label: 'Settings', icon: Settings },
  ];

  return (
    <div className="w-64 bg-gradient-to-b from-slate-900 to-slate-800 text-white h-screen fixed left-0 top-0 shadow-2xl">
      {/* Logo Section */}
      <div className="p-6 border-b border-slate-700">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-gradient-to-br from-primary-500 to-primary-700 rounded-lg flex items-center justify-center shadow-lg">
            <Shield className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-xl font-bold">Samadhan AI</h1>
            <p className="text-xs text-slate-400">Sovereign Portal</p>
          </div>
        </div>
      </div>

      {/* Navigation Menu */}
      <nav className="p-4 space-y-2">
        {menuItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg transition-all duration-200 ${
                isActive
                  ? 'bg-primary-600 text-white shadow-lg shadow-primary-500/50'
                  : 'text-slate-300 hover:bg-slate-700 hover:text-white'
              }`}
            >
              <Icon className="w-5 h-5" />
              <span className="font-medium">{item.label}</span>
            </button>
          );
        })}
      </nav>

      {/* Bottom Info */}
      <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-slate-700">
        <div className="bg-slate-800/50 rounded-lg p-3">
          <p className="text-xs text-slate-400">Powered by</p>
          <p className="text-sm font-semibold text-white">Databricks AI</p>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
