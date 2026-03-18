#!/usr/bin/env python3
"""
Quick startup test for Railway deployment
Run this locally to verify the app starts without errors
"""

import sys
import traceback

print("🧪 Testing app startup...")

try:
    print("1. Testing imports...")
    from app import app
    print("   ✓ App imported successfully")
    
    print("\n2. Testing FastAPI app object...")
    print(f"   ✓ FastAPI app: {app}")
    print(f"   ✓ Title: {app.title}")
    
    print("\n3. Testing routers...")
    routes = app.routes
    print(f"   ✓ Total routes: {len(routes)}")
    for route in routes[:5]:
        if hasattr(route, 'path'):
            print(f"     - {route.path}")
    
    print("\n4. Testing services...")
    from services import event_service, report_service, ai_detector
    print("   ✓ Event service imported")
    print("   ✓ Report service imported")
    print("   ✓ AI detector imported")
    
    print("\n✅ ALL TESTS PASSED - App should start successfully on Railway!")
    print("\n📝 Next steps:")
    print("   1. Commit changes to git")
    print("   2. Push to your Railway-connected repository")
    print("   3. Railway will automatically deploy")
    print("   4. Check Railway dashboard for logs if there are still issues")
    
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    print("\nFull traceback:")
    traceback.print_exc()
    sys.exit(1)
