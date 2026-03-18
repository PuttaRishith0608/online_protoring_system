import React, { useState, useEffect, useRef } from 'react';
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
  const isAlertActive = useRef(false);

  // ============ EVENT LOGGING FUNCTION ============
  const logEvent = async (eventType, metadata = {}) => {
    try {
      console.log(`📤 Sending event to backend: ${eventType}`, metadata);
      await api.logEvent(userId, eventType, metadata);
      
      const newEvent = {
        type: eventType,
        time: new Date().toLocaleTimeString(),
        metadata
      };
      setEventLog(prev => [...prev, newEvent]);
      console.log(`✓ Event logged successfully: ${eventType}`);
    } catch (error) {
      console.error('❌ Failed to log event:', error);
    }
  };

  // ============ COPY-PASTE DETECTION SETUP ============
  useEffect(() => {
    console.log('🔧 Setting up event listeners...');

    // ===== COPY EVENT HANDLER =====
    const handleCopy = (e) => {
      console.warn('⚠️ COPY EVENT DETECTED - using Ctrl+C or right-click menu');
      e.preventDefault();
      
      logEvent('copy_paste', {
        operation: 'copy',
        source: 'copy_event',
        timestamp: new Date().toISOString()
      });
      setCopyCounts(prev => prev + 1);
      
      isAlertActive.current = true;
      alert('❌ Copy-paste is not allowed during exam!');
      isAlertActive.current = false;
    };

    // ===== PASTE EVENT HANDLER =====
    const handlePaste = (e) => {
      console.warn('⚠️ PASTE EVENT DETECTED - user tried to paste');
      e.preventDefault();
      
      logEvent('copy_paste', {
        operation: 'paste',
        source: 'paste_event',
        timestamp: new Date().toISOString()
      });
      setCopyCounts(prev => prev + 1);
      
      isAlertActive.current = true;
      alert('❌ Pasting is not allowed during exam!');
      isAlertActive.current = false;
      return false;
    };

    // ===== CUT EVENT HANDLER =====
    const handleCut = (e) => {
      console.warn('⚠️ CUT EVENT DETECTED - using Ctrl+X');
      e.preventDefault();
      
      logEvent('copy_paste', {
        operation: 'cut',
        source: 'cut_event',
        timestamp: new Date().toISOString()
      });
      setCopyCounts(prev => prev + 1);
      
      isAlertActive.current = true;
      alert('❌ Cut operation is not allowed during exam!');
      isAlertActive.current = false;
      return false;
    };

    // ===== KEYBOARD SHORTCUT DETECTION =====
    const handleKeyDown = (e) => {
      // Detect Ctrl+C (or Cmd+C on Mac)
      if ((e.ctrlKey || e.metaKey) && e.key === 'c') {
        console.warn('⚠️ KEYBOARD SHORTCUT DETECTED - Ctrl+C');
        e.preventDefault();
        
        logEvent('copy_paste', {
          operation: 'copy',
          source: 'keyboard_ctrl_c',
          timestamp: new Date().toISOString()
        });
        setCopyCounts(prev => prev + 1);
        
        isAlertActive.current = true;
        alert('❌ Copy operation (Ctrl+C) is not allowed during exam!');
        isAlertActive.current = false;
        return false;
      }

      // Detect Ctrl+V (or Cmd+V on Mac)
      if ((e.ctrlKey || e.metaKey) && e.key === 'v') {
        console.warn('⚠️ KEYBOARD SHORTCUT DETECTED - Ctrl+V');
        e.preventDefault();
        
        logEvent('copy_paste', {
          operation: 'paste',
          source: 'keyboard_ctrl_v',
          timestamp: new Date().toISOString()
        });
        setCopyCounts(prev => prev + 1);
        
        isAlertActive.current = true;
        alert('❌ Paste operation (Ctrl+V) is not allowed during exam!');
        isAlertActive.current = false;
        return false;
      }

      // Detect Ctrl+X (or Cmd+X on Mac)
      if ((e.ctrlKey || e.metaKey) && e.key === 'x') {
        console.warn('⚠️ KEYBOARD SHORTCUT DETECTED - Ctrl+X');
        e.preventDefault();
        
        logEvent('copy_paste', {
          operation: 'cut',
          source: 'keyboard_ctrl_x',
          timestamp: new Date().toISOString()
        });
        setCopyCounts(prev => prev + 1);
        
        isAlertActive.current = true;
        alert('❌ Cut operation (Ctrl+X) is not allowed during exam!');
        isAlertActive.current = false;
        return false;
      }
    };

    // ===== TAB SWITCH DETECTION =====
    const handleBlur = () => {
      // Don't count as tab switch if alert is active (alert causes blur event)
      if (isAlertActive.current) {
        console.log('ℹ️ Blur event from alert - not counting as tab switch');
        return;
      }
      
      console.warn('⚠️ TAB SWITCH DETECTED - user left window');
      logEvent('tab_switch', {
        event: 'user_switched_to_different_tab',
        timestamp: new Date().toISOString()
      });
      setTabSwitchCounts(prev => prev + 1);
    };

    const handleFocus = () => {
      console.log('✓ User returned to exam');
    };

    // ===== REGISTER EVENT LISTENERS =====
    // Add listeners to document for copy/paste/cut events
    document.addEventListener('copy', handleCopy, true);  // true = capture phase
    document.addEventListener('paste', handlePaste, true);
    document.addEventListener('cut', handleCut, true);
    document.addEventListener('keydown', handleKeyDown, true);

    // Add listeners for tab switching
    window.addEventListener('blur', handleBlur);
    window.addEventListener('focus', handleFocus);

    console.log('✓ All event listeners registered successfully');

    // ===== CLEANUP ON UNMOUNT =====
    return () => {
      console.log('🧹 Cleaning up event listeners...');
      document.removeEventListener('copy', handleCopy, true);
      document.removeEventListener('paste', handlePaste, true);
      document.removeEventListener('cut', handleCut, true);
      document.removeEventListener('keydown', handleKeyDown, true);
      window.removeEventListener('blur', handleBlur);
      window.removeEventListener('focus', handleFocus);
      console.log('✓ Event listeners cleaned up');
    };
  }, [userId]);



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
      
      isAlertActive.current = true;
      alert('✓ Exam submitted successfully');
      isAlertActive.current = false;
      resetExam();
    } catch (error) {
      isAlertActive.current = true;
      alert('✗ Error submitting exam');
      isAlertActive.current = false;
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
