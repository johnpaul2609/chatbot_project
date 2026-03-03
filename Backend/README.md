# 🎓 College Chatbot Backend - SQLite Version

## ⚡ SUPER FAST SETUP (5 Minutes!)

### Step 1: Create Virtual Environment (1 min)
```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```

### Step 2: Install Packages (2 min)
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### Step 3: Create Database (30 seconds)
```bash
python create_database.py
```

### Step 4: Configure Environment (30 seconds)
```bash
# Copy .env.example to .env
copy .env.example .env     # Windows
# or
cp .env.example .env       # Mac/Linux

# Edit .env and change:
# CORS_ORIGINS=http://localhost:5173
```

### Step 5: Run! (10 seconds)
```bash
python run.py
```

✅ **Backend running at:** http://localhost:8000
✅ **API Docs at:** http://localhost:8000/docs

---

## 🎯 What You'll See:

```
🚀 Starting chatbot backend with SQLite...
✅ SQLite connected! Found 15 intents
✅ NLP model loaded
🎓 Training intent classifier...
✅ Trained on 50+ patterns, 15 intents
INFO: Uvicorn running on http://0.0.0.0:8000
```

---

## 📁 Project Structure:

```
chatbot-sqlite-backend/
├── college_chatbot.db       (auto-created)
├── create_database.py       ← Run this first!
├── run.py                   ← Then run this!
├── requirements.txt
├── .env.example
├── app/
│   ├── main.py
│   ├── models.py
│   ├── database_sqlite.py
│   ├── routes/
│   │   └── chat.py
│   └── services/
│       ├── data_service_sqlite.py
│       ├── nlp_service.py
│       └── intent_classifier.py
```

---

## 🧪 Test Your Setup:

### 1. Test in Browser:
- Visit: http://localhost:8000
- Should see: `{"message": "College Chatbot API is running!", "database": "SQLite"}`

### 2. Test API Docs:
- Visit: http://localhost:8000/docs
- Try the `/api/chat/message` endpoint

### 3. Test with cURL:
```bash
curl -X POST "http://localhost:8000/api/chat/message" \
  -H "Content-Type: application/json" \
  -d '{"message": "What are the fees?", "user_id": "test"}'
```

---

## ✅ What's Included:

- ✅ SQLite database (no installation needed!)
- ✅ 15 trained intents
- ✅ 50+ training patterns
- ✅ NLP with spaCy
- ✅ ML intent classification
- ✅ Conversation history
- ✅ Smart suggestions
- ✅ FastAPI with auto docs

---

## 🔧 Troubleshooting:

### "Database file not found"
```bash
python create_database.py
```

### "Module not found"
```bash
pip install -r requirements.txt
```

### "spaCy model not found"
```bash
python -m spacy download en_core_web_sm
```

### CORS error from React
Edit `.env`:
```
CORS_ORIGINS=http://localhost:5173
```
Then restart: `python run.py`

---

## 🎯 API Endpoints:

- `POST /api/chat/message` - Send message
- `GET /api/chat/history/{user_id}` - Get history
- `DELETE /api/chat/history/{user_id}` - Clear history
- `GET /health` - Health check
- `GET /docs` - API documentation

---

## 📊 Database Info:

**File:** `college_chatbot.db` (SQLite)

**Tables:**
- colleges (1 record)
- programs (4 records)
- facilities (5 records)
- placements (1 record)
- intents (15 records)
- intent_patterns (50+ records)
- intent_responses (15 records)
- conversations (auto-filled)
- study_materials (3 records)

---

## 🚀 Ready to Deploy!

Your backend is ready to connect with your React frontend!

**Next:** Update your React chatbot component's API URL to `http://localhost:8000`

---

## 💯 Total Setup Time: 5 Minutes!

No PostgreSQL, no passwords, no hassle! Just works! ✨
