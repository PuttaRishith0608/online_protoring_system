const BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

/**
 * Log an event to the backend
 * @param {string} userId - User ID
 * @param {string} eventType - Type of event (copy_paste, tab_switch, answer_submission)
 * @param {object} metadata - Additional event data
 */
export const logEvent = async (userId, eventType, metadata = {}) => {
  try {
    const response = await fetch(`${BASE_URL}/log-event`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_id: userId,
        event_type: eventType,
        timestamp: Date.now() / 1000,
        metadata: metadata
      })
    });
    
    if (!response.ok) {
      throw new Error(`API error: ${response.statusText}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error logging event:', error);
    throw error;
  }
};

/**
 * Get integrity report for a user
 * @param {string} userId - User ID
 * @returns {object} Integrity report with statistical data
 */
export const getIntegrityReport = async (userId) => {
  try {
    const response = await fetch(`${BASE_URL}/report/${userId}`);
    
    if (!response.ok) {
      throw new Error(`API error: ${response.statusText}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error fetching report:', error);
    throw error;
  }
};

/**
 * Get all events for a user (debug purposes)
 * @param {string} userId - User ID
 */
export const getUserEvents = async (userId) => {
  try {
    const response = await fetch(`${BASE_URL}/events/${userId}`);
    
    if (!response.ok) {
      throw new Error(`API error: ${response.statusText}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error fetching events:', error);
    throw error;
  }
};

/**
 * Check if backend is running
 */
export const healthCheck = async () => {
  try {
    const response = await fetch(`${BASE_URL}/health`);
    return response.ok;
  } catch (error) {
    return false;
  }
};

export default {
  logEvent,
  getIntegrityReport,
  getUserEvents,
  healthCheck
};
