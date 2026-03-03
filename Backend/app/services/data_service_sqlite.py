from app.database_sqlite import Database

class DataService:
    """Service to fetch data from SQLite"""
    
    @staticmethod
    def get_intents():
        """Get all intents with patterns and responses"""
        intents_query = "SELECT id, tag, context FROM intents"
        intents_rows = Database.execute_query(intents_query)
        
        intents = []
        for intent_row in intents_rows:
            intent_id = intent_row['id']
            
            patterns_query = "SELECT pattern FROM intent_patterns WHERE intent_id = ?"
            pattern_rows = Database.execute_query(patterns_query, (intent_id,))
            patterns = [row['pattern'] for row in pattern_rows]
            
            responses_query = "SELECT response FROM intent_responses WHERE intent_id = ?"
            response_rows = Database.execute_query(responses_query, (intent_id,))
            responses = [row['response'] for row in response_rows]
            
            intents.append({
                'tag': intent_row['tag'],
                'context': intent_row['context'] or '',
                'patterns': patterns,
                'responses': responses
            })
        
        return intents
    
    @staticmethod
    def save_conversation(user_id, message, response, intent, confidence):
        """Save conversation to database"""
        query = """INSERT INTO conversations (user_id, message, response, intent, confidence)
        VALUES (?, ?, ?, ?, ?)"""
        Database.execute_insert(query, (user_id, message, response, intent, confidence))
    
    @staticmethod
    def get_chat_history(user_id, limit=10):
        """Get user's chat history"""
        query = """SELECT message, response, intent, confidence, created_at
        FROM conversations WHERE user_id = ? ORDER BY created_at DESC LIMIT ?"""
        rows = Database.execute_query(query, (user_id, limit))
        
        history = []
        for row in rows:
            history.append({
                'message': row['message'],
                'response': row['response'],
                'intent': row['intent'],
                'confidence': row['confidence'] if row['confidence'] else 0,
                'timestamp': row['created_at']
            })
        
        return list(reversed(history))
