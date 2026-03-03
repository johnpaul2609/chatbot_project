from pydantic import BaseModel, Field
from typing import Optional, List

class ChatMessage(BaseModel):
    """Model for incoming chat messages"""
    message: str = Field(..., min_length=1, max_length=500)
    user_id: Optional[str] = None

class ChatResponse(BaseModel):
    """Model for chatbot responses"""
    response: str
    intent: str
    confidence: float
    suggestions: Optional[List[str]] = []
