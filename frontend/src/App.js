import React, { useState, useEffect } from 'react';
import api from './services/api';
import ExamPage from './components/ExamPage';
import ReportPage from './components/ReportPage';
import './App.css';

function App() {
  const [currentPage, setCurrentPage] = useState('exam'); // 'exam' or 'report'
  const [userId, setUserId] = useState('student_001');
  const [backendConnected, setBackendConnected] = useState(false);

  // Check if backend is running
  useEffect(() => {
    const checkBackend = async () => {
      const isConnected = await api.healthCheck();
      setBackendConnected(isConnected);
    };
    
    checkBackend();
    const interval = setInterval(checkBackend, 5000); // Check every 5 seconds
    
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Online Proctoring System</h1>
        <div className="status">
          <span className={`status-badge ${backendConnected ? 'connected' : 'disconnected'}`}>
            {backendConnected ? '✓ Backend Connected' : '✗ Backend Offline'}
          </span>
        </div>
      </header>

      <div className="navigation">
        <button 
          className={`nav-button ${currentPage === 'exam' ? 'active' : ''}`}
          onClick={() => setCurrentPage('exam')}
        >
          📝 Exam Page
        </button>
        <button 
          className={`nav-button ${currentPage === 'report' ? 'active' : ''}`}
          onClick={() => setCurrentPage('report')}
        >
          📊 Report
        </button>
      </div>

      <div className="user-input">
        <label>User ID:</label>
        <input 
          type="text" 
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
          placeholder="Enter student ID"
        />
      </div>

      <main className="main-content">
        {currentPage === 'exam' ? (
          <ExamPage userId={userId} />
        ) : (
          <ReportPage userId={userId} />
        )}
      </main>

      <footer className="App-footer">
        <p>Online Proctoring System v1.0</p>
        <p>Backend: http://localhost:8000</p>
      </footer>
    </div>
  );
}

export default App;
