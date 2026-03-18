# System Architecture & Overview

Complete documentation of the Online Proctoring System architecture, data flow, and components.

## System Overview

The Online Proctoring System is a full-stack web application designed to detect academic integrity violations during online exams.

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     STUDENT BROWSER                              │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │          React Frontend (Exam & Report Pages)           │   │
│  │                                                          │   │
│  │  • Display exam questions                               │   │
│  │  • Track user events (copy, tab switch, typing)         │   │
│  │  • Send events to backend                               │   │
│  │  • Display integrity reports                            │   │
│  └──────────────┬───────────────────────────────────────────┘   │
└─────────────────┼──────────────────────────────────────────────────┘
                  │
        HTTP/REST │ API Calls
                  │
        ┌─────────▼──────────────────────────────────────────┐
        │                                                    │
        │         FASTAPI BACKEND (Python)                  │
        │                                                    │
        │  ┌────────────────────────────────────────────┐   │
        │  │         HTTP Routes Layer                 │   │
        │  │                                            │   │
        │  │  POST /log-event                          │   │
        │  │  GET  /report/{user_id}                   │   │
        │  │  GET  /events/{user_id}                   │   │
        │  │  GET  /health                             │   │
        │  └────────────┬─────────────────────────────┘   │
        │               │                                  │
        │  ┌────────────▼─────────────────────────────┐   │
        │  │     Services Layer (Business Logic)     │   │
        │  │                                          │   │
        │  │  • event_service.py (store events)      │   │
        │  │  • report_service.py (generate reports) │   │
        │  │  • ai_detector.py (detect suspicions)   │   │
        │  │  • logger.py (logging)                  │   │
        │  └────────────┬─────────────────────────────┘   │
        │               │                                  │
        │  ┌────────────▼─────────────────────────────┐   │
        │  │    Data Models (Pydantic)               │   │
        │  │                                          │   │
        │  │  • LogEvent (incoming requests)         │   │
        │  │  • ActivityLog (stored events)          │   │
        │  │  • IntegrityReport (responses)          │   │
        │  └────────────┬─────────────────────────────┘   │
        │               │                                  │
        │  ┌────────────▼─────────────────────────────┐   │
        │  │    Storage Layer (In-Memory)            │   │
        │  │                                          │   │
        │  │  event_store = {                        │   │
        │  │    "user_123": [log1, log2, ...],       │   │
        │  │    "user_456": [log3, log4, ...]        │   │
        │  │  }                                       │   │
        │  └────────────────────────────────────────┘   │
        │                                                │
        └────────────────────────────────────────────────┘
```

## Data Flow

### 1. Event Logging Flow

```
Student Takes Exam
    │
    ├─ Copies text → window.addEventListener('copy')
    │                      │
    │                      └─ logEvent('copy_paste', ...)
    │
    ├─ Switches tab → window.addEventListener('blur')
    │                      │
    │                      └─ logEvent('tab_switch', ...)
    │
    └─ Submits answer → handleSubmitExam()
                              │
                              └─ logEvent('answer_submission', ...)

                              │
                              │ (All events)
                              ▼
                    
            POST /log-event
                │
                └─► event_service.log_event()
                    {
                      "user_id": "student_001",
                      "event_type": "copy_paste",
                      "timestamp": 1647384720.123,
                      "metadata": {...}
                    }
                    │
                    └─► Store in event_store
                        event_store["student_001"].append(log)
```

### 2. Report Generation Flow

```
Student Clicks "Get Report"
    │
    └─ GET /report/student_001
        │
        ├─► event_service.get_events("student_001")
        │   Returns: [log1, log2, log3, ...]
        │
        ├─► report_service.generate_report()
        │   
        │   ├─ Count copy_paste events
        │   │  copy_paste_count = 2
        │   │
        │   ├─ Count tab_switch events
        │   │  tab_switch_count = 3
        │   │
        │   ├─ ai_detector.check_ai_suspicion()
        │   │  For each answer_submission event:
        │   │    If length > 200 AND time < 10 seconds:
        │   │      ai_suspicion_count += 1
        │   │  Result: ai_suspicion_count = 1
        │   │
        │   └─ ai_detector.calculate_integrity_score()
        │      total = 2 + 3 + 1 = 6
        │      If total <= 3: "MEDIUM"
        │      If total > 3: "LOW"
        │      Result: integrity_score = "LOW"
        │
        └─► Return IntegrityReport
            {
              "user_id": "student_001",
              "copy_paste_count": 2,
              "tab_switch_count": 3,
              "ai_suspicion_count": 1,
              "integrity_score": "LOW",
              "details": {...}
            }
            │
            └─► Display in React ReportPage
