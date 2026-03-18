# Online Proctoring System

A complete online proctoring solution that detects academic integrity violations including copy-paste activity, tab switching, and AI-generated answers.

## Features

✅ **Activity Logging** - Captures user events (copy-paste, tab switches, answer submissions)  
✅ **AI Detection** - Detects suspicious patterns in answer submissions  
✅ **Integrity Reports** - Generates detailed integrity scores for each user  
✅ **In-Memory Storage** - Fast event storage without database setup  
✅ **REST API** - Simple FastAPI endpoints for logging and reporting  
✅ **CORS Enabled** - Ready for React frontend integration  
✅ **Interactive Docs** - Built-in Swagger UI for API testing  

## Project Structure

```
online-proctoring-system/
├── backend/
│   ├── app.py                    # Main FastAPI application
│   ├── requirements.txt          # Python dependencies
│   ├── routes/
│   │   ├── activity.py          # POST /log-event endpoint
│   │   └── report.py            # GET /report/{user_id} endpoint
│   ├── models/
│   │   └── activity_model.py    # Data models
│   ├── services/
│   │   ├── event_service.py     # Event storage management
│   │   ├── report_service.py    # Report generation
│   │   ├── ai_detector.py       # AI detection heuristics
│   │   └── logger.py            # Logging utility
│   └── database/
│       └── db.py                # Database setup (placeholder)
├── frontend/
│   ├── src/
│   │   ├── App.js
│   │   ├── components/
│   │   │   ├── ExamPage.js
│   │   │   └── ReportPage.js
│   │   └── services/
│   │       └── api.js
│   └── package.json
└── README.md
```

## Quick Start

### Backend Setup

1. **Install Python dependencies:**
```bash
cd backend
pip install -r requirements.txt
```

2. **Run the server:**
```bash
python app.py
```

The backend will start at `http://localhost:8000`

3. **Access API Documentation:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### 1. Log an Event
**POST** `/log-event`

Log user activity events (copy-paste, tab switches, answer submissions).

**Request Body:**
```json
{
  "user_id": "user123",
  "event_type": "copy_paste",
  "timestamp": 1647384720.123,
  "metadata": {
    "source": "exam_text",
    "destination": "answer_field"
  }
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Event logged for user user123",
  "event_type": "copy_paste"
}
```

**Supported Event Types:**
- `copy_paste` - User copied text
- `tab_switch` - User switched to another tab
- `answer_submission` - User submitted an answer
- `keyboard_input` - User typed something

---

### 2. Get Integrity Report
**GET** `/report/{user_id}`

Get a comprehensive integrity report for a user showing suspicious activity counts and overall integrity score.

**Example:** `GET /report/user123`

**Response:**
```json
{
  "user_id": "user123",
  "copy_paste_count": 2,
  "tab_switch_count": 3,
  "ai_suspicion_count": 1,
  "integrity_score": "MEDIUM",
  "details": {
    "total_events": 10,
    "event_types": ["copy_paste", "tab_switch", "answer_submission"],
    "suspicious_answers": [
      {
        "timestamp": 1647384725.456,
        "answer_length": 250,
        "time_taken": 5,
        "reason": "Long answer submitted too quickly"
      }
    ]
  }
}
```

---

### 3. Get User Events (Debug)
**GET** `/events/{user_id}`

Retrieve all events logged for a specific user (for debugging/admin purposes).

**Example:** `GET /events/user123`

---

### 4. Health Check
**GET** `/health`

Check if the backend is running.

## Integrity Scoring System

The integrity score is calculated based on the total number of suspicious events:

| Score | Condition | Meaning |
|-------|-----------|---------|
| **HIGH** | 0 suspicious events | ✅ No violations detected |
| **MEDIUM** | 1-3 suspicious events | ⚠️ Minor violations detected |
| **LOW** | 4+ suspicious events | ❌ Multiple violations detected |

## AI Detection Heuristic

The system flags answer submissions as suspicious if:
- **Answer length > 200 characters** AND
- **Submitted in < 10 seconds**

This heuristic detects unusually long, high-quality answers submitted too quickly, which is indicative of copy-paste or AI-generated content.

## Working with the Frontend

The frontend should send events to the backend as users interact with the exam:

```javascript
// Example: Log a copy-paste event
const logEvent = async (event) => {
  const response = await fetch('http://localhost:8000/log-event', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(event)
  });
  return response.json();
};

// Example: Get a report
const getReport = async (userId) => {
  const response = await fetch(`http://localhost:8000/report/${userId}`);
  return response.json();
};
```

## Testing the API

### Using cURL

```bash
# Log an event
curl -X POST http://localhost:8000/log-event \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "event_type": "copy_paste",
    "timestamp": '$(date +%s)'.000,
    "metadata": {"source": "clipboard"}
  }'

# Get a report
curl http://localhost:8000/report/user123
```

### Using Python

```python
import requests
import time

BASE_URL = "http://localhost:8000"

# Log an event
event = {
    "user_id": "user123",
    "event_type": "tab_switch",
    "timestamp": time.time(),
    "metadata": {"tab": "facebook.com"}
}
response = requests.post(f"{BASE_URL}/log-event", json=event)
print(response.json())

# Get report
response = requests.get(f"{BASE_URL}/report/user123")
print(response.json())
```

## Data Storage

Events are stored in **memory** using Python dictionaries. This means:

✅ **Fast** - No database latency  
✅ **Simple** - No configuration needed  
⚠️ **Temporary** - Data is lost when server restarts  

For production, extend the `database/db.py` module to use SQLite, PostgreSQL, or MongoDB.

## Code Architecture

### Clean & Modular Design

- **models/** - Data structures using Pydantic
- **routes/** - FastAPI endpoints (HTTP layer)
- **services/** - Business logic (AI detection, report generation, event management)
- **database/** - Data persistence (currently in-memory, extensible)

This separation makes the code easy to test and extend.

## Next Steps

1. ✅ Build the **React frontend** in `frontend/` to capture user events
2. ✅ Add comprehensive **unit tests** for detection logic
3. ✅ Integrate a **real database** (PostgreSQL recommended)
4. ✅ Add **authentication** (JWT tokens)
5. ✅ Deploy to **production** using Docker and AWS/Azure

## License

MIT License - Free to use and modify

## Support

For issues or questions, please refer to the `backend/context.md` file for project documentation.
