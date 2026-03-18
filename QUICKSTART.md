# Quick Start Guide

Get the Online Proctoring System backend running in 3 minutes!

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- A terminal/command prompt

## Installation & Running

### Step 1: Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Start the Server

```bash
python app.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### Step 3: Test the API

Open your browser and go to:
- **Interactive API Docs**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc

## First API Call

### Using Swagger UI (Easiest)

1. Go to http://localhost:8000/docs
2. Click "Try it out" on the `/log-event` endpoint
3. Enter this in the Request body:

```json
{
  "user_id": "student1",
  "event_type": "copy_paste",
  "timestamp": 1647384720.123,
  "metadata": {
    "source": "exam_text"
  }
}
```

4. Click "Execute"
5. You should see status 200 with response: `{"status": "success", ...}`

### Using cURL

```bash
curl -X POST http://localhost:8000/log-event \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "student1",
    "event_type": "copy_paste",
    "timestamp": 1647384720.123,
    "metadata": {"source": "exam_text"}
  }'
```

### Using Python

```python
import requests

# Log an event
event = {
    "user_id": "student1",
    "event_type": "copy_paste",
    "timestamp": 1647384720.123,
    "metadata": {"source": "exam_text"}
}
response = requests.post("http://localhost:8000/log-event", json=event)
print(response.json())

# Get a report
response = requests.get("http://localhost:8000/report/student1")
print(response.json())
```

## Test with Sample Data

Run the included test script:

```bash
python test_api.py
```

This will:
- Log multiple events for test users
- Generate sample violations
- Show integrity reports
- Demonstrate AI detection

## Understanding the Response

### Successful Log Response
```json
{
  "status": "success",
  "message": "Event logged for user student1",
  "event_type": "copy_paste"
}
```

### Report Response
```json
{
  "user_id": "student1",
  "copy_paste_count": 2,           // Number of copy-paste events
  "tab_switch_count": 1,           // Number of tab switches
  "ai_suspicion_count": 0,         // Number of suspicious answers
  "integrity_score": "MEDIUM",     // HIGH / MEDIUM / LOW
  "details": {
    "total_events": 3,
    "event_types": ["copy_paste", "tab_switch"],
    "suspicious_answers": []
  }
}
```

## Common Issues

### "Connection refused" error

**Problem:** Cannot connect to server

**Solution:** Make sure the server is running:
```bash
python app.py
```

### "Module not found" error

**Problem:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:** Install dependencies:
```bash
pip install -r requirements.txt
```

### Port already in use

**Problem:** `Address already in use` on port 8000

**Solution:** Either:
1. Stop the other process using port 8000
2. Run on a different port:
```bash
uvicorn app:app --port 8001
```

## Connecting Frontend

Your React frontend can call these endpoints:

```javascript
// Log an event
await fetch('http://localhost:8000/log-event', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    user_id: userId,
    event_type: 'copy_paste',
    timestamp: Date.now() / 1000,
    metadata: { source: 'clipboard' }
  })
});

// Get report
await fetch(`http://localhost:8000/report/${userId}`)
  .then(r => r.json())
  .then(report => console.log(report.integrity_score));
```

## API Endpoint Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/log-event` | Log a user activity |
| GET | `/report/{user_id}` | Get integrity report |
| GET | `/events/{user_id}` | Get all events (debug) |
| GET | `/health` | Health check |

## Next Steps

1. ✅ Read [README.md](README.md) for full documentation
2. ✅ Read [BACKEND_GUIDE.md](../BACKEND_GUIDE.md) for architecture details
3. ✅ Build the React frontend in `frontend/` folder
4. ✅ Implement authentication for production
5. ✅ Add database persistence

## Useful Links

- 📖 [FastAPI Docs](https://fastapi.tiangolo.com/)
- 🧪 [Testing Guide](README.md#testing-the-api)
- 🏗️ [Architecture Guide](../BACKEND_GUIDE.md)

---

**Need help?** Check the full README.md for detailed API documentation and examples.
