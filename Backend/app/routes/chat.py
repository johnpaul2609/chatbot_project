from fastapi import APIRouter, HTTPException
from app.models import ChatMessage, ChatResponse
from app.services.nlp_service import NLPService
from app.services.intent_classifier import IntentClassifier
from app.services.academic_classifier import (
    classify_academic, get_academic_response,
    get_academic_suggestions, get_material_download_info,
    get_timetable_info
)
from app.services.data_service_sqlite import DataService

router = APIRouter()

nlp_service = NLPService()
intent_classifier = IntentClassifier(nlp_service)

BACKEND_URL = "http://127.0.0.1:8000"

YEAR_NAMES = {1: "1st Year", 2: "2nd Year", 3: "3rd Year", 4: "4th Year"}

@router.post("/message", response_model=ChatResponse)
async def process_message(chat_message: ChatMessage):
    try:
        message  = chat_message.message.strip()
        user_id  = chat_message.user_id or "anonymous"
        mode     = chat_message.mode or "admission"

        # ── ACADEMIC MODE ──────────────────────────────────────────────────
        if mode == "academic":
            intent, confidence = classify_academic(message)

            # ── Timetable image response ───────────────────────────────────
            tt_info = get_timetable_info(intent, message)
            if tt_info:
                year_name = YEAR_NAMES.get(tt_info["year"], "")
                response_text = (
                    f"Here is the {tt_info['dept']} {year_name} Weekly Timetable!\n\n"
                    f"Timing: Mon–Fri 8:45 AM – 4:30 PM | Sat 8:45 AM – 1:00 PM\n"
                    f"The timetable image is shown below.\n\n"
                    f"For the latest timetable, always check with your class coordinator or LMS portal."
                )
                suggestions = [
                    f"{tt_info['dept']} Notes?",
                    f"{tt_info['dept']} Syllabus?",
                    "Exam schedule?",
                    "Other year timetable?"
                ]
                DataService.save_conversation(user_id, message, response_text, intent, confidence)
                return ChatResponse(
                    response=response_text,
                    intent=intent,
                    confidence=confidence,
                    suggestions=suggestions,
                    image_url=tt_info["image_url"],
                    image_label=tt_info["label"],
                )

            # ── PDF download response ──────────────────────────────────────
            material = get_material_download_info(intent)
            if material:
                download_url  = f"{BACKEND_URL}/api/materials/download/{material['material_id']}"
                response_text = (
                    f"Here are the notes for {material['subject']}!\n\n"
                    f"Topics covered:\n{material['description']}\n\n"
                    f"Department: {material['dept']}\n"
                    f"Semester: {material['semester']} | {material['pages']}\n\n"
                    f"Click the Download button below to get the PDF."
                )
                suggestions = ["More notes?", "Exam schedule?", "Timetable?", "Other subjects?"]
                DataService.save_conversation(user_id, message, response_text, intent, confidence)
                return ChatResponse(
                    response=response_text,
                    intent=intent,
                    confidence=confidence,
                    suggestions=suggestions,
                    download_url=download_url,
                    material_name=f"{material['subject']}.pdf",
                )

            # ── Normal academic text response ──────────────────────────────
            response_text = get_academic_response(intent)
            suggestions   = get_academic_suggestions(intent)
            DataService.save_conversation(user_id, message, response_text, intent, confidence)
            return ChatResponse(
                response=response_text,
                intent=intent,
                confidence=confidence,
                suggestions=suggestions,
            )

        # ── ADMISSION MODE ─────────────────────────────────────────────────
        intent, confidence = intent_classifier.classify(message)
        response_text = intent_classifier.get_response(intent)
        suggestions   = intent_classifier.get_suggestions(intent)
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
        return {"conversations": DataService.get_chat_history(user_id, limit)}
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