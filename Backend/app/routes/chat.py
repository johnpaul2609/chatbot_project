from fastapi import APIRouter, HTTPException
from app.models import ChatMessage, ChatResponse
from app.services.nlp_service import NLPService
from app.services.intent_classifier import IntentClassifier
from app.services.data_service_sqlite import DataService

router = APIRouter()

nlp_service = NLPService()
intent_classifier = IntentClassifier()

@router.post("/message", response_model=ChatResponse)
async def process_message(chat_message: ChatMessage):
    """Process incoming chat messages"""
    try:
        processed_text = nlp_service.preprocess(chat_message.message)
        intent, confidence = intent_classifier.classify(processed_text)
        response_text = intent_classifier.get_response(intent)
        suggestions = intent_classifier.get_suggestions(intent)
        
        DataService.save_conversation(
            user_id=chat_message.user_id or "anonymous",
            message=chat_message.message,
            response=response_text,
            intent=intent,
            confidence=confidence
        )
        
        return ChatResponse(
            response=response_text,
            intent=intent,
            confidence=confidence,
            suggestions=suggestions
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/history/{user_id}")
async def get_chat_history(user_id: str, limit: int = 10):
    """Get conversation history"""
    try:
        conversations = DataService.get_chat_history(user_id, limit)
        return {"conversations": conversations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.delete("/history/{user_id}")
async def clear_chat_history(user_id: str):
    """Clear chat history"""
    try:
        from app.database_sqlite import Database
        query = "DELETE FROM conversations WHERE user_id = ?"
        Database.execute_insert(query, (user_id,))
        return {"message": "Chat history cleared"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
