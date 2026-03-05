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
        """Execute SELECT query"""
        conn = Database.get_connection()
        cursor = conn.cursor()

        cursor.execute(query, params)
        results = cursor.fetchall()

        conn.close()
        return results

    @staticmethod
    def execute_insert(query: str, params: tuple = ()):
        """Execute INSERT / UPDATE query"""
        conn = Database.get_connection()
        cursor = conn.cursor()

        cursor.execute(query, params)
        conn.commit()

        last_id = cursor.lastrowid
        conn.close()

        return last_id  