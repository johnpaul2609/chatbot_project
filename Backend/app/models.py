from pydantic import BaseModel, Field
from typing import Optional, List, Literal

class ChatMessage(BaseModel):
    message: str = Field(..., min_length=1, max_length=500)
    user_id: Optional[str] = None
    mode: Optional[Literal["admission", "academic"]] = "admission"

class ChatResponse(BaseModel):
    response: str
    intent: str
    confidence: float
    suggestions: Optional[List[str]] = []

