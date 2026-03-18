#!/usr/bin/env python3
"""
Backend Verification Script for Online Proctoring System
This script verifies that the backend is properly set up and all dependencies are installed.
Run this to ensure your backend is ready for testing.
Usage: python verify_setup.py
"""

import sys
import subprocess
import importlib.util
from pathlib import Path

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_header(text):
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}{text:^60}{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}✗ {text}{Colors.END}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ {text}{Colors.END}")

def check_python_version():
    print_header("Python Version Check")
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    print(f"Current Python version: {version_str}")
    
    if version.major >= 3 and version.minor >= 8:
        print_success(f"Python {version_str} is supported (3.8+)")
        return True
    else:
        print_error(f"Python {version_str} is not supported. Required: 3.8+")
        return False

def check_required_packages():
    print_header("Required Packages Check")
    
    required_packages = {
        'fastapi': 'FastAPI',
        'uvicorn': 'Uvicorn',
        'pydantic': 'Pydantic',
    }
    
    all_installed = True
    
    for module_name, package_name in required_packages.items():
        spec = importlib.util.find_spec(module_name)
        if spec is not None:
            try:
                module = __import__(module_name)
                version = getattr(module, '__version__', 'unknown')
                print_success(f"{package_name} is installed (version: {version})")
            except Exception as e:
                print_error(f"{package_name} is installed but cannot import: {str(e)}")
                all_installed = False
        else:
            print_error(f"{package_name} is NOT installed")
            print_info(f"  Install with: pip install {module_name}")
            all_installed = False
    
    return all_installed

def check_project_files():
    print_header("Project Files Check")
    
    required_files = {
        'app.py': 'Main FastAPI application',
        'requirements.txt': 'Python dependencies file',
        'models/activity_model.py': 'Data models',
        'services/event_service.py': 'Event storage service',
        'services/report_service.py': 'Report generation service',
        'services/ai_detector.py': 'AI detection logic',
        'routes/activity.py': 'Activity endpoints',
        'routes/report.py': 'Report endpoints',
    }
    
    all_exist = True
    
    for file_path, description in required_files.items():
        full_path = Path(file_path)
        if full_path.exists():
            size = full_path.stat().st_size
            print_success(f"{description} - {file_path} ({size} bytes)")
        else:
            print_error(f"{description} - {file_path} NOT FOUND")
            all_exist = False
    
    return all_exist

def check_backend_structure():
    print_header("Backend Structure Check")
    
    required_dirs = [
        'models',
        'services',
        'routes',
        'database',
    ]
    
    all_exist = True
    
    for dir_name in required_dirs:
        dir_path = Path(dir_name)
        if dir_path.is_dir():
            print_success(f"Directory exists: {dir_name}/")
        else:
            print_error(f"Directory missing: {dir_name}/")
            all_exist = False
    
    return all_exist

def check_event_storage():
    print_header("Event Storage Check")
    
    try:
        from services.event_service import event_store
        print_success("Event storage module loads successfully")
        print_info(f"Event store initialized as: {type(event_store).__name__}")
        return True
    except Exception as e:
        print_error(f"Cannot import event storage: {str(e)}")
        return False

def check_models():
    print_header("Data Models Check")
    
    try:
        from models.activity_model import LogEvent, ActivityLog, IntegrityReport
        print_success("LogEvent model loads successfully")
        print_success("ActivityLog model loads successfully")
        print_success("IntegrityReport model loads successfully")
        
        # Try to create a sample event
        sample_event = LogEvent(
            user_id="test_user",
            event_type="copy_paste",
            timestamp=1234567890.0,
            metadata={"operation": "copy"}
        )
        print_info(f"Sample event created: {sample_event.event_type}")
        return True
    except Exception as e:
        print_error(f"Cannot import data models: {str(e)}")
        return False

