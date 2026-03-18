# 📊 Copy-Paste Detection - Visual Flow

## Event Detection Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    STUDENT BROWSER                           │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           Exam Page (React Component)               │  │
│  │                                                      │  │
│  │  Student Types Answer or Tries to Copy/Paste        │  │
│  │           ↓                                          │  │
│  │  ┌────────────────────────────────────────────────┐ │  │
│  │  │  Event Listener Catches:                       │ │  │
│  │  │  - 'copy' event (Ctrl+C or right-click)       │ │  │
│  │  │  - 'paste' event (Ctrl+V or right-click)      │ │  │
│  │  │  - 'cut' event (Ctrl+X)                        │ │  │
│  │  │  - 'keydown' event (keyboard shortcuts)        │ │  │
│  │  └─────────────┬──────────────────────────────────┘ │  │
│  │               ↓                                       │  │
│  │  ┌────────────────────────────────────────────────┐ │  │
│  │  │ Event Handler:                                 │ │  │
│  │  │ 1. e.preventDefault() - Block operation        │ │  │
│  │  │ 2. console.warn() - Log to console with ⚠️     │ │  │
│  │  │ 3. alert() - Warn user                         │ │  │
│  │  │ 4. setCopyCounts() - Increment counter         │ │  │
│  │  │ 5. logEvent() - Send to backend                │ │  │
│  │  └─────────────┬──────────────────────────────────┘ │  │
│  │               ↓                                       │  │
│  │  ┌────────────────────────────────────────────────┐ │  │
│  │  │ Visual Feedback:                               │ │  │
│  │  │ ❌ Alert popup appears                          │ │  │
│  │  │ 📋 Copy Events: N counter increases             │ │  │
│  │  │ 📅 Event appears in Event Log                   │ │  │
│  │  └────────────────────────────────────────────────┘ │  │
│  └──────────────────────────────────────────────────────┘  │
└───────────────────────┬─────────────────────────────────────┘
                        │
                 HTTP POST Request
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                    BACKEND (Python FastAPI)                │
│                                                              │
│  POST /log-event                                           │
│      ↓                                                      │
│  ┌────────────────────────────────────────────────────┐   │
│  │ Request Body:                                      │   │
│  │ {                                                  │   │
│  │   "user_id": "student_001",                        │   │
│  │   "event_type": "copy_paste",                      │   │
│  │   "timestamp": 1710766800.123,                     │   │
│  │   "metadata": {                                    │   │
│  │     "operation": "copy",  // or "paste" or "cut"   │   │
│  │     "source": "keyboard_ctrl_c"                    │   │
│  │   }                                                │   │
│  │ }                                                  │   │
│  └────────────┬─────────────────────────────────────┘   │
│               ↓                                            │
│  ┌────────────────────────────────────────────────────┐   │
│  │ event_service.log_event()                          │   │
│  │ Stores event in event_store dict                   │   │
│  │                                                    │   │
│  │ event_store["student_001"].append({event log})    │   │
│  └────────────┬─────────────────────────────────────┘   │
│               ↓                                            │
│  ┌────────────────────────────────────────────────────┐   │
│  │ Response (200 OK):                                 │   │
│  │ {                                                  │   │
│  │   "status": "success",                             │   │
│  │   "message": "Event logged",                       │   │
│  │   "event_type": "copy_paste"                       │   │
│  │ }                                                  │   │
│  └────────────────────────────────────────────────────┘   │
└───────────────────────┬─────────────────────────────────────┘
                        │
             Events stored in memory
                        │
                        ▼
               GET /report/{user_id}
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                  Report Generation                          │
│                                                              │
│  ┌────────────────────────────────────────────────────┐   │
│  │ Analyze all events for user_001:                   │   │
│  │                                                    │   │
│  │ for each event:                                    │   │
│  │   if event_type == "copy_paste":                   │   │
│  │     copy_paste_count += 1                          │   │
│  │   if event_type == "tab_switch":                   │   │
│  │     tab_switch_count += 1                          │   │
│  │   if event_type == "answer_submission":            │   │
│  │     check_ai_suspicion()                           │   │
│  │       if answer_length > 200 && time < 10s:        │   │
│  │         ai_suspicion_count += 1                    │   │
│  │                                                    │   │
│  │ total_violations = copy_paste + tab_switch + ai    │   │
│  │                                                    │   │
│  │ if total_violations == 0:                          │   │
│  │   integrity_score = "HIGH"  ✅                      │   │
│  │ elif total_violations <= 3:                        │   │
│  │   integrity_score = "MEDIUM" ⚠️                    │   │
│  │ else:                                              │   │
│  │   integrity_score = "LOW" ❌                        │   │
│  └────────────┬─────────────────────────────────────┘   │
│               ↓                                            │
│  ┌────────────────────────────────────────────────────┐   │
│  │ Return Integrity Report:                           │   │
│  │ {                                                  │   │
│  │   "user_id": "student_001",                        │   │
│  │   "copy_paste_count": 5,                           │   │
│  │   "tab_switch_count": 2,                           │   │
│  │   "ai_suspicion_count": 0,                         │   │
│  │   "integrity_score": "LOW",                        │   │
│  │   "details": { ... }                               │   │
│  │ }                                                  │   │
│  └────────────────────────────────────────────────────┘   │
└───────────────────────┬─────────────────────────────────────┘
                        │
           Back to Browser for Display
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                  Report Page (React)                        │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Integrity Report for student_001                  │  │
│  │                                                     │  │
│  │  ┌──────────────────────────────────────────────┐  │  │
│  │  │ Integrity Score: LOW ❌                       │  │  │
│  │  └──────────────────────────────────────────────┘  │  │
│  │                                                     │  │
│  │  📋 Copy-Paste Events: 5                           │  │
│  │  📑 Tab Switches: 2                                │  │
│  │  🤖 AI Suspicions: 0                               │  │
│  │  🎯 Total Events: 7                                │  │
│  │                                                     │  │
│  │  ⚠️ Multiple violations detected                    │  │
│  │  ❌ Exam integrity compromised                      │  │
│  └──────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────┘
```

## Detailed Copy Event Flow

```
┌─────────────────────────────────────────────────────────────┐
│            COPY EVENT DETECTION FLOW                        │
└─────────────────────────────────────────────────────────────┘

