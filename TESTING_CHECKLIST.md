# ✅ Copy-Paste Detection - Testing Checklist

Use this checklist to verify all copy-paste detection features are working correctly.

## Prerequisites Setup

- [ ] Clone/have the project ready at: `c:\Users\putta\Desktop\vsproject\edwisely-r1\online-proctoring-system`
- [ ] Backend folder exists with Python files
- [ ] Frontend folder exists with React files
- [ ] Python installed (3.8+)
- [ ] Node.js & npm installed
- [ ] Git command line available

## Backend Setup

- [ ] Navigate to backend folder: `cd backend`
- [ ] Create Python virtual environment: `python -m venv venv`
- [ ] Activate virtual environment: `venv\Scripts\activate` (Windows)
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Start backend: `python app.py`
- [ ] Verify output shows: `Uvicorn running on http://127.0.0.1:8000`
- [ ] Backend health check: `curl http://localhost:8000/health`
- [ ] Expected response: `{"status": "running"}`

## Frontend Setup

- [ ] Navigate to frontend folder: `cd frontend`
- [ ] Install npm packages: `npm install`
- [ ] Start frontend development server: `npm start`
- [ ] Verify browser opens to: `http://localhost:3000`
- [ ] UI loads without errors
- [ ] No red error messages in console

## Functional Testing

### Test 1: Basic Page Load
- [ ] ExamPage component displays correctly
- [ ] Student ID shows in the interface
- [ ] "Exam Question" visible in question area
- [ ] Input field for answer is present
- [ ] Event Log section visible below
- [ ] Copy Events counter shows "0"
- [ ] Paste Events counter shows "0"
- [ ] Cut Events counter shows "0"
- [ ] Tab Switches counter shows "0"

### Test 2: Check Browser Console
- [ ] Open DevTools: Press `F12`
- [ ] Switch to Console tab
- [ ] Refresh page (F5)
- [ ] Expected logs appear:
  - [ ] `🔧 Setting up event listeners...`
  - [ ] `✓ Copy listener attached`
  - [ ] `✓ Paste listener attached`
  - [ ] `✓ Cut listener attached`
  - [ ] `✓ Keyboard listener attached`
  - [ ] `✓ All event listeners registered successfully`

### Test 3: Detect Ctrl+C (Copy)
- [ ] Click in the answer input field
- [ ] Select some text: `Ctrl+A` (select all)
- [ ] Try to copy: Press `Ctrl+C`
- [ ] Verify alert appears: "❌ Copy policy violation detected!"
- [ ] Click OK to close alert
- [ ] Console shows: `⚠️ KEYBOARD SHORTCUT DETECTED - Ctrl+C`
- [ ] Console shows: `📤 Sending event to backend: copy_paste`
- [ ] UI updates: "📋 Copy Events: 1"
- [ ] Event appears in Event Log with timestamp

### Test 4: Detect Ctrl+V (Paste)
- [ ] Press `Ctrl+V` in the answer field
- [ ] Verify alert appears: "❌ Paste operation (Ctrl+V) is not allowed during exam!"
- [ ] Click OK to close alert
- [ ] Console shows: `⚠️ KEYBOARD SHORTCUT DETECTED - Ctrl+V`
- [ ] Console shows: `📤 Sending event to backend: copy_paste`
- [ ] UI updates: "📋 Paste Events: 1"
- [ ] Event appears in Event Log with different timestamp

### Test 5: Detect Ctrl+X (Cut)
- [ ] Select text in the answer field
- [ ] Press `Ctrl+X`
- [ ] Verify alert appears
- [ ] Click OK to close alert
- [ ] Console shows: `⚠️ KEYBOARD SHORTCUT DETECTED - Ctrl+X`
- [ ] Console shows: `📤 Sending event to backend: copy_paste`
- [ ] UI updates: "📋 Cut Events: 1"
- [ ] Event appears in Event Log

### Test 6: Detect Right-Click Copy
- [ ] Click in the answer field
- [ ] Select some text
- [ ] Right-click → Select "Copy"
- [ ] Verify alert appears: "❌ Copy policy violation detected!"
- [ ] Click OK to close alert
- [ ] Console shows: `⚠️ Copy operation detected!`
- [ ] UI updates: "📋 Copy Events: 2" (incremented from previous)
- [ ] Event logged to backend

