# Copy-Paste Detection Testing & Debugging Guide

## 📋 What Was Fixed

Your React copy-paste detection has been completely rewritten with:

✅ **Event Listeners Added:**
- `copy` event - Detects copy operations
- `paste` event - Detects paste operations
- `cut` event - Detects cut operations
- `keydown` event - Detects keyboard shortcuts (Ctrl+C, Ctrl+V, Ctrl+X)
- `blur`/`focus` events - Detects tab switching (already working)

✅ **Keyboard Shortcuts Detected:**
- `Ctrl+C` (or `Cmd+C` on Mac) - Copy
- `Ctrl+V` (or `Cmd+V` on Mac) - Paste
- `Ctrl+X` (or `Cmd+X` on Mac) - Cut

✅ **Detection Works In:**
- Textarea fields
- Text input fields
- Entire document
- Right-click context menu

✅ **Features Implemented:**
- Prevents copy/paste/cut using `event.preventDefault()`
- Shows alert to user on violation
- Logs detailed events to backend
- Logs to browser console for debugging
- Proper cleanup on component unmount
- Uses capture phase for reliable event detection

## 🧪 Testing the Copy-Paste Detection

### Prerequisites

1. **Backend Running:**
```bash
cd backend
python app.py
# Should show: Uvicorn running on http://0.0.0.0:8000
```

2. **Frontend Running:**
```bash
cd frontend
npm start
# Should open http://localhost:3000
```

### Test Scenario 1: Detect Copy (Ctrl+C)

**Steps:**
1. Go to http://localhost:3000
2. Make sure you're on the **Exam Page** tab
3. In a question text, try to **copy using Ctrl+C** (or Cmd+C on Mac)

**Expected Result:**
- ❌ Alert appears: "Copy-paste is not allowed during exam!"
- Console shows: `⚠️ KEYBOARD SHORTCUT DETECTED - Ctrl+C`
- Copy Events counter increases: `📋 Copy Events: 1`
- Event appears in Event Log with timestamp

**Console Output Should Show:**
```
⚠️ KEYBOARD SHORTCUT DETECTED - Ctrl+C
📤 Sending event to backend: copy_paste
{operation: "copy", source: "keyboard_ctrl_c", timestamp: "..."}
✓ Event logged successfully: copy_paste
```

### Test Scenario 2: Detect Paste (Ctrl+V)

**Steps:**
1. On the Exam Page
2. Try to **paste using Ctrl+V** (or Cmd+V on Mac)

**Expected Result:**
- ❌ Alert appears: "Paste operation (Ctrl+V) is not allowed during exam!"
- Console shows: `⚠️ KEYBOARD SHORTCUT DETECTED - Ctrl+V`
- Copy Events counter increases: `📋 Copy Events: 2`
- Event appears in Event Log

**Console Output:**
```
⚠️ KEYBOARD SHORTCUT DETECTED - Ctrl+V
📤 Sending event to backend: copy_paste
{operation: "paste", source: "keyboard_ctrl_v", timestamp: "..."}
✓ Event logged successfully: copy_paste
```

### Test Scenario 3: Detect Cut (Ctrl+X)

**Steps:**
1. On the Exam Page
2. Try to **cut using Ctrl+X** (or Cmd+X on Mac)

**Expected Result:**
- ❌ Alert appears: "Cut operation (Ctrl+X) is not allowed during exam!"
- Console shows: `⚠️ KEYBOARD SHORTCUT DETECTED - Ctrl+X`
- Copy Events counter increases
- Event logged

### Test Scenario 4: Right-Click Context Menu Copy

**Steps:**
1. On the Exam Page, over some text in a question
2. **Right-click** → Choose "Copy"

**Expected Result:**
- ❌ Alert appears: "Copy-paste is not allowed during exam!"
- Console shows: `⚠️ COPY EVENT DETECTED - using Ctrl+C or right-click menu`
- Copy Events counter increases
- Event logged with `source: "copy_event"`

### Test Scenario 5: Paste from Context Menu

**Steps:**
1. On the Exam Page
2. **Right-click** in an answer field → Choose "Paste"

