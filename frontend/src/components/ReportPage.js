import React, { useState, useEffect, useCallback } from 'react';
import api from '../services/api';

function ReportPage({ userId }) {
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchReport = useCallback(async () => {
    setLoading(true);
    setError(null);
    
    try {
      const data = await api.getIntegrityReport(userId);
      setReport(data);
    } catch (err) {
      setError('Failed to fetch report. Make sure backend is running.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, [userId]);

  // Fetch report when userId changes
  useEffect(() => {
    fetchReport();
  }, [fetchReport]);

  const getScoreColor = (score) => {
    switch(score) {
      case 'HIGH':
        return '#4caf50'; // Green
      case 'MEDIUM':
        return '#ff9800'; // Orange
      case 'LOW':
        return '#f44336'; // Red
      default:
        return '#999';
    }
  };

  const getScoreEmoji = (score) => {
    switch(score) {
      case 'HIGH':
        return '✅';
      case 'MEDIUM':
        return '⚠️';
      case 'LOW':
        return '❌';
      default:
        return '❓';
    }
  };

  return (
    <div className="report-page">
      <div className="report-header">
        <h2>Integrity Report</h2>
        <button onClick={fetchReport} className="refresh-btn" disabled={loading}>
          {loading ? '⏳ Loading...' : '🔄 Refresh'}
        </button>
      </div>

      {error && (
        <div className="error-message">
          ⚠️ {error}
        </div>
      )}

      {loading && (
        <div className="loading">
          Loading report...
        </div>
      )}

      {report && !loading && (
        <div className="report-content">
          <div className="report-card">
            <h3>📊 Summary for {report.user_id}</h3>
            
            {/* Integrity Score */}
            <div className="score-section">
              <h4>Integrity Score</h4>
              <div 
                className="score-badge"
                style={{ 
                  backgroundColor: getScoreColor(report.integrity_score),
                  color: 'white',
                  padding: '20px',
                  borderRadius: '10px',
                  textAlign: 'center',
                  fontSize: '24px',
                  fontWeight: 'bold',
                  marginTop: '10px'
                }}
              >
                {getScoreEmoji(report.integrity_score)} {report.integrity_score}
              </div>
              <p style={{ marginTop: '10px', fontSize: '14px', color: '#666' }}>
                {report.integrity_score === 'HIGH' && '✅ No violations detected. Exam appears legitimate.'}
                {report.integrity_score === 'MEDIUM' && '⚠️ Minor violations detected. Further review recommended.'}
                {report.integrity_score === 'LOW' && '❌ Multiple violations detected. Exam integrity compromised.'}
              </p>
            </div>

            {/* Statistics */}
            <div className="stats-grid">
              <div className="stat-card">
                <h4>📋 Copy-Paste Events</h4>
                <div className="stat-value">{report.copy_paste_count}</div>
                <p>Attempts to copy content</p>
              </div>

              <div className="stat-card">
                <h4>📑 Tab Switches</h4>
                <div className="stat-value">{report.tab_switch_count}</div>
                <p>Times user left the exam</p>
              </div>

              <div className="stat-card">
                <h4>🤖 AI Suspicion</h4>
                <div className="stat-value">{report.ai_suspicion_count}</div>
                <p>Suspicious answers detected</p>
              </div>

              <div className="stat-card">
                <h4>🎯 Total Events</h4>
                <div className="stat-value">{report.details.total_events}</div>
                <p>Events recorded</p>
              </div>
            </div>

            {/* Event Types */}
            {report.details.event_types && report.details.event_types.length > 0 && (
              <div className="event-types-section">
                <h4>📝 Event Types Detected</h4>
                <div className="event-types">
                  {report.details.event_types.map((type, index) => (
                    <span key={index} className="event-type-tag">
                      {type.replace('_', ' ').toUpperCase()}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Suspicious Answers */}
            {report.details.suspicious_answers && report.details.suspicious_answers.length > 0 && (
              <div className="suspicious-section">
                <h4>🚨 Suspicious Answers</h4>
                <div className="suspicious-list">
                  {report.details.suspicious_answers.map((answer, index) => (
                    <div key={index} className="suspicious-item">
                      <p><strong>Answer {index + 1}:</strong></p>
                      <p>📏 Length: {answer.answer_length} characters</p>
                      <p>⏱️ Time taken: {answer.time_taken} seconds</p>
                      <p>⚠️ {answer.reason}</p>
                      <p style={{ fontSize: '12px', color: '#999', marginTop: '5px' }}>
                        Timestamp: {new Date(answer.timestamp * 1000).toLocaleString()}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Detailed Information */}
            <div className="detailed-info">
              <h4>ℹ️ Detailed Information</h4>
              <table className="info-table">
                <tbody>
                  <tr>
                    <td><strong>User ID:</strong></td>
                    <td>{report.user_id}</td>
                  </tr>
                  <tr>
                    <td><strong>Total Events:</strong></td>
                    <td>{report.details.total_events}</td>
                  </tr>
                  <tr>
                    <td><strong>Copy-Paste Count:</strong></td>
                    <td>{report.copy_paste_count}</td>
                  </tr>
                  <tr>
                    <td><strong>Tab Switch Count:</strong></td>
                    <td>{report.tab_switch_count}</td>
                  </tr>
                  <tr>
                    <td><strong>AI Suspicion Count:</strong></td>
                    <td>{report.ai_suspicion_count}</td>
                  </tr>
                  <tr>
                    <td><strong>Overall Score:</strong></td>
                    <td style={{ color: getScoreColor(report.integrity_score), fontWeight: 'bold' }}>
                      {report.integrity_score}
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            {/* Recommendations */}
            <div className="recommendations">
              <h4>💡 Recommendations</h4>
              <ul>
                {report.integrity_score === 'HIGH' && (
                  <>
                    <li>✅ This exam appears legitimate and ready for grading.</li>
                    <li>✅ No suspicious activity detected.</li>
                  </>
                )}
                {report.integrity_score === 'MEDIUM' && (
                  <>
                    <li>⚠️ Review the exam manually due to minor violations.</li>
                    <li>⚠️ Interview the student about the detected activity.</li>
                    <li>⚠️ Consider allowing the student to retake if violations were minor.</li>
                  </>
                )}
                {report.integrity_score === 'LOW' && (
                  <>
                    <li>❌ Do not accept this exam without further investigation.</li>
                    <li>❌ Contact the student immediately for clarification.</li>
                    <li>❌ Consider invalidating the exam and requiring a retake.</li>
                  </>
                )}
              </ul>
            </div>
          </div>
        </div>
      )}

      {!report && !loading && !error && (
        <div className="no-data">
          No report data available. Try entering a different user ID.
        </div>
      )}
    </div>
  );
}

export default ReportPage;
