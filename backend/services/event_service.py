"""
Service to manage and store activity events in memory
"""
from typing import List, Dict, Any
from models.activity_model import ActivityLog

# In-memory storage for all events
event_store: Dict[str, List[ActivityLog]] = {}


def log_event(user_id: str, event_type: str, timestamp: float, metadata: dict) -> None:
    """
    Store a new event for a user
    
    Args:
        user_id: Unique identifier for the user
        event_type: Type of event (copy_paste, tab_switch, answer_submission, etc.)
        timestamp: Unix timestamp of when event occurred
        metadata: Additional data about the event
    """
    if user_id not in event_store:
        event_store[user_id] = []
    
    log = ActivityLog(
        user_id=user_id,
        event_type=event_type,
        timestamp=timestamp,
        metadata=metadata if metadata else {}
    )
    
    event_store[user_id].append(log)


def get_events(user_id: str) -> List[ActivityLog]:
    """
    Retrieve all events for a specific user
    
    Args:
        user_id: Unique identifier for the user
        
    Returns:
        List of ActivityLog objects for the user
    """
    return event_store.get(user_id, [])


def get_all_events() -> Dict[str, List[ActivityLog]]:
    """
    Get all stored events
    
    Returns:
        Dictionary mapping user_id to their event logs
    """
    return event_store


def clear_user_events(user_id: str) -> None:
    """
    Clear all events for a specific user (for testing)
    
    Args:
        user_id: Unique identifier for the user
    """
    if user_id in event_store:
        event_store[user_id] = []
