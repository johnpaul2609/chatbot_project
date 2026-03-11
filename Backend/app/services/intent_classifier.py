from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import numpy as np
import random
from app.services.data_service_sqlite import DataService

# Keyword override map - checked BEFORE ML model
KEYWORD_OVERRIDES = {
    "fees_general":         ["fee","fees","tuition","how much","annual fee","yearly fee","cost","price"],
    "fees_breakdown":       ["fee breakdown","detailed fee","total fee","all fees","complete fee","full cost"],
    "scholarships":         ["scholarship","waiver","free seat","financial aid","sc st","obc","merit scholarship"],
    "fees_installment":     ["installment","emi","payment option","pay in parts","split fee"],
    "program_cse":          ["cse","computer science engineering","be cse","b.e cse"],
    "program_it":           ["b.tech it","btech it","information technology","it course","it branch"],
    "program_aids":         ["aids","ai and data science","ai ds","data science course","artificial intelligence data"],
    "program_cyber":        ["cyber security","cybersecurity","ethical hacking","cyber branch"],
    "program_mech":         ["mech","mechanical engineering","be mech","mechanical course"],
    "programs_overview":    ["courses","programs","branches","list of courses","what do you offer","available courses","which courses"],
    "eligibility":          ["eligible","eligibility","minimum marks","cutoff","required percentage","who can apply","pcm","50 percent","45 percent"],
    "admission_process":    ["how to apply","admission process","how to get admission","how to join","how can i apply","enrollment","apply now"],
    "management_quota":     ["management quota","direct admission","direct seat","without tnea","nri quota","spot admission"],
    "important_dates":      ["deadline","last date","when to apply","admission date","tnea date","counseling date","when does"],
    "hostel":               ["hostel","accommodation","boys hostel","girls hostel","stay on campus","room and board","hostel fee"],
    "transport":            ["transport","bus","college bus","bus route","bus fee","commute","how to reach"],
    "placements_overview":  ["placement","placed","campus placement","placement percentage","placement rate","job after"],
    "placements_companies": ["which companies","top recruiters","companies visiting","who recruits","list of companies","mnc"],
    "placements_package":   ["salary","package","lpa","ctc","average package","highest package","how much salary"],
    "contact":              ["contact","phone","email","office","helpline","call college","reach college","college number"],
    "naac_accreditation":   ["naac","accreditation","naac grade","aicte","recognized","approved college"],
    "affiliation":          ["affiliation","affiliated","anna university","which university"],
    "campus":               ["campus","where is college","college location","how big","campus area","campus size"],
    "college_overview":     ["about college","college information","tell me about college","overview","profile"],
    "faculty":              ["faculty","teachers","professors","phd","teaching staff"],
    "library":              ["library","books","e-library","nptel","reading room","digital library"],
    "labs":                 ["lab","laboratory","computer lab","gpu lab","cyber lab","which labs"],
    "sports":               ["sports","cricket","football","basketball","gymnasium","gym","sports facility"],
    "facilities_overview":  ["facilities","infrastructure","amenities","campus facilities","what does college provide"],
}