USER ACTION: Student presses Ctrl+C
        ↓
┌─────────────────────────────────────────┐
│ Browser detects 'keydown' event         │
│ Event properties:                       │
│  - e.key = 'c'                          │
│  - e.ctrlKey = true (or e.metaKey on Mac)
└────────────┬────────────────────────────┘
             ↓
┌─────────────────────────────────────────┐
│ React event listener catches it         │
│ (Using capture phase: true)             │
└────────────┬────────────────────────────┘
             ↓
┌─────────────────────────────────────────┐
│ handleKeyDown() function called         │
│                                         │
│ Check condition:                        │
│ (e.ctrlKey || e.metaKey) && e.key==='c' │
│ Result: TRUE                            │
└────────────┬────────────────────────────┘
             ↓
┌─────────────────────────────────────────┐
│ 1. e.preventDefault()                   │
│    Browser no longer executes copy      │
│                                         │
│ 2. console.warn('⚠️ COPY DETECTED...')   │
│    Console logs with warning emoji      │
│                                         │
│ 3. logEvent('copy_paste', {...})        │
│    Prepares event object with metadata  │
│                                         │
│ 4. setCopyCounts(prev => prev + 1)      │
│    Increments counter (triggers re-render)
│                                         │
│ 5. alert('❌ Copy is not allowed...')    │
│    Shows popup alert to user            │
└────────────┬────────────────────────────┘
             ↓
┌─────────────────────────────────────────┐
│ logEvent() function:                    │
│                                         │
│ console.log('📤 Sending event...')       │
│                                         │
│ await api.logEvent(userId, eventType,   │
│    metadata)                            │
│                                         │
│ Makes HTTP POST request to backend      │
│ URL: http://localhost:8000/log-event    │
│ Body: {                                 │
│   user_id: 'student_001',              │
│   event_type: 'copy_paste',            │
│   timestamp: 1710766800.123,           │
│   metadata: {                           │
│     operation: 'copy',                  │
│     source: 'keyboard_ctrl_c',         │
│     timestamp: '2026-03-18T...'        │
│   }                                     │
│ }                                       │
└────────────┬────────────────────────────┘
             ↓
┌─────────────────────────────────────────┐
│ Backend processes request:              │
│                                         │
│ event_service.log_event()               │
│ Stores in event_store dict              │
│                                         │
│ Returns: {                              │
│   "status": "success",                  │
│   "message": "Event logged"             │
│ }                                       │
└────────────┬────────────────────────────┘
             ↓
┌─────────────────────────────────────────┐
│ UI Updates:                             │
│                                         │
│ 1. Alert popup disappears (user closes) │
│                                         │
│ 2. Copy Events counter updates:        │
│    📋 Copy Events: 1 → 2                │
│                                         │
│ 3. Event Log displays:                  │
│    ⏰ 14:30:00                          │
│    ⚠️ copy_paste                        │
│                                         │
│ 4. Console shows:                       │
│    ✓ Event logged successfully          │
└─────────────────────────────────────────┘
```

## Event Types & Metadata Reference

```
┌─────────────────────────────────────────────────────────────┐
│                    EVENT STRUCTURE                          │
└─────────────────────────────────────────────────────────────┘

