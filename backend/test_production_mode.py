#!/usr/bin/env python3
"""
Production simulation test - mimics exactly what Railway does
This will show us the exact error causing the crash
"""

import subprocess
import sys
import os

# Set PORT like Railway does
os.environ['PORT'] = '8080'

print("\n" + "=" * 70)
print("PRODUCTION MODE TEST - Starting app like Railway does")
print("=" * 70)
print(f"PORT environment variable: {os.environ.get('PORT')}\n")

# Run the exact command Railway uses
cmd = [
    sys.executable, "-m", "uvicorn",
    "app:app",
    "--host", "0.0.0.0",
    "--port", os.environ['PORT'],
    "--log-level", "info"
]

print(f"Running command: {' '.join(cmd)}\n")
print("=" * 70 + "\n")

try:
    result = subprocess.run(cmd, timeout=10)
except subprocess.TimeoutExpired:
    print("\n✓ App ran for 10 seconds without crashing!")
    print("If it stays running on Railway, the issue is elsewhere.\n")
except Exception as e:
    print(f"\n❌ Error running app: {e}\n")
