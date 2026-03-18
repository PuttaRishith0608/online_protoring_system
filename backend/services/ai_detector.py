"""
Service to detect suspicious AI-generated answers using simple heuristics
"""
from typing import List, Tuple
from models.activity_model import ActivityLog


def check_ai_suspicion(events: List[ActivityLog]) -> Tuple[int, List[dict]]:
    """
    Detect potentially AI-generated answers based on submission patterns
    
    Heuristic: If answer length > 200 characters AND submitted in < 10 seconds → suspicious
    
    Args:
        events: List of ActivityLog events for a user
        
    Returns:
        Tuple of (suspicion_count, suspicious_events_list)
    """
    suspicion_count = 0
    suspicious_events = []
    
    # Look for answer_submission events
    submission_events = [e for e in events if e.event_type == "answer_submission"]
    
    for submission in submission_events:
        metadata = submission.metadata or {}
        
        # Get answer length and time taken
        answer_text = metadata.get("answer", "")
        time_taken = metadata.get("time_taken_seconds", 0)
        
        answer_length = len(answer_text)
        
        # Check for suspicious pattern: long answer submitted too quickly
        if answer_length > 200 and time_taken < 10:
            suspicion_count += 1
            suspicious_events.append({
                "timestamp": submission.timestamp,
                "answer_length": answer_length,
                "time_taken": time_taken,
                "reason": "Long answer submitted too quickly"
            })
    
    return suspicion_count, suspicious_events


def calculate_integrity_score(copy_paste_count: int, tab_switch_count: int, ai_suspicion_count: int) -> str:
    """
    Calculate overall integrity score based on suspicious activity counts
    
    Scoring:
    - HIGH: No suspicious activity
    - MEDIUM: 1-3 suspicious events
    - LOW: 4+ suspicious events
    
    Args:
        copy_paste_count: Number of copy-paste events detected
        tab_switch_count: Number of tab switches detected
        ai_suspicion_count: Number of AI-suspicious answers
        
    Returns:
        Integrity score: "HIGH", "MEDIUM", or "LOW"
    """
    total_suspicious = copy_paste_count + tab_switch_count + ai_suspicion_count
    
    if total_suspicious == 0:
        return "HIGH"
    elif total_suspicious <= 3:
        return "MEDIUM"
    else:
        return "LOW"