Base Event Structure (sent to backend):
{
  "user_id": string,
  "event_type": string,
  "timestamp": float (Unix timestamp),
  "metadata": object
}

EVENT TYPES:
─────────────────────────────────────────────────────────────

1. COPY_PASTE EVENT
   event_type: "copy_paste"
   
   Variations:
   a) Keyboard Ctrl+C:
      metadata: {
        operation: "copy",
        source: "keyboard_ctrl_c",
        timestamp: ISO string
      }
   
   b) Keyboard Ctrl+V:
      metadata: {
        operation: "paste",
        source: "keyboard_ctrl_v",
        timestamp: ISO string
      }
   
   c) Keyboard Ctrl+X:
      metadata: {
        operation: "cut",
        source: "keyboard_ctrl_x",
        timestamp: ISO string
      }
   
   d) Right-click Copy:
      metadata: {
        operation: "copy",
        source: "copy_event",
        timestamp: ISO string
      }
   
   e) Right-click Paste:
      metadata: {
        operation: "paste",
        source: "paste_event",
        timestamp: ISO string
      }
   
   f) Right-click Cut:
      metadata: {
        operation: "cut",
        source: "cut_event",
        timestamp: ISO string
      }

2. TAB_SWITCH EVENT
   event_type: "tab_switch"
   metadata: {
     event: "user_switched_to_different_tab",
     timestamp: ISO string
   }

3. ANSWER_SUBMISSION EVENT
   event_type: "answer_submission"
   metadata: {
     question_id: string,
     answer: string,
     time_taken_seconds: number,
     answer_length: number
   }
```

## Browser Event Listener Chain

```
┌─────────────────────────────────────────────────────┐
│           EVENT LISTENER REGISTRATION               │
└─────────────────────────────────────────────────────┘

When Exam Page mounts (useEffect hook runs):

document.addEventListener('copy', handleCopy, true)
  ↓
  Listens for any 'copy' event in the document
  Capture phase = true means it catches event early
  Even if event.stopPropagation() is called elsewhere

document.addEventListener('paste', handlePaste, true)
  ↓
  Listens for any 'paste' event
  Works with right-click paste, Ctrl+V, etc.

document.addEventListener('cut', handleCut, true)
  ↓
  Listens for any 'cut' event
  Catches Ctrl+X and right-click cut

document.addEventListener('keydown', handleKeyDown, true)
  ↓
  Listens for keyboard key press
  Checks for Ctrl+C, Ctrl+V, Ctrl+X combinations
  Also checks e.metaKey for Mac (Cmd key)

window.addEventListener('blur', handleBlur)
  ↓
  Listens when user leaves window
  Detects tab switch or app switch

window.addEventListener('focus', handleFocus)
  ↓
  Listens when user returns to window
  Just logs, doesn't penalize

┌─────────────────────────────────────────────────────┐
│           CLEANUP ON COMPONENT UNMOUNT              │
└─────────────────────────────────────────────────────┘

When Exam Page unmounts (return from useEffect):

document.removeEventListener('copy', handleCopy, true)
document.removeEventListener('paste', handlePaste, true)
document.removeEventListener('cut', handleCut, true)
document.removeEventListener('keydown', handleKeyDown, true)
window.removeEventListener('blur', handleBlur)
window.removeEventListener('focus', handleFocus)

All listeners properly cleaned up to prevent memory leaks
```

## Response Timing Diagram

```
TIME →

0ms:  Student presses Ctrl+C
      ↓
5ms:  Event caught by listener
10ms: e.preventDefault() executed
15ms: alert() shown
      console logged
20ms: logEvent() called
      setCopyCounts() updates state
25ms: HTTP POST request sent to backend
      ↓
30ms: Backend receives request
35ms: event_service.log_event() processes
40ms: Response returned (200 OK)
      ↓
45ms: Browser receives response
      console.log('✓ Event logged')
50ms: React re-renders with new count
      UI displays:
      - Updated counter (📋 Copy Events: N)
      - New event in Event Log
      - Alert still visible
      ↓
100ms: User closes alert (presses OK)
      Flow complete
```

## Integrity Score Calculation

```
All Events for User
        ↓
Count by Type:
  ├── copy_paste_count (copy, paste, cut events)
  ├── tab_switch_count (tab switches)
  └── ai_suspicion_count (long answers submitted fast)
        ↓
Calculate Total Violations:
  total = copy_paste + tab_switch + ai_suspicion
        ↓
Determine Score:
  
  if (total == 0)    → "HIGH" ✅
     No violations detected
     Exam appears legitimate
     
  if (1-3)           → "MEDIUM" ⚠️
     Minor violations
     Review recommended
     
  if (4+)            → "LOW" ❌
     Multiple violations
     Exam integrity compromised
```

---

This visual guide shows the complete flow of copy-paste detection from user action to integrity score!