```

## API Endpoints

### POST /log-event

**Purpose:** Log a user activity event

**Request:**
```json
{
  "user_id": "student_001",
  "event_type": "copy_paste",
  "timestamp": 1647384720.123,
  "metadata": {
    "source": "exam_text",
    "destination": "answer_field"
  }
}
```

**Response (200):**
```json
{
  "status": "success",
  "message": "Event logged for user student_001",
  "event_type": "copy_paste"
}
```

**Error Response (400):**
```json
{
  "detail": "Error logging event: ..."
}
```

---

### GET /report/{user_id}

**Purpose:** Get integrity report for a user

**URL:** `GET /report/student_001`

**Response (200):**
```json
{
  "user_id": "student_001",
  "copy_paste_count": 2,
  "tab_switch_count": 3,
  "ai_suspicion_count": 1,
  "integrity_score": "LOW",
  "details": {
    "total_events": 6,
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

### GET /events/{user_id}

**Purpose:** Get all events for a user (debug endpoint)

**URL:** `GET /events/student_001`

**Response:**
```json
{
  "user_id": "student_001",
  "event_count": 6,
  "events": [
    {
      "event_type": "copy_paste",
      "timestamp": 1647384720.123,
      "metadata": {"source": "exam_text"}
    },
    {
      "event_type": "tab_switch",
      "timestamp": 1647384725.456,
      "metadata": {"new_tab": "google.com"}
    },
    ...
  ]
}
```

---

### GET /health

**Purpose:** Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "message": "Proctoring system backend is running"
}
```

## Event Types

### copy_paste

Triggered when user copies text (Ctrl+C / Cmd+C)

```json
{
  "event_type": "copy_paste",
  "timestamp": 1647384720.123,
  "metadata": {
    "source": "exam_text",
    "destination": "answer_field"
  }
}
```

### tab_switch

Triggered when user leaves or returns to exam window

```json
{
  "event_type": "tab_switch",
  "timestamp": 1647384725.456,
  "metadata": {
    "event": "user_switched_to_different_tab"
  }
}
```

### answer_submission

Triggered when user submits answers

```json
{
  "event_type": "answer_submission",
  "timestamp": 1647384780.000,
  "metadata": {
    "question_id": "q1",
    "answer": "Student's answer text...",
    "time_taken_seconds": 45,
    "answer_length": 180
  }
}
```

### keyboard_input (optional)

For tracking keyboard activity

```json
{
  "event_type": "keyboard_input",
  "timestamp": 1647384750.000,
  "metadata": {
    "key": "a",
    "field": "answer_textarea"
  }
}
```

## AI Detection Algorithm

### Heuristic: Answer Length & Speed

```python
def check_ai_suspicion(events):
    for event in events:
        if event.event_type == "answer_submission":
            answer_text = event.metadata.get("answer", "")
            time_taken = event.metadata.get("time_taken_seconds", 0)
            
            # Red flags
            if len(answer_text) > 200 and time_taken < 10:
                # Suspicious: Long, high-quality answer in < 10 seconds
                mark_as_suspicious()
```

### Why This Works

1. **Length > 200 characters**
   - Indicates detailed, comprehensive answer
   - Difficult to write this quickly naturally
   - Common for copy-paste or AI

2. **Time < 10 seconds**
   - Extreme speed for 200+ character answer
   - Average typing speed: 40-60 WPM
   - 200 chars ≈ 40 words ≈ 30-45 seconds minimum
   - Less than 10 seconds is unrealistic

### Future Enhancements

- Vocabulary complexity analysis
- Grammatical perfection detection
- Plagiarism scoring
- Machine learning models
- Semantic analysis

## In-Memory Data Structure

### Event Store

```python
event_store = {
    "student_001": [
        ActivityLog(
            user_id="student_001",
            event_type="copy_paste",
            timestamp=1647384720.123,
            metadata={"source": "exam_text"}
        ),
        ActivityLog(
            user_id="student_001",
            event_type="tab_switch",
            timestamp=1647384725.456,
            metadata={"new_tab": "google.com"}
        ),
        ...
    ],
    "student_002": [
        ...
    ]
}
```

### Memory Complexity

- **Space:** O(n) where n = total number of events
- **Time to add:** O(1) - Direct append
- **Time to retrieve:** O(1) - Direct lookup
- **Report generation:** O(n) - Scan all events for user

## Integrity Score Calculation

### Algorithm

```python
def calculate_integrity_score(copy_paste_count, tab_switch_count, ai_suspicion_count):
    total_violations = copy_paste_count + tab_switch_count + ai_suspicion_count
    
    if total_violations == 0:
        return "HIGH"      # No violations
    elif total_violations <= 3:
        return "MEDIUM"    # Minor violations
    else:
        return "LOW"       # Multiple violations
```

### Scoring Table

| Score | Total Violations | Meaning |
|-------|------------------|---------|
| HIGH | 0 | ✅ Legitimate exam, no violations |
| MEDIUM | 1-3 | ⚠️ Minor violations, review needed |
| LOW | 4+ | ❌ Multiple violations, exam compromised |

### Example Scenarios

**Scenario 1: Clean Exam**
- Copy-paste: 0
- Tab switches: 0
- AI suspicions: 0
- **Total: 0 → Score: HIGH** ✅

**Scenario 2: Minor Violations**
- Copy-paste: 1
- Tab switches: 1
- AI suspicions: 0
- **Total: 2 → Score: MEDIUM** ⚠️

**Scenario 3: Serious Violations**
- Copy-paste: 2
- Tab switches: 3
- AI suspicions: 2
- **Total: 7 → Score: LOW** ❌

## Technology Stack

### Backend
- **Framework:** FastAPI (Python web framework)
- **Server:** Uvicorn (ASGI server)
- **Data Validation:** Pydantic (type checking)
- **Async:** Built-in async/await support

### Frontend
- **Framework:** React 18 (JavaScript UI library)
- **State Management:** React Hooks (useState, useEffect)
- **Communication:** Fetch API (HTTP client)
- **Styling:** CSS3 with flexbox/grid

### Storage (Current)
- **In-Memory:** Python dictionaries
- **Future:** PostgreSQL, MongoDB, SQLite

## Deployment Diagram

```
Production Deployment
┌─────────────────────────────────────────────────────┐
│                    Internet                         │
└────────────────────┬────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
    ┌───▼──────────┐      ┌──────▼───────────┐
    │ Frontend CDN │      │  API Gateway     │
    │ (React)      │      │  (Load Balancer) │
    └──────────────┘      └────────┬─────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
            ┌───────▼────────┐        ┌────────▼───────┐
            │  Backend Pod 1 │        │ Backend Pod 2  │
            │  (FastAPI)     │        │ (FastAPI)      │
            └───────┬────────┘        └────────┬───────┘
                    │                         │
                    └──────────┬──────────────┘
                               │
                    ┌──────────▼──────────┐
                    │  Database Service  │
                    │  (PostgreSQL)      │
                    │      OR            │
                    │  Memory Cache      │
                    │  (Redis)           │
                    └────────────────────┘
```

## Performance Characteristics

### Current (In-Memory)
- Event logging: **Sub-millisecond**
- Report generation: **10-100ms** (depends on event count)
- Memory usage: **~1KB per event**
- Scalability: **~1M events OK on modern machine**

### Future (Database)
- Event logging: **5-20ms** (network + DB)
- Report generation: **50-500ms** (with query optimization)
- Memory usage: **~100MB for 1M events** (DB indexed)
- Scalability: **Unlimited with sharding**

## Security Considerations

### Current System
- ⚠️ No authentication
- ⚠️ No authorization
- ⚠️ No encryption
- ⚠️ No rate limiting

### For Production
- Add JWT authentication
- Add role-based access control (RBAC)
- Use HTTPS/TLS encryption
- Implement rate limiting
- Add input validation
- Sanitize user inputs
- Use environment variables for secrets
- Add audit logging

## Error Handling

### Frontend
```javascript
try {
  const report = await api.getIntegrityReport(userId);
} catch (error) {
  setError("Failed to fetch report");
  console.error(error);
}
```

### Backend
```python
@router.post("/log-event")
async def log_event(event: LogEvent):
    try:
        # Process event
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
```

## Testing Strategy

### Unit Tests (TODO)
```python
def test_copy_paste_count():
    events = [copy_paste_event, copy_paste_event]
    report = generate_report("user1", events)
    assert report.copy_paste_count == 2

def test_ai_detection():
    events = [
        {
            "event_type": "answer_submission",
            "metadata": {"answer": "x" * 250, "time_taken_seconds": 5}
        }
    ]
    suspicions = check_ai_suspicion(events)
    assert len(suspicions) == 1
```

### Integration Tests (TODO)
```javascript
test('Complete exam flow', async () => {
  // Login
  // Answer questions
  // Tab switch
  // Copy text
  // Submit exam
  // Check report
});
```

### Load Tests (TODO)
```
- Simulate 1000 concurrent students
- 100 events per student
- Measure response times
- Monitor memory usage
```

---

**This document describes the complete system architecture and should be kept up-to-date as the system evolves.**
