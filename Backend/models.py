"""
app/models.py
Pydantic request and response models.
"""
from pydantic import BaseModel, Field
from typing import Optional, List


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)
    user_id: str = Field(default="anonymous", max_length=100)
    mode: str = Field(default="auto", description="auto | admission | academic")


class ChatResponse(BaseModel):
    response: str
    intent: Optional[str] = None
    mode: str = "general"
    confidence: float = 0.0
    suggestions: List[str] = []
    structured_data: Optional[dict] = None
    timestamp: str = ""


class ConversationMessage(BaseModel):
    user_message: str
    bot_response: str
    intent_tag: Optional[str] = None
    confidence: Optional[float] = None
    mode: Optional[str] = "general"
    timestamp: str


class HistoryResponse(BaseModel):
    user_id: str
    messages: List[ConversationMessage]
    total: int
