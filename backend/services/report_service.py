"""
Service to generate integrity reports from collected activity events
"""
from typing import List, Dict, Any
from models.activity_model import ActivityLog, IntegrityReport
from services.ai_detector import check_ai_suspicion, calculate_integrity_score


def generate_report(user_id: str, events: List[ActivityLog]) -> IntegrityReport:
    """
    Generate an integrity report for a user based on their activity logs
    
    Args:
        user_id: Unique identifier for the user
        events: List of ActivityLog events for the user
        
    Returns:
        IntegrityReport with counts and integrity score
    """
    
    # Count copy-paste events
    copy_paste_count = len([e for e in events if e.event_type == "copy_paste"])
    
    # Count tab switch events
    tab_switch_count = len([e for e in events if e.event_type == "tab_switch"])
    
    # Check for AI-generated answers
    ai_suspicion_count, suspicious_answers = check_ai_suspicion(events)
    
    # Calculate integrity score
    integrity_score = calculate_integrity_score(copy_paste_count, tab_switch_count, ai_suspicion_count)
    
    # Build details
    details = {
        "total_events": len(events),
        "event_types": list(set(e.event_type for e in events)),
        "suspicious_answers": suspicious_answers,
    }
    
    # Create and return report
    report = IntegrityReport(
        user_id=user_id,
        copy_paste_count=copy_paste_count,
        tab_switch_count=tab_switch_count,
        ai_suspicion_count=ai_suspicion_count,
        integrity_score=integrity_score,
        details=details
    )
    
    return report
