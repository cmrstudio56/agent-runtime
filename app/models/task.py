from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, Literal
from datetime import datetime


class TaskRequest(BaseModel):
    intent: Literal["design", "music", "analysis", "writing"]
    action: str
    parameters: Dict[str, Any]
    priority: int = Field(default=5, ge=1, le=10)


class TaskResponse(BaseModel):
    task_id: str
    status: Literal["queued", "processing", "completed", "failed"]
    intent: str
    action: str
    created_at: datetime
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    execution_time_ms: Optional[int] = None


class TaskStatusResponse(BaseModel):
    task_id: str
    status: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    execution_time_ms: Optional[int] = None
