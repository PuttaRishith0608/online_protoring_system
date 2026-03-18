# 🚀 Vercel Deployment Guide - Frontend

## Quick Start (5 minutes)

### Prerequisites
- Frontend code at: `frontend/`
- Backend deployed at Railway: `https://onlineprotoringsystem-production.up.railway.app`
- GitHub account with the project pushed
- Free Vercel account

---

## Deployment Method 1: Connect GitHub (Recommended ⭐)

**Easiest & Quickest:**

### Step 1: Push to GitHub
```bash
cd c:\Users\putta\Desktop\vsproject\edwisely-r1\online-proctoring-system
git add -A
git commit -m "Prepare frontend for Vercel deployment"
git push
```

### Step 2: Create Vercel Account
1. Go to https://vercel.com/signup
2. Click "Continue with GitHub"
3. Authorize Vercel to access your repos

### Step 3: Deploy on Vercel Dashboard
1. Go to https://vercel.com/dashboard
2. Click "New Project"
3. Select your GitHub repository (`edwisely-r1` or similar)
4. Choose the `frontend` folder as root:
   - **Framework Preset:** React
   - **Root Directory:** `frontend`
   - Click "Continue"

### Step 4: Add Environment Variables
1. On the "Environment Variables" section:
   - **Name:** `REACT_APP_API_URL`
   - **Value:** `https://onlineprotoringsystem-production.up.railway.app`
   - Click "Add"

2. Click "Deploy"

**That's it!** Vercel will:
- ✅ Build your React app
- ✅ Deploy to CDN
- ✅ Give you a URL like: `https://edwisely-frontend.vercel.app`
- ✅ Auto-redeploy on every git push

---

## Deployment Method 2: Vercel CLI

**For more control:**

### Step 1: Install Vercel CLI
```bash
npm install -g vercel
```

### Step 2: Login to Vercel
```bash
vercel login
```

### Step 3: Deploy
```bash
cd frontend
vercel --prod
```

### Step 4: Add Environment Variables
When prompted:
- Link to existing project? **Yes**
- Paste the Vercel project ID from https://vercel.com/dashboard
- Environment variables will be set via dashboard

---

## Configuration Files

### `frontend/vercel.json`
Already handled by Vercel, but for reference:

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "build",
  "env": {
    "REACT_APP_API_URL": "@react_app_api_url"
  }
}
```

### `frontend/.env.local` (Local Testing)
```
REACT_APP_API_URL=http://localhost:8000
```

---

## After Deployment

### Test the Frontend
```bash
# Once deployed, test:
https://your-vercel-app.vercel.app/

# Should show:
- Exam page with questions
- Report page accessible
- All buttons functional
```

### Test Backend Connection
1. Open DevTools (F12)
2. Go to Console tab
3. Try to copy/paste on exam page
4. You should see:
   - Console message: `📤 Sending event to backend`
   - No CORS errors
   - Events logged to backend

---

## Common Issues & Fixes

### ❌ CORS Error
**Error:** `Access to XMLHttpRequest blocked by CORS policy`

**Fix:** Already configured on backend with:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    ...
)
```

### ❌ API Not Responding
**Error:** `Failed to fetch` when sending events

**Fix:** 
1. Check Vercel environment variable is set correctly
2. Verify Railway backend is running
3. Check console for exact URL being called

### ❌ 404 on Page Refresh
**Error:** Page not found when refreshing non-root URLs

**Fix:** Vercel already handles this for React apps automatically

### ❌ Events Not Logging
**Problem:** Copy-paste works locally but not on Vercel

**Check:**
1. Open DevTools → Network tab
2. Try to copy/paste
3. Look for POST request to `/log-event`
4. If request shows 502, Railway backend may have crashed
5. If request doesn't appear, API URL might be wrong

---

## Deployment URLs

After successful deployment:

- **Frontend:** `https://your-app.vercel.app`
- **Backend:** `https://onlineprotoringsystem-production.up.railway.app`
- **API Docs:** `https://onlineprotoringsystem-production.up.railway.app/docs`

---

## Automatic Deployments

Both GitHub and Vercel CLI will set up automatic deployments:

- **Any push to main branch** → Vercel redeploys automatically
- **Pull requests** → Vercel creates preview deployments
- **Merge to main** → Production deployment

---

## Testing Checklist

After deployment, verify:

- [ ] Frontend loads without errors
- [ ] Exam page displays correctly
- [ ] Can navigate to Report page
- [ ] Copy detection works (try Ctrl+C)
- [ ] Paste detection works (try Ctrl+V)
- [ ] Alert appears on violation
- [ ] Counter increments
- [ ] Backend receives events (check logs)
- [ ] Report shows violation counts
- [ ] No CORS errors in console

---

## Environment Variables Reference

| Variable | Value | Where |
|----------|-------|-------|
| `REACT_APP_API_URL` | `https://onlineprotoringsystem-production.up.railway.app` | Vercel Dashboard → Settings → Environment Variables |

---

## Next Steps

1. **Choose deployment method** (GitHub recommended)
2. **Follow the steps above**
3. **Test the deployed app**
4. **Share your URLs**:
   - Frontend URL (for users)
   - Backend API docs (for developers)

---

## Need Help?

Common commands:

```bash
# Test locally before deploying
cd frontend
npm start

# Build for production
npm run build

# Check build size
npm run build  # Look at the "build" folder size

# Clear Vercel cache and redeploy
vercel --prod --force
```

---

## Vercel Dashboard Tips

**Useful features:**
- **Analytics** → See traffic and performance
- **Logs** → Debug issues
- **Deployments** → Rollback to previous version
- **Settings** → Add custom domain, change environment variables
- **Git** → Disconnect/reconnect GitHub

---

**You're almost done!** Deploy to Vercel now 🚀