**Expected Result:**
- ❌ Alert appears: "Pasting is not allowed during exam!"
- Console shows: `⚠️ PASTE EVENT DETECTED - user tried to paste`
- Copy Events counter increases
- Event logged with `source: "paste_event"`

### Test Scenario 6: Tab Switching (Should Still Work)

**Steps:**
1. On the Exam Page
2. **Click on a different browser tab** (or Alt+Tab)

**Expected Result:**
- No alert (this is allowed to log)
- Console shows event detection
- Tab Switches counter increases: `📑 Tab Switches: 1`

## 🔍 Browser Console Debugging

### Open Console

**Chrome/Firefox/Edge:**
- Press `F12` or `Right-Click` → `Inspect` → `Console` tab

### Check for Initialization

When you load the Exam Page, you should see:
```
🔧 Setting up event listeners...
✓ All event listeners registered successfully
```

### Monitor Real-Time Events

**Try an action and watch console:**

**Copy attempt (Ctrl+C):**
```
⚠️ KEYBOARD SHORTCUT DETECTED - Ctrl+C
📤 Sending event to backend: copy_paste {operation: "copy", source: "keyboard_ctrl_c", timestamp: "2026-03-18T..."}
✓ Event logged successfully: copy_paste
```

**Paste attempt (Ctrl+V):**
```
⚠️ KEYBOARD SHORTCUT DETECTED - Ctrl+V
📤 Sending event to backend: copy_paste {operation: "paste", source: "keyboard_ctrl_v", timestamp: "2026-03-18T..."}
✓ Event logged successfully: copy_paste
```

**Tab switch:**
```
⚠️ TAB SWITCH DETECTED - user left window
📤 Sending event to backend: tab_switch {event: "user_switched_to_different_tab", timestamp: "2026-03-18T..."}
✓ Event logged successfully: tab_switch
```

## 📊 Verify Backend Received Events

### Check Backend Logs

The backend should show requests coming in:
```
INFO:     POST /log-event
INFO:     "POST /log-event HTTP/1.1" 200 OK
```

### Test with API

```bash
# Get all events for a user
curl http://localhost:8000/events/student_001

# Get integrity report
curl http://localhost:8000/report/student_001
```

**Expected Report after testing:**
```json
{
  "user_id": "student_001",
  "copy_paste_count": 5,
  "tab_switch_count": 1,
  "ai_suspicion_count": 0,
  "integrity_score": "LOW"
}
```

### Using Python

```python
import requests

# Get events
response = requests.get('http://localhost:8000/events/student_001')
print(response.json())

# Get report
response = requests.get('http://localhost:8000/report/student_001')
print(response.json())
```

## 🐛 Troubleshooting

### Problem: Copy-Paste Detection Not Working

**Step 1: Check Console for Initialization**
- Open DevTools (F12)
- Go to Console tab
- Refresh page
- Should see: `🔧 Setting up event listeners...`
- Should see: `✓ All event listeners registered successfully`

**If not showing:**
- Problem is with useEffect hook
- Check for errors in console

**Step 2: Check if Events Are Being Triggered**
- Try to copy something
- Look for console output
- Should see `⚠️ KEYBOARD SHORTCUT DETECTED`

**If not showing:**
- Event listeners not attached properly
- Check browser console for JavaScript errors

**Step 3: Check Backend Connection**
- Open DevTools → Network tab
- Try to copy
- Look for `POST` request to `localhost:8000/log-event`

**If no request appears:**
- logEvent function not being called
- API might be down
- Check backend terminal for errors

**Step 4: Check Browser Compatibility**
- Copy detection works in all modern browsers
- Ensure you're using recent version:
  - Chrome 90+
  - Firefox 88+
  - Safari 14+
  - Edge 90+

### Problem: Alert Not Showing

**Cause 1: Browser blocked alerts**
- Some browsers block alerts
- Check browser settings

**Cause 2: Event.preventDefault() not working**
- Try different browser
- Check if browser is allowing preventDefault

### Problem: Events Not Reaching Backend

**Check 1: Is backend running?**
```bash
curl http://localhost:8000/health
# Should return: {"status": "healthy"}
```

**Check 2: Check API endpoint**
- Open DevTools → Network tab
- Try to copy
- Click on the POST request
- Check URL: should be `http://localhost:8000/log-event`
- Check Response: should show success message

