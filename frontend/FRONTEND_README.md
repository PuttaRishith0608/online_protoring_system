# Frontend - Online Proctoring System

React-based frontend for the Online Proctoring System that detects academic integrity violations.

## Features

✅ **Exam Interface** - Clean exam page with multiple questions  
✅ **Event Tracking** - Detects copy-paste and tab switching  
✅ **Real-time Monitoring** - Logs events as they happen  
✅ **Integrity Reports** - Beautiful visual reports with violation details  
✅ **Responsive Design** - Works on desktop and tablet  
✅ **Live Backend Status** - Shows connection status to backend  

## Installation

### Prerequisites

- Node.js 14+ and npm
- Backend server running at `http://localhost:8000`

### Setup

1. **Install dependencies:**
```bash
cd frontend
npm install
```

2. **Start development server:**
```bash
npm start
```

The frontend will open at `http://localhost:3000`

3. **Build for production:**
```bash
npm run build
```

## How It Works

### Exam Page

1. Student enters their user ID
2. Answers multiple questions
3. System tracks:
   - ✂️ Copy-paste attempts (Ctrl+C)
   - 📱 Tab switches (window blur/focus)
   - ⏱️ Answer submission time
   - 📏 Answer length

### Report Page

Shows comprehensive integrity report with:
- 📊 Copy-paste count
- 📑 Tab switch count
- 🤖 AI suspicion score
- 📈 Overall integrity rating (HIGH/MEDIUM/LOW)
- 📋 Detailed violation list
- 💡 Recommendations

## Project Structure

```
frontend/src/
├── App.js                  # Main React component
├── App.css                # Global styles
├── index.js               # React entry point
├── components/
│   ├── ExamPage.js       # Exam taking interface
│   └── ReportPage.js     # Report viewing interface
└── services/
    └── api.js            # Backend API calls
```

## Component Documentation

### App.js

Main component that manages:
- Navigation between pages
- User ID state
- Backend connectivity status
- Page routing

```jsx
<App>
  ├─ Header (status bar)
  ├─ Navigation (page switcher)
  ├─ User Input (ID field)
  ├─ Main Content
  │  ├─ ExamPage (when exam tab active)
  │  └─ ReportPage (when report tab active)
  └─ Footer
</App>
```

### ExamPage.js

Handles exam functionality:
- Displays questions
- Captures answers
- Tracks events
- Detects violations

**Events tracked:**
- `copy_paste` - When user copies text (Ctrl+C/Cmd+C)
- `tab_switch` - When user leaves the exam window
- `answer_submission` - When user submits answers

```jsx
<ExamPage>
  ├─ Exam Header (stats: copy count, tab switches, time)
  ├─ Questions List
  │  └─ Question Block (answer textarea)
  ├─ Action Buttons (Submit, Reset)
  └─ Event Log (shows detected violations)
</ExamPage>
```

### ReportPage.js

Displays integrity report:
- Visual score badge
- Statistics grid
- Violation details
- Recommendations

```jsx
<ReportPage>
  ├─ Report Header
  ├─ Integrity Score (HIGH/MEDIUM/LOW with color)
  ├─ Statistics Grid
  │  ├─ Copy-Paste Count
  │  ├─ Tab Switches
  │  ├─ AI Suspicions
  │  └─ Total Events
  ├─ Event Types
  ├─ Suspicious Answers
  ├─ Detailed Information
  └─ Recommendations
</ReportPage>
```

### api.js

Service for backend communication:

```javascript
// Log an event
await api.logEvent(userId, eventType, metadata);

// Get integrity report
const report = await api.getIntegrityReport(userId);

// Get all events (debug)
const events = await api.getUserEvents(userId);

// Check backend health
const isHealthy = await api.healthCheck();
```

## Event Types

### Copy Paste
```javascript
{
  event_type: "copy_paste",
  metadata: {
    event: "user_copied_text"
  }
}
```

