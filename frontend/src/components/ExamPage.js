import React, { useState, useEffect } from 'react';
import api from '../services/api';

function ExamPage({ userId }) {
  const [questions, setQuestions] = useState([
    { id: 'q1', text: 'Explain the concept of inheritance in OOP', answer: '' },
    { id: 'q2', text: 'What is polymorphism?', answer: '' },
    { id: 'q3', text: 'Describe encapsulation', answer: '' },
  ]);
  
  const [startTime, setStartTime] = useState(null);
  const [copyCounts, setCopyCounts] = useState(0);
  const [tabSwitchCounts, setTabSwitchCounts] = useState(0);
  const [eventLog, setEventLog] = useState([]);

  // Track when user leaves the window
  useEffect(() => {
    const handleBlur = () => {
      logEvent('tab_switch', {
        event: 'user_switched_to_different_tab'
      });
      console.warn('⚠️ Tab switch detected');
    };

    const handleFocus = () => {
      console.log('✓ User returned to exam');
    };

    const handleCopy = () => {
      logEvent('copy_paste', {
        event: 'user_copied_text'
      });
      setCopyCounts(prev => prev + 1);
      console.warn('⚠️ Copy detected');
    };

    window.addEventListener('blur', handleBlur);
    window.addEventListener('focus', handleFocus);
    document.addEventListener('copy', handleCopy);

    return () => {
      window.removeEventListener('blur', handleBlur);
      window.removeEventListener('focus', handleFocus);
      document.removeEventListener('copy', handleCopy);
    };
  }, [userId]);

  // Log event to backend
  const logEvent = async (eventType, metadata = {}) => {
    try {
      await api.logEvent(userId, eventType, metadata);
      
      const newEvent = {
        type: eventType,
        time: new Date().toLocaleTimeString(),
        metadata
      };
      setEventLog(prev => [...prev, newEvent]);
    } catch (error) {
      console.error('Failed to log event:', error);
    }
  };

  // Handle answer change
  const handleAnswerChange = (questionId, value) => {
    setQuestions(questions.map(q => 
      q.id === questionId ? { ...q, answer: value } : q
    ));
  };

  // Submit exam
  const handleSubmitExam = async () => {
    try {
      // Log all answers as submission
      for (const q of questions) {
        if (q.answer) {
          const timeSpent = Math.floor((Date.now() - startTime) / 1000);
          await api.logEvent(userId, 'answer_submission', {
            question_id: q.id,
            answer: q.answer,
            time_taken_seconds: timeSpent,
            answer_length: q.answer.length
          });
        }
      }
      
      alert('✓ Exam submitted successfully');
      resetExam();
    } catch (error) {
      alert('✗ Error submitting exam');
      console.error(error);
    }
  };

  // Reset exam
  const resetExam = () => {
    setQuestions(questions.map(q => ({ ...q, answer: '' })));
    setCopyCounts(0);
    setTabSwitchCounts(0);
    setEventLog([]);
    setStartTime(Date.now());
  };

  // Initialize
  useEffect(() => {
    if (!startTime) {
      setStartTime(Date.now());
    }
  }, []);

  return (
    <div className="exam-page">
      <div className="exam-header">
        <h2>Exam Paper</h2>
        <div className="stats">
          <span>📋 Copy Events: {copyCounts}</span>
          <span>📑 Tab Switches: {tabSwitchCounts}</span>
          <span>⏱️ Time: {startTime ? Math.floor((Date.now() - startTime) / 1000) : 0}s</span>
        </div>
      </div>

      <div className="exam-questions">
        {questions.map((question, index) => (
          <div key={question.id} className="question-block">
            <h3>Question {index + 1}</h3>
            <p className="question-text">{question.text}</p>
            <textarea
              value={question.answer}
              onChange={(e) => handleAnswerChange(question.id, e.target.value)}
              placeholder="Type your answer here..."
              rows="4"
              className="answer-input"
            />
            <p className="char-count">Characters: {question.answer.length}</p>
          </div>
        ))}
      </div>

      <div className="exam-actions">
        <button onClick={handleSubmitExam} className="submit-btn">
          🚀 Submit Exam
        </button>
        <button onClick={resetExam} className="reset-btn">
          🔄 Reset
        </button>
      </div>

      <div className="event-log">
        <h3>📅 Event Log</h3>
        <div className="log-list">
          {eventLog.length === 0 ? (
            <p className="no-events">No suspicious events yet</p>
          ) : (
            eventLog.map((event, index) => (
              <div key={index} className="log-entry">
                <span className="time">{event.time}</span>
                <span className="event-type">⚠️ {event.type}</span>
              </div>
            ))
          )}
        </div>
      </div>

      <div className="warning">
        ⚠️ <strong>Important:</strong> Any attempt to copy content, switch tabs, or use external resources will be detected and logged.
      </div>
    </div>
  );
}

export default ExamPage;
