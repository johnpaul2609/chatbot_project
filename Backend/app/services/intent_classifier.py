from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import numpy as np
from app.services.data_service_sqlite import DataService
import random

class IntentClassifier:
    """ML Intent Classifier"""
    
    def __init__(self):
        self.pipeline = None
        self.intents = []
        self.intent_responses = {}
        self.intent_suggestions = {}
        self.train()
    
    def train(self):
        """Train the intent classification model"""
        print("🎓 Training intent classifier...")
        
        self.intents = DataService.get_intents()
        
        if not self.intents:
            print("⚠️ No intents found")
            return
        
        patterns = []
        labels = []
        
        for intent in self.intents:
            tag = intent['tag']
            self.intent_responses[tag] = intent['responses']
            self.intent_suggestions[tag] = self._generate_suggestions(intent)
            
            for pattern in intent['patterns']:
                patterns.append(pattern.lower())
                labels.append(tag)
        
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(stop_words="english")),
            ('clf', MultinomialNB())
        ])
        
        self.pipeline.fit(patterns, labels)
        print(f"✅ Trained on {len(patterns)} patterns, {len(set(labels))} intents")
    
    def classify(self, text: str):
        """Classify intent"""
        if not self.pipeline:
            return "unknown", 0.0
        
        intent = self.pipeline.predict([text.lower()])[0]
        probabilities = self.pipeline.predict_proba([text.lower()])[0]
        confidence = float(np.max(probabilities))
        
        if confidence < 0.1:
            intent = "unknown"
        
        return intent, confidence
    
    def get_response(self, intent: str) -> str:
        """Get response for intent"""
        if intent == "unknown":
            return "I'm not sure I understand. Ask about admissions, fees, programs, or facilities."
        
        responses = self.intent_responses.get(intent, [])
        return random.choice(responses) if responses else "I don't have info about that."
    
    def get_suggestions(self, intent: str) -> list:
        """Get follow-up suggestions"""
        return self.intent_suggestions.get(intent, [])
    
    def _generate_suggestions(self, intent: dict) -> list:
        """Generate contextual suggestions"""
        context = intent.get('context', '')
        
        context_suggestions = {
            'greeting': ["Tell me about admission", "What programs?", "What are fees?"],
            'admission': ["Eligibility?", "When to apply?", "What are fees?"],
            'programs': ["Tell me about CSE", "Placements?", "Fees?"],
            'fees': ["Scholarships?", "Hostel fees?", "Facilities?"],
            'facilities': ["Hostel?", "Placements?", "Contact?"],
            'placements': ["Programs?", "Fees?", "Faculty?"]
        }
        
        return context_suggestions.get(context, ["What else?", "Ask about admissions"])