**Check 3: Check CORS settings**
- Backend has CORS enabled
- If getting CORS error in browser console
- Backend might not be running

### Problem: Events Showing But Count Not Increasing

**Possible Causes:**
1. State not updating properly
2. Wrong event type being sent
3. Backend not counting correctly

**Debug:**
```javascript
// In ExamPage.js, add this temporary line
console.log('Copy count should now be:', copyCounts);
```

### Problem: React Not Re-rendering After Event

**Cause:** State not being updated

**Check:**
- `setCopyCounts(prev => prev + 1)` should be called
- Look in console for: `Copy Events: 2` appearing

## 📝 Manual Testing Checklist

Use this checklist to verify all functionality:

```
Copy Detection:
- [ ] Ctrl+C triggers alert
- [ ] Ctrl+C shows in console
- [ ] Ctrl+C increments counter
- [ ] Ctrl+C sends to backend

Paste Detection:
- [ ] Ctrl+V triggers alert
- [ ] Ctrl+V shows in console
- [ ] Ctrl+V increments counter
- [ ] Ctrl+V sends to backend

Cut Detection:
- [ ] Ctrl+X triggers alert
- [ ] Ctrl+X shows in console
- [ ] Ctrl+X increments counter
- [ ] Ctrl+X sends to backend

Context Menu:
- [ ] Right-click Copy triggers alert
- [ ] Right-click Paste triggers alert

Tab Switch:
- [ ] Switching tabs increments counter
- [ ] Switching tabs shows in console

Backend:
- [ ] Events appear in backend logs
- [ ] curl /events/{user_id} shows all events
- [ ] curl /report/{user_id} shows correct counts

Report Page:
- [ ] Copy-paste count is correct
- [ ] Tab switch count is correct
- [ ] Integrity score is correct (LOW if many violations)
```

## 🔧 Code Changes Summary

### What Changed in ExamPage.js

**Before:**
```javascript
// Only listened for copy event
document.addEventListener('copy', handleCopy);
// No paste detection
// No cut detection
// No keyboard shortcuts
```

**After:**
```javascript
// Listen for all copy-paste operations
document.addEventListener('copy', handleCopy, true);      // Capture phase
document.addEventListener('paste', handlePaste, true);    // Capture phase
document.addEventListener('cut', handleCut, true);        // Capture phase
document.addEventListener('keydown', handleKeyDown, true); // Capture phase

// Detect keyboard shortcuts:
// - Ctrl+C for copy
// - Ctrl+V for paste
// - Ctrl+X for cut
// - Works on Mac with Cmd key too
```

## 📤 Event Data Being Sent

Each event sent to backend looks like:

```json
{
  "user_id": "student_001",
  "event_type": "copy_paste",
  "timestamp": 1710766800.123,
  "metadata": {
    "operation": "copy",
    "source": "keyboard_ctrl_c",
    "timestamp": "2026-03-18T14:30:00.123Z"
  }
}
```

**Metadata Fields:**
- `operation`: "copy", "paste", or "cut"
- `source`: Where it came from
  - `keyboard_ctrl_c` - Ctrl+C
  - `keyboard_ctrl_v` - Ctrl+V
  - `keyboard_ctrl_x` - Ctrl+X
  - `copy_event` - Copy event (right-click menu)
  - `paste_event` - Paste event (right-click menu)
  - `cut_event` - Cut event (right-click menu)
- `timestamp`: When it happened (ISO format)

## ✅ Next Steps

1. Test all scenarios above
2. Check browser console and backend logs
3. Verify integrity report shows correct counts
4. Go to Report Page to see statistics

If everything works, you have a fully functional copy-paste detection system! 🎉

## 📞 Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Events not showing in console | Check F12 → Console, refresh page |
| Counts not increasing | Check if backend is running, check network tab |
| Alerts not appearing | Try different browser, check F12 for errors |
| Backend showing 400 error | Check API request format in Network tab |
| Events logged but report wrong | Wait a moment for report to fetch, refresh report |

---

**Remember:** All events are logged to browser console with emoji indicators for easy spotting:
- 🔧 Setup messages
- ⚠️ Warning messages (violations)
- 📤 Sending to backend
- ✓ Success messages
- ❌ Error messages
