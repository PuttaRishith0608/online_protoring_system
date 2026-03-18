# Backend Development Guide

## Overview

The Online Proctoring System backend is built with **FastAPI**, a modern Python web framework that combines speed, ease of use, and built-in API documentation.

## Architecture

### Layered Architecture

```
┌─────────────────────────────────────┐
│      FastAPI Routes (HTTP Layer)    │
│   - activity.py (POST /log-event)   │
│   - report.py (GET /report/{id})    │
└────────────┬────────────────────────┘
             │
┌────────────▼────────────────────────┐
│  Services Layer (Business Logic)    │
│  - event_service.py (Storage)       │
│  - report_service.py (Reports)      │
│  - ai_detector.py (Detection)       │
│  - logger.py (Logging)              │
└────────────┬────────────────────────┘
             │
┌────────────▼────────────────────────┐
│   Models Layer (Data Structures)    │
│  - activity_model.py (Pydantic)     │
└────────────┬────────────────────────┘
             │
┌────────────▼────────────────────────┐
│   Storage Layer (In-Memory/Database)│
│  - event_store dict (Memory)        │
│  - db.py (Future: PostgreSQL)       │
└─────────────────────────────────────┘
```

## How It Works

### 1. Event Flow

```
Client → POST /log-event → activity.py → event_service.log_event() → event_store
                                                ↓
                                        Event stored in memory
```

### 2. Report Generation Flow

```
Client → GET /report/{user_id} → report.py → report_service.generate_report()
                                                      ↓
                                            ai_detector.check_ai_suspicion()
                                                      ↓
                                            Calculate integrity_score
                                                      ↓
                                              Return IntegrityReport
```

## File Descriptions

### Models (`models/`)

**activity_model.py**
- `LogEvent`: Pydantic model for incoming JSON requests
- `ActivityLog`: Internal model for storing events
- `IntegrityReport`: Model for API responses

Pydantic automatically validates and converts JSON to Python objects.

### Services (`services/`)

**event_service.py**
```python
# In-memory storage
event_store = {
    "user123": [ActivityLog(...), ActivityLog(...), ...],
    "user456": [ActivityLog(...), ...],
}
```
- `log_event()`: Add event to storage
- `get_events()`: Retrieve events for a user
- `get_all_events()`: Retrieve all events (admin)

**ai_detector.py**
- `check_ai_suspicion()`: Detect suspicious answer patterns
- `calculate_integrity_score()`: Compute overall integrity score

**report_service.py**
- `generate_report()`: Combine all data to create an integrity report

**logger.py**
- Utility functions for logging at different levels (info, error, warning, debug)

### Routes (`routes/`)

**activity.py**
- `POST /log-event`: Accept and store event
- `GET /events/{user_id}`: Debug endpoint to see all events for a user

**report.py**
- `GET /report/{user_id}`: Generate integrity report
- `GET /health`: Health check

### Database (`database/`)

**db.py**
- Currently a placeholder for future database integration
- Ready to add SQLite, PostgreSQL, or MongoDB support

## Key Concepts

### Pydantic Models

Pydantic automatically:
- ✅ Validates incoming data
- ✅ Converts JSON to Python objects
- ✅ Generates API documentation
- ✅ Serializes responses to JSON

```python
# Before: Raw dictionary
data = request.json()  # Unsafe, no validation

# After: Pydantic model
event = LogEvent(**request.json())  # Safe, validated
```

### In-Memory Storage

```python
# Storage is a simple dictionary
event_store = {}

# Storing events
event_store["user123"] = [log1, log2, log3]

# Retrieving events
user_events = event_store.get("user123", [])
```

**Advantages:**
- ⚡ Very fast
- 🔧 No setup required
- 📝 Easy to understand

**Disadvantages:**
- 💾 Data lost on restart
- 🔒 No persistence

### AI Detection Heuristic

The current heuristic is simple:
```python
if answer_length > 200 and time_taken < 10:
    mark_as_suspicious()
```

This can be enhanced to:
- Check for grammatical perfection vs. student's typical writing
- Detect plagiarism using similarity algorithms
- Use ML models for more accurate detection
- Check for common AI phrases

## Extending the Backend

### Adding a New Event Type

1. **Update detection logic** (`ai_detector.py`):
```python
def check_new_event(events):
    new_type_events = [e for e in events if e.event_type == "new_type"]
    count = len(new_type_events)
    return count
```

2. **Update report generation** (`report_service.py`):
```python
new_type_count = check_new_event(events)
```

3. **Update integrity score** (`ai_detector.py`):
```python
def calculate_integrity_score(..., new_type_count):
    total_suspicious = copy_paste_count + new_type_count + ...
    # ...
```

### Adding Database Support

1. **Replace in-memory storage** in `event_service.py`:
```python
# From:
event_store = {}

# To:
def log_event(user_id, event_type, timestamp, metadata):
    db.insert('events', {
        'user_id': user_id,
        'event_type': event_type,
        'timestamp': timestamp,
        'metadata': json.dumps(metadata)
    })
```

2. **Update data retrieval**:
```python
def get_events(user_id):
    return db.query('events', {'user_id': user_id})
```

### Adding Authentication

1. **Install JWT library**:
```bash
pip install python-jose
pip install passlib
```

2. **Add to app.py**:
```python
from fastapi import Depends
from fastapi.security import HTTPBearer

security = HTTPBearer()

@app.post("/log-event")
async def log_event(event: LogEvent, credentials = Depends(security)):
    # Verify token
    # Process event
    # ...
```

## Running Tests

```bash
# Test the API manually
python test_api.py

# Or use curl/Postman with the Swagger UI
# http://localhost:8000/docs
```

## Performance Considerations

### Current Performance
- Event logging: **O(1)** - Direct dictionary append
- Report generation: **O(n)** - Scan all events for user
- Memory usage: **O(n)** - Linear with number of events

### Scalability Tips

For large-scale deployment:

1. **Add caching**:
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_report(user_id):
    # Cache reports for frequently accessed users
```

2. **Use async operations**:
```python
from concurrent.futures import ThreadPoolExecutor
executor = ThreadPoolExecutor(max_workers=10)
```

3. **Add database indexing**:
```sql
CREATE INDEX idx_user_id ON events(user_id);
CREATE INDEX idx_event_type ON events(event_type);
```

## Debugging

### Enable Verbose Logging

```python
# In app.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Access Event Store

```python
# In Python shell
python
>>> from services import event_service
>>> print(event_service.event_store)
```

## Best Practices

✅ **Do:**
- Use type hints (helps with documentation and debugging)
- Write docstrings for functions
- Keep functions small and focused
- Use meaningful variable names
- Add logging for debugging

❌ **Don't:**
- Store sensitive data in metadata
- Make synchronous API calls to external services
- Ignore error handling
- Hardcode configuration values
- Skip input validation

## Next Steps

1. 🔐 Add JWT authentication
2. 💾 Integrate PostgreSQL database
3. 📊 Add analytics dashboard
4. 🧪 Write comprehensive unit tests
5. 🚀 Deploy using Docker and Kubernetes
6. 📈 Add rate limiting and monitoring

## Useful Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://pydantic-settings.readthedocs.io/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [REST API Best Practices](https://restfulapi.net/)
