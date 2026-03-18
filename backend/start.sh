#!/bin/bash
# Railway deployment configuration

# Install dependencies
pip install -r requirements.txt

# Run the application
python -m uvicorn app:app --host 0.0.0.0 --port ${PORT:-8000} --log-level info