### Tab Switch
```javascript
{
  event_type: "tab_switch",
  metadata: {
    event: "user_switched_to_different_tab"
  }
}
```

### Answer Submission
```javascript
{
  event_type: "answer_submission",
  metadata: {
    question_id: "q1",
    answer: "Student's answer text...",
    time_taken_seconds: 120,
    answer_length: 250
  }
}
```

## Styling

### Color Scheme

- **Primary:** #667eea (Purple)
- **Secondary:** #764ba2 (Dark Purple)
- **Success:** #4caf50 (Green)
- **Warning:** #ff9800 (Orange)
- **Error:** #f44336 (Red)

### Responsive Design

- Desktop: Full width layout
- Tablet: Adjusted padding and grid
- Mobile: Single column layout, reduced font sizes

## API Integration

The frontend communicates with the backend API:

```
Frontend (React)  ←→  Backend (FastAPI)
   :3000               :8000

POST /log-event
GET /report/{user_id}
GET /events/{user_id}
GET /health
```

## Development Tips

### Hot Reload

Changes are automatically reloaded during development:

```bash
npm start
# Edit files, changes appear instantly
```

### Debug Events

Open browser console (F12) to see logged events:

```javascript
// In ExamPage, events are logged to console
console.log("✓ Tab switch detected");
console.log("⚠️ Copy detected");
```

### Mock Backend

If backend is down, you'll see "✗ Backend Offline" in the header.

To test with mock data, modify `api.js`:

```javascript
export const getIntegrityReport = async (userId) => {
  // Mock response
  return {
    user_id: userId,
    copy_paste_count: 2,
    tab_switch_count: 1,
    ai_suspicion_count: 0,
    integrity_score: "MEDIUM"
  };
};
```

## Deployment

### Build Production Bundle

```bash
npm run build
```

Creates optimized build in `build/` folder.

### Deploy to Netlify

```bash
npm run build
# Upload build/ folder to Netlify
```

### Deploy to AWS S3

```bash
npm run build
aws s3 sync build/ s3://your-bucket-name
```

### Configure Backend URL

For production, change `BASE_URL` in `src/services/api.js`:

```javascript
const BASE_URL = 'https://api.example.com';  // Production
```

## Troubleshooting

### "Cannot connect to backend"

**Problem:** Frontend shows "✗ Backend Offline"

**Solution:**
1. Make sure backend is running: `python app.py`
2. Check backend URL in `api.js`
3. Ensure CORS is enabled on backend

### "Module not found"

**Problem:** `Module not found: Can't resolve 'react'`

**Solution:**
```bash
npm install
```

### Port 3000 already in use

**Problem:** `Something is already running on port 3000`

**Solution:**
```bash
npm start -- --port 3001
```

### Events not being logged

**Problem:** No events appear in report

**Solution:**
1. Check browser console for errors (F12)
2. Verify backend is running and healthy
3. Check that event listeners are attached (see ExamPage.js useEffect)

## Testing Scenarios

### Scenario 1: Clean Exam
- Student completes exam normally
- ✅ Result: HIGH integrity score

### Scenario 2: Copy-Paste Violation
- Student copies text from question
- ⚠️ Result: MEDIUM integrity score

### Scenario 3: Multiple Violations
- Student copies multiple times
- Student switches tabs
- Submits long answer too quickly
- ❌ Result: LOW integrity score

## Browser Compatibility

✅ **Supported:**
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

❌ **Not Supported:**
- Internet Explorer
- Older browser versions

## Performance Tips

1. **Use React DevTools**: Browser extension for debugging
2. **Monitor Network**: Check API response times
3. **Check Console**: Look for warnings and errors
4. **Profile Performance**: Use Chrome DevTools Performance tab

## Further Development

- ✅ Add authentication (JWT)
- ✅ Add camera/microphone proctoring
- ✅ Add screen recording
- ✅ Add more advanced AI detection
- ✅ Add exam timer
- ✅ Add question randomization

---

**Need help?** Check the backend README for API documentation.
