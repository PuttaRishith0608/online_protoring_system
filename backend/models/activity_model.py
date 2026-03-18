from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime


class LogEvent(BaseModel):
    """Model for incoming log events"""
    user_id: str
    event_type: str  # e.g., "copy_paste", "tab_switch", "answer_submission"
    timestamp: float
    metadata: Optional[dict[str, Any]] = None


class ActivityLog(BaseModel):
    """Model for storing activity logs internally"""
    user_id: str
    event_type: str
    timestamp: float
    metadata: dict[str, Any]


class IntegrityReport(BaseModel):
    """Model for the integrity report returned to client"""
    user_id: str
    copy_paste_count: int
    tab_switch_count: int
    ai_suspicion_count: int
    integrity_score: str  # "LOW", "MEDIUM", "HIGH"
    details: dict[str, Any]