def check_services():
    print_header("Services Check")
    
    all_good = True
    
    try:
        from services.event_service import log_event, get_events
        print_success("Event service functions load successfully")
    except Exception as e:
        print_error(f"Cannot import event service: {str(e)}")
        all_good = False
    
    try:
        from services.report_service import generate_report
        print_success("Report service function loads successfully")
    except Exception as e:
        print_error(f"Cannot import report service: {str(e)}")
        all_good = False
    
    try:
        from services.ai_detector import check_ai_suspicion, calculate_integrity_score
        print_success("AI detector functions load successfully")
    except Exception as e:
        print_error(f"Cannot import AI detector: {str(e)}")
        all_good = False
    
    return all_good

def check_routes():
    print_header("Routes Check")
    
    all_good = True
    
    try:
        from routes.activity import router as activity_router
        print_success("Activity routes load successfully")
    except Exception as e:
        print_error(f"Cannot import activity routes: {str(e)}")
        all_good = False
    
    try:
        from routes.report import router as report_router
        print_success("Report routes load successfully")
    except Exception as e:
        print_error(f"Cannot import report routes: {str(e)}")
        all_good = False
    
    return all_good

def check_fastapi_app():
    print_header("FastAPI App Check")
    
    try:
        from app import app
        print_success("FastAPI app initializes successfully")
        
        # Check if routes are registered
        routes = app.routes
        print_info(f"Total routes registered: {len(routes)}")
        
        for route in routes:
            if hasattr(route, 'path'):
                print_info(f"  - {route.path}")
        
        return True
    except Exception as e:
        print_error(f"Cannot initialize FastAPI app: {str(e)}")
        return False

def generate_test_curl_commands():
    print_header("Test Commands (for manual testing)")
    
    print(f"{Colors.YELLOW}Health Check:{Colors.END}")
    print("  curl http://localhost:8000/health")
    print()
    
    print(f"{Colors.YELLOW}Get Events for student_001:{Colors.END}")
    print("  curl http://localhost:8000/events/student_001")
    print()
    
    print(f"{Colors.YELLOW}Get Report for student_001:{Colors.END}")
    print("  curl http://localhost:8000/report/student_001")
    print()
    
    print(f"{Colors.YELLOW}Post Test Event:{Colors.END}")
    print('  curl -X POST http://localhost:8000/log-event \\')
    print('  -H "Content-Type: application/json" \\')
    print('  -d "{\\"user_id\\": \\"test_student\\", \\"event_type\\": \\"copy_paste\\", \\"timestamp\\": 1234567890.0, \\"metadata\\": {\\"operation\\": \\"copy\\"}}"')

def main():
    print(f"\n{Colors.BLUE}Online Proctoring System - Backend Verification{Colors.END}\n")
    
    checks = [
        ("Python Version", check_python_version),
        ("Required Packages", check_required_packages),
        ("Backend Structure", check_backend_structure),
        ("Project Files", check_project_files),
        ("Event Storage", check_event_storage),
        ("Data Models", check_models),
        ("Services", check_services),
        ("Routes", check_routes),
        ("FastAPI App", check_fastapi_app),
    ]
    
    results = {}
    
    for check_name, check_func in checks:
        try:
            results[check_name] = check_func()
        except Exception as e:
            print_error(f"Unexpected error during '{check_name}': {str(e)}")
            results[check_name] = False
    
    # Generate test commands
    generate_test_curl_commands()
    
    # Summary
    print_header("Verification Summary")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    print(f"\nChecks Passed: {passed}/{total}\n")
    
    for check_name, result in results.items():
        status = f"{Colors.GREEN}PASS{Colors.END}" if result else f"{Colors.RED}FAIL{Colors.END}"
        print(f"  {check_name}: {status}")
    
    print()
    
    if passed == total:
        print_success("All checks passed! Backend is ready for testing.")
        print_info("Start backend with: python app.py")
        return 0
    else:
        print_warning(f"{total - passed} check(s) failed. Please fix issues above.")
        print_info("Common fixes:")
        print_info("  1. Install dependencies: pip install -r requirements.txt")
        print_info("  2. Ensure all required files exist in backend/")
        print_info("  3. Check Python version is 3.8+")
        return 1

if __name__ == "__main__":
    exit(main())
