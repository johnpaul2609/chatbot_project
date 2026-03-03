import sqlite3
import os

class Database:
    """SQLite Database Manager"""
    
    DB_PATH = "college_chatbot.db"
    
    @staticmethod
    def get_connection():
        """Get database connection"""
        if not os.path.exists(Database.DB_PATH):
            raise FileNotFoundError(
                f"Database file not found: {Database.DB_PATH}\n"
                f"Please run: python create_database.py"
            )
        conn = sqlite3.connect(Database.DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    
    @staticmethod
    def test_connection():
        """Test database connection"""
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM intents")
            count = cursor.fetchone()[0]
            conn.close()
            print(f"✅ SQLite connected! Found {count} intents")
            return True
        except Exception as e:
            print(f"❌ SQLite error: {e}")
            return False
    
    @staticmethod
    def execute_query(query: str, params: tuple = ()):
        """Execute query and return results"""
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        return results
    
    @staticmethod
    def execute_insert(query: str, params: tuple = ()):
        """Execute insert/update query"""
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        last_id = cursor.lastrowid
        conn.close()
        return last_id
    
import sqlite3

def create_tables():
    conn = sqlite3.connect("college_chatbot.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS intents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tag TEXT NOT NULL,
        context TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patterns (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        intent_id INTEGER,
        pattern TEXT NOT NULL,
        FOREIGN KEY(intent_id) REFERENCES intents(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS responses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        intent_id INTEGER,
        response TEXT NOT NULL,
        FOREIGN KEY(intent_id) REFERENCES intents(id)
    )
    """)

    conn.commit()
    conn.close()
    print("✅ Tables created successfully")

