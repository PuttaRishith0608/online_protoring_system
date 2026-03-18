"""
Routes for handling activity logging
"""
from fastapi import APIRouter, HTTPException
from models.activity_model import LogEvent
from services import event_service

router = APIRouter(tags=["activity"])


@router.post("/log-event")
async def log_event(event: LogEvent):
    """
    Log a user activity event
    
    Expected event types:
    - copy_paste: User copied text
    - tab_switch: User switched to another tab
    - answer_submission: User submitted an answer
    - keyboard_input: User typed something
    - etc.
    
    Example request body:
    {
        "user_id": "user123",
        "event_type": "copy_paste",
        "timestamp": 1647384720.123,
        "metadata": {
            "source": "exam_text",
            "destination": "answer_field"
        }
    }
    """
    
    try:
        # Store the event
        event_service.log_event(
            user_id=event.user_id,
            event_type=event.event_type,
            timestamp=event.timestamp,
            metadata=event.metadata or {}
        )
        
        return {
            "status": "success",
            "message": f"Event logged for user {event.user_id}",
            "event_type": event.event_type
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error logging event: {str(e)}")


@router.get("/events/{user_id}")
async def get_events(user_id: str):
    """
    Get all events for a specific user (for debugging/admin purposes)
    
    Returns list of all logged events for the user
    """
    events = event_service.get_events(user_id)
    
    return {
        "user_id": user_id,
        "event_count": len(events),
        "events": [
            {
                "event_type": e.event_type,
                "timestamp": e.timestamp,
                "metadata": e.metadata
            }
            for e in events
        ]
    }
