from app.database_sqlite import Database

class DataService:

    @staticmethod
    def get_intents():
        intents_rows = Database.execute_query("SELECT id, tag, context FROM intents")
        intents = []
        for row in intents_rows:
            intent_id = row["id"]
            patterns = [r["pattern"] for r in Database.execute_query(
                "SELECT pattern FROM intent_patterns WHERE intent_id = ?", (intent_id,))]
            responses = [r["response"] for r in Database.execute_query(
                "SELECT response FROM intent_responses WHERE intent_id = ? ORDER BY priority DESC", (intent_id,))]
            intents.append({"tag": row["tag"], "context": row["context"] or "", "patterns": patterns, "responses": responses})
        return intents

    @staticmethod
    def save_conversation(user_id, message, response, intent, confidence):
        Database.execute_insert(
            "INSERT INTO conversations (user_id, message, response, intent, confidence) VALUES (?, ?, ?, ?, ?)",
            (user_id, message, response, intent, confidence))

    @staticmethod
    def get_chat_history(user_id, limit=10):
        rows = Database.execute_query(
            "SELECT message, response, intent, confidence, created_at FROM conversations WHERE user_id = ? ORDER BY created_at DESC LIMIT ?",
            (user_id, limit))
        history = [{"message": r["message"], "response": r["response"], "intent": r["intent"],
                    "confidence": r["confidence"] or 0, "timestamp": r["created_at"]} for r in rows]
        return list(reversed(history))