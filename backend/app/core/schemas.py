from pydantic import BaseModel
from typing import Any, Optional


class APIResponse(BaseModel):
    success: bool
    data: Optional[Any] = None
    error: Optional[dict] = None


class ChatRequest(BaseModel):
    user_input: str
    session_id: str
