import re
from typing import List
from nltk.stem import PorterStemmer

class NLPService:
    """Simple NLP Service without spaCy"""
    
    def __init__(self):
        print("✅ Using simple NLP (without spaCy)")
    
    def preprocess(self, text: str) -> str:
        """Clean and normalize text"""
        text = text.lower()
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        text = ' '.join(text.split())
        
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                     'of', 'with', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
                     'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'can',
                     'i', 'you', 'he', 'she', 'it', 'we', 'they', 'what', 'how'}
        
        words = text.split()
        words = [w for w in words if w not in stop_words]
        return ' '.join(words)
    
    def extract_keywords(self, text: str) -> List[str]:
        """Extract keywords"""
        text = text.lower()
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        words = text.split()
        keywords = [w for w in words if len(w) > 3]
        return keywords[:5]
    
    def get_similarity(self, text1: str, text2: str) -> float:
        """Simple similarity"""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
   
        if not words1 or not words2:
            return 0.0
        common = words1.intersection(words2)
        return len(common) / max(len(words1), len(words2))
stemmer = PorterStemmer()
words = [stemmer.stem(w) for w in words if w not in stop_words]    