from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.database_sqlite import Database
from app.routes import chat
from app.routes import materials
from app.routes import admin
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(
    title="College Chatbot API",
    description="Backend with SQLite",
    version="1.0.0"
)

origins = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    print("Starting chatbot backend with SQLite...")
    Database.test_connection()

@app.get("/")
async def root():
    return {"message": "College Chatbot API is running!", "database": "SQLite", "status": "active"}

@app.get("/health")
async def health_check():
    try:
        Database.test_connection()
        return {"status": "healthy", "database": "sqlite"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

app.include_router(chat.router,      prefix="/api/chat",      tags=["chat"])
app.include_router(materials.router, prefix="/api/materials", tags=["materials"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])