### Test 7: Detect Right-Click Paste
- [ ] Right-click in the answer field
- [ ] Select "Paste" from context menu
- [ ] Verify alert appears
- [ ] Click OK to close alert
- [ ] Console shows appropriate warning
- [ ] UI updates: "📋 Paste Events: 2" (incremented)
- [ ] Event logged to backend

### Test 8: Detect Right-Click Cut
- [ ] Select text in the answer field
- [ ] Right-click → Select "Cut"
- [ ] Verify alert appears
- [ ] Click OK to close alert
- [ ] UI updates: "📋 Cut Events: 2"

### Test 9: Tab Switch Detection
- [ ] Click "Report" in navigation (or stay on Exam)
- [ ] Click back to "Exam" page
- [ ] Watch for blur/focus events in console
- [ ] If tab switch happens: "📋 Tab Switches: 1"
- [ ] Optional: Switch to a different browser tab and back
- [ ] Tab switch should be detected

### Test 10: Event Log Display
- [ ] Verify Event Log shows all attempted operations
- [ ] Each entry should have:
  - [ ] Timestamp (HH:MM:SS format)
  - [ ] Event type (copy_paste, tab_switch, etc.)
  - [ ] Operation type (copy, paste, cut, etc.)
  - [ ] Source (keyboard_ctrl_c, paste_event, etc.)
- [ ] Entries appear in chronological order

## Backend API Testing

### Test 11: Verify Events Stored
- [ ] Open terminal/PowerShell
- [ ] Run: `curl http://localhost:8000/events/student_001`
- [ ] Expected: JSON array with all events logged
- [ ] Each event should contain:
  - [ ] `user_id`: "student_001"
  - [ ] `event_type`: "copy_paste"
  - [ ] `timestamp`: Unix timestamp
  - [ ] `metadata`: Object with operation, source, timestamp

### Test 12: Check Copy-Paste Count in Report
- [ ] Run: `curl http://localhost:8000/report/student_001`
- [ ] Expected response includes:
  - [ ] `"copy_paste_count"`: Should match your violations
  - [ ] `"tab_switch_count"`: Number of tab switches
  - [ ] `"ai_suspicion_count"`: 0 (unless submitted long answers fast)
  - [ ] `"integrity_score"`: Based on total violations

### Test 13: Integrity Score Calculation
After performing multiple violations:
- [ ] 0 violations → Score should be "HIGH" ✅
- [ ] 1-3 violations → Score should be "MEDIUM" ⚠️
- [ ] 4+ violations → Score should be "LOW" ❌

Expected example after your tests:
```
curl http://localhost:8000/report/student_001
```
Response:
```json
{
  "user_id": "student_001",
  "copy_paste_count": 5,
  "tab_switch_count": 1,
  "ai_suspicion_count": 0,
  "integrity_score": "LOW",
  "details": { ... }
}
```

## Console Message Verification

### Verify Console Shows All Message Types

- [ ] **Setup Messages** (on page load):
  - `🔧 Setting up event listeners...`
  - `✓ Copy listener attached`
  - `✓ Paste listener attached`

- [ ] **Detection Messages** (on violations):
  - `⚠️ KEYBOARD SHORTCUT DETECTED - Ctrl+C`
  - `⚠️ KEYBOARD SHORTCUT DETECTED - Ctrl+V`
  - `⚠️ KEYBOARD SHORTCUT DETECTED - Ctrl+X`
  - `⚠️ Copy operation detected!`
  - `⚠️ Paste operation detected!`
  - `⚠️ Cut operation detected!`

- [ ] **Sending Messages** (logging):
  - `📤 Sending event to backend: copy_paste`

- [ ] **Success Messages**:
  - `✓ Event logged successfully: copy_paste`

- [ ] **No Error Messages** (should not see):
  - [ ] ❌ "TypeError: Cannot read property..."
  - [ ] ❌ "ReferenceError: handleCopy is not defined"
  - [ ] ❌ Red error messages in console

## Edge Cases & Stress Testing

### Test 14: Rapid Consecutive Actions
- [ ] Press Ctrl+C multiple times quickly (3-5 times)
- [ ] Verify each press triggers alert and counter increments
- [ ] All events appear in Event Log
- [ ] No JavaScript errors in console

### Test 15: Page Refresh
- [ ] Perform copy violation
- [ ] Refresh page (F5)
- [ ] Note: Old events will be lost (in-memory storage)
- [ ] New event log starts at 0
- [ ] Listeners re-attach (verify in console)

