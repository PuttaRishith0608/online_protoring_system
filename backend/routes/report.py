"""
Routes for generating and retrieving integrity reports
"""
from fastapi import APIRouter, HTTPException
from services import event_service, report_service

router = APIRouter(tags=["report"])


@router.get("/report/{user_id}")
async def get_report(user_id: str):
    """
    Get the integrity report for a user
    
    Returns:
    {
        "user_id": "user123",
        "copy_paste_count": 2,
        "tab_switch_count": 3,
        "ai_suspicion_count": 1,
        "integrity_score": "MEDIUM",
        "details": {
            "total_events": 10,
            "event_types": ["copy_paste", "tab_switch", "answer_submission"],
            "suspicious_answers": [...]
        }
    }
    """
    
    try:
        # Get all events for the user
        events = event_service.get_events(user_id)
        
        # Generate report
        report = report_service.generate_report(user_id, events)
        
        return report.dict()
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")


@router.get("/health")
async def health_check():
    """
    Simple health check endpoint
    """
    return {"status": "healthy", "message": "Proctoring system backend is running"}