SUGGESTIONS = {
    "greeting":             ["Admission process?", "Courses available?", "Fee structure?", "Placement record?"],
    "college_overview":     ["Admission process?", "Fee structure?", "Courses offered?", "Contact details?"],
    "admission_process":    ["Eligibility criteria?", "Important dates?", "Management quota?", "Fee structure?"],
    "eligibility":          ["How to apply?", "Important dates?", "Fee structure?", "Courses offered?"],
    "important_dates":      ["Admission process?", "Eligibility?", "Fee structure?", "Contact us"],
    "management_quota":     ["Eligibility?", "Fee structure?", "Contact us", "Courses offered?"],
    "fees_general":         ["Fee breakdown?", "Scholarships available?", "Pay in installments?", "Hostel fees?"],
    "fees_breakdown":       ["Scholarships?", "Pay in installments?", "Hostel fees?", "Courses offered?"],
    "scholarships":         ["Eligibility criteria?", "Fee structure?", "How to apply?", "Contact us"],
    "fees_installment":     ["Full fee structure?", "Scholarships?", "Contact us"],
    "programs_overview":    ["Tell me about CSE", "Tell me about AI&DS", "Tell me about Cyber Security", "Fees?"],
    "program_cse":          ["CSE placements?", "Eligibility for CSE?", "Other courses?", "Fee structure?"],
    "program_it":           ["IT placements?", "Eligibility for IT?", "Other courses?", "Fee structure?"],
    "program_aids":         ["AI&DS placements?", "Eligibility?", "Other courses?", "Fee structure?"],
    "program_cyber":        ["Cyber placements?", "Eligibility?", "Other courses?", "Fee structure?"],
    "program_mech":         ["Mech placements?", "Eligibility?", "Other courses?", "Fee structure?"],
    "placements_overview":  ["Top recruiting companies?", "Salary packages?", "Programs offered?", "Admission process?"],
    "placements_companies": ["Salary packages?", "Placement percentage?", "Programs offered?", "Contact us"],
    "placements_package":   ["Top companies?", "Placement percentage?", "Courses offered?"],
    "hostel":               ["Hostel fees?", "Transport details?", "Campus facilities?", "Contact us"],
    "transport":            ["Transport fees?", "Hostel details?", "Contact us"],
    "facilities_overview":  ["Library details?", "Lab details?", "Sports facilities?", "Hostel?"],
    "library":              ["Lab facilities?", "Sports?", "Campus details?", "Contact us"],
    "labs":                 ["Library?", "Sports?", "Hostel?", "Courses offered?"],
    "sports":               ["Hostel?", "Transport?", "Other facilities?"],
    "faculty":              ["Courses offered?", "Placement record?", "Contact us"],
    "contact":              ["Admission process?", "Fee structure?", "Courses offered?"],
    "naac_accreditation":   ["About the college?", "Courses offered?", "Placement record?"],
    "affiliation":          ["About the college?", "Admission process?", "Courses offered?"],
    "campus":               ["Hostel?", "Transport?", "Facilities?", "Contact us"],
    "thanks":               ["Admission process?", "Fee structure?", "Courses offered?"],
    "goodbye":              [],
}

class IntentClassifier:
    def __init__(self, nlp_service):
        self.nlp = nlp_service
        self.pipeline = None
        self.intent_responses = {}
        self.last_intent = ""
        self.train()

    def train(self):
        print("Training intent classifier...")
        intents = DataService.get_intents()
        if not intents:
            print("No intents found in DB")
            return

        patterns, labels = [], []
        for intent in intents:
            tag = intent["tag"]
            self.intent_responses[tag] = intent["responses"]
            for pattern in intent["patterns"]:
                patterns.append(pattern.lower())
                labels.append(tag)

        self.pipeline = Pipeline([
            ("tfidf", TfidfVectorizer(
                lowercase=True,
                stop_words="english",
                ngram_range=(1, 2),
                max_features=6000,
            )),
            ("clf", MultinomialNB(alpha=0.05)),
        ])
        self.pipeline.fit(patterns, labels)
        print(f"Trained: {len(patterns)} patterns | {len(set(labels))} intents")

    def classify(self, text: str):
        text_lower = text.lower().strip()

        # Step 1: keyword override (fast, reliable)
        override = self._keyword_match(text_lower)
        if override:
            self.last_intent = override
            return override, 0.99

        # Step 2: ML model fallback
        if not self.pipeline:
            return "unknown", 0.0

        clean = self.nlp.preprocess(text)
        pred = self.pipeline.predict([clean])[0]
        proba = self.pipeline.predict_proba([clean])[0]
        confidence = float(np.max(proba))

        if confidence < 0.15:
            pred = "unknown"

        self.last_intent = pred
        return pred, confidence

    def _keyword_match(self, text: str) -> str:
        for intent_tag, keywords in KEYWORD_OVERRIDES.items():
            for kw in keywords:
                if kw in text:
                    return intent_tag
        return ""

    def get_response(self, intent: str) -> str:
        if intent == "unknown":
            return (
                "I'm not sure I understood that.\n\n"
                "You can ask me about:\n"
                "• Admission process & steps\n"
                "• Eligibility criteria\n"
                "• Fees & scholarships\n"
                "• Courses (CSE, IT, AI&DS, Cyber, MECH)\n"
                "• Placement record & companies\n"
                "• Hostel, transport & facilities\n"
                "• Contact information\n\n"
                "Try: 'How to apply?' or 'What are the fees?'"
            )
        responses = self.intent_responses.get(intent, [])
        if not responses:
            return self.get_response("unknown")
        return random.choice(responses)

    def get_suggestions(self, intent: str) -> list:
        return SUGGESTIONS.get(intent, ["Admission process?", "Fee structure?", "Courses?", "Contact us"])