### Test 16: Mixed Operations
- [ ] Perform sequence: Ctrl+C → Ctrl+V → Ctrl+X → Right-click Copy
- [ ] Verify all 4 violations logged
- [ ] UI shows counters updated correctly
- [ ] Total should be reflected in integrity report

### Test 17: Long Duration Test
- [ ] Leave exam page open for several minutes
- [ ] Perform occasional copy-paste attempts
- [ ] Verify listeners don't stop working
- [ ] Events continue to log

## Report Page Verification

### Test 18: Navigate to Report Page
- [ ] Click "Report" button/link in navigation
- [ ] ReportPage component loads without errors
- [ ] Shows title: "Integrity Report for student_001"

### Test 19: Report Displays Correct Data
- [ ] Copy-Paste Count: Shows number of violations
- [ ] Tab Switches: Shows number of tab switches
- [ ] AI Suspicions: Shows 0 (unless applicable)
- [ ] Integrity Score: Shows HIGH/MEDIUM/LOW status
- [ ] Score indicator color:
  - [ ] GREEN for HIGH ✅
  - [ ] YELLOW for MEDIUM ⚠️
  - [ ] RED for LOW ❌

### Test 20: Report Details Section
- [ ] Show Violations Details button present and clickable
- [ ] When clicked, displays list of specific violations:
- [ ] Each showing:
  - [ ] Event type
  - [ ] Operation (copy/paste/cut)
  - [ ] Source
  - [ ] Timestamp

## Performance Testing

### Test 21: No Memory Leaks on Navigation
- [ ] Open DevTools → Memory tab
- [ ] Navigate Exam → Report → Exam (several times)
- [ ] Heap size should remain relatively stable
- [ ] No warnings about detached DOM nodes

### Test 22: Event Listeners Cleanup
- [ ] In console, check for proper cleanup
- [ ] No "multiple listeners added" warnings
- [ ] Each navigation removes old listeners before adding new

## Mac Testing (if on macOS)

### Test 23: Cmd+C Detection (Mac Users)
- [ ] Press `Cmd+C` instead of `Ctrl+C`
- [ ] Should trigger same detection as Ctrl+C
- [ ] Alert appears with copy violation
- [ ] Counter increments

### Test 24: Cmd+V Detection (Mac Users)
- [ ] Press `Cmd+V` instead of `Ctrl+V`
- [ ] Should trigger same detection as Ctrl+V
- [ ] Alert appears

### Test 25: Cmd+X Detection (Mac Users)
- [ ] Press `Cmd+X` instead of `Ctrl+X`
- [ ] Should trigger same detection as Ctrl+X
- [ ] Alert appears

## Browser Compatibility Testing

### Test 26: Chrome/Chromium
- [ ] All tests pass in Chrome
- [ ] DevTools console shows all messages
- [ ] Event listeners work

### Test 27: Firefox (Optional)
- [ ] All tests pass in Firefox
- [ ] DevTools console shows all messages

### Test 28: Edge (Windows)
- [ ] All tests pass in Edge
- [ ] DevTools console shows all messages

## Final Checklist

### Prerequisites Done
- [ ] Backend running on http://localhost:8000
- [ ] Frontend running on http://localhost:3000
- [ ] No errors in either terminal
- [ ] Both applications responding to requests

### All Tests Completed
- [ ] Tests 1-10: Browser tests ✅
- [ ] Tests 11-13: Backend API tests ✅
- [ ] Tests 14-17: Stress tests ✅
- [ ] Tests 18-20: Report page tests ✅
- [ ] Tests 21-22: Performance tests ✅
- [ ] Tests 23-25: Mac tests (if applicable) ✅
- [ ] Tests 26-28: Browser compatibility (if needed) ✅

### Game Plan for Issues

If tests fail:
1. [ ] Check console for error messages
2. [ ] Verify event listeners attached (see test 2)
3. [ ] Check backend is running (test 11)
4. [ ] Review COPY_PASTE_DEBUGGING.md for troubleshooting
5. [ ] Check ExamPage.js for syntax errors
6. [ ] Verify metadata structure matches backend expectations

### Success Criteria

✅ All manual tests pass
✅ Event counters increment correctly
✅ Backend receives and stores all events
✅ Report generates accurate scores
✅ No console errors
✅ Alerts show for all violations
✅ Listeners cleanup properly

---

**Ready to start testing?** 🚀 Begin with "Backend Setup" above!

