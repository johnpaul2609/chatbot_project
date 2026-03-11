from fastapi import APIRouter, HTTPException
from app.models import ChatMessage, ChatResponse
from app.services.nlp_service import NLPService
from app.services.intent_classifier import IntentClassifier
from app.services.data_service_sqlite import DataService

router = APIRouter()

nlp_service = NLPService()
intent_classifier = IntentClassifier(nlp_service)

ACADEMIC_RESPONSE = (
    "I'm the Admission Support Assistant.\n\n"
    "I can only help with admission-related questions:\n"
    "• Fees & scholarships\n"
    "• Eligibility criteria\n"
    "• Courses & programs\n"
    "• Hostel & facilities\n"
    "• Placement records\n\n"
    "For academic queries, contact:\n"
    "Phone: +91-44-12345678\n"
    "Email: admissions@stlourdes.edu"
)

@router.post("/message", response_model=ChatResponse)
async def process_message(chat_message: ChatMessage):
    try:
        message = chat_message.message.strip()
        user_id = chat_message.user_id or "anonymous"
        mode = chat_message.mode or "admission"

        if mode == "academic":
            DataService.save_conversation(user_id, message, ACADEMIC_RESPONSE, "academic_redirect", 1.0)
            return ChatResponse(
                response=ACADEMIC_RESPONSE,
                intent="academic_redirect",
                confidence=1.0,
                suggestions=["What are the fees?", "How to apply?", "Hostel facility?", "Placement details?"],
            )

        intent, confidence = intent_classifier.classify(message)
        response_text = intent_classifier.get_response(intent)
        suggestions = intent_classifier.get_suggestions(intent)

        DataService.save_conversation(user_id, message, response_text, intent, confidence)

        return ChatResponse(
            response=response_text,
            intent=intent,
            confidence=confidence,
            suggestions=suggestions,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.get("/history/{user_id}")
async def get_chat_history(user_id: str, limit: int = 10):
    try:
        conversations = DataService.get_chat_history(user_id, limit)
        return {"conversations": conversations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.delete("/history/{user_id}")
async def clear_chat_history(user_id: str):
    try:
        from app.database_sqlite import Database
        Database.execute_insert("DELETE FROM conversations WHERE user_id = ?", (user_id,))
        return {"message": "Chat history cleared"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")