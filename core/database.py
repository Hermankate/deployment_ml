# # core/database.py
# import sqlite3
# import pandas as pd
# from config.settings import DATABASE_PATH

# class DatabaseManager:
#     def __init__(self):
#         self.conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
#         self._init_db()

#     def _init_db(self):
#         cursor = self.conn.cursor()
#         cursor.execute("""
#             CREATE TABLE IF NOT EXISTS candidates (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 name TEXT,
#                 resume_text TEXT,
#                 job_description TEXT,
#                 score REAL,
#                 category TEXT,
#                 timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
#             )
#         """)
#         self.conn.commit()

#     def store_results(self, candidates, job_desc):
#         cursor = self.conn.cursor()
#         cursor.execute("DELETE FROM candidates")
#         for candidate in candidates:
#             cursor.execute("""
#                 INSERT INTO candidates 
#                 (name, resume_text, job_description, score, category)
#                 VALUES (?, ?, ?, ?, ?)
#             """, (
#                 candidate.get('name', 'Unknown'),  # Ensure name extraction
#                 candidate['resume_text'],
#                 job_desc,
#                 candidate['score'],
#                 candidate['category']
#             ))
#         self.conn.commit()
#     def get_historical_results(self, limit=50):
#         return pd.read_sql(
#             "SELECT name, score, category, timestamp FROM candidates ORDER BY timestamp DESC LIMIT ?",
#             self.conn,
#             params=(limit,)
#         )

#     def __del__(self):
#         self.conn.close()

# import sqlite3
# import pandas as pd
# from config.settings import DATABASE_PATH

# class DatabaseManager:
#     def __init__(self):
#         self.conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
#         self._init_db()

#     def _init_db(self):
#         cursor = self.conn.cursor()
#         cursor.execute("""
#             CREATE TABLE IF NOT EXISTS candidates (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 name TEXT,
#                 resume_text TEXT,
#                 job_description TEXT,
#                 score REAL,
#                 category TEXT,
#                 analysis TEXT,
#                 timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
#             )
#         """)
#         self.conn.commit()

#     def store_results(self, candidates, job_desc):
#         cursor = self.conn.cursor()
#         cursor.execute("DELETE FROM candidates")
#         for candidate in candidates:
#             cursor.execute("""
#                 INSERT INTO candidates 
#                 (name, resume_text, job_description, score, category, analysis)
#                 VALUES (?, ?, ?, ?, ?, ?)
#             """, (
#                 candidate.get('name', 'Unknown'),
#                 candidate['resume_text'],
#                 job_desc,
#                 candidate['score'],
#                 candidate['category'],
#                 candidate['analysis']
#             ))
#         self.conn.commit()

#     def get_historical_results(self, limit=50):
#         return pd.read_sql(
#             "SELECT name, score, category, analysis, timestamp FROM candidates ORDER BY timestamp DESC LIMIT ?",
#             self.conn,
#             params=(limit,)
#         )

#     def __del__(self):
#         self.conn.close()
import sqlite3
import pandas as pd
from config.settings import DATABASE_PATH

class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
        self._init_db()

    def _init_db(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS candidates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                resume_text TEXT NOT NULL,
                job_description TEXT NOT NULL,
                score REAL NOT NULL,
                category TEXT NOT NULL,
                analysis TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()

    def store_results(self, candidates, job_desc):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM candidates")
        for candidate in candidates:
            cursor.execute("""
                INSERT INTO candidates 
                (name, resume_text, job_description, score, category, analysis)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                candidate['name'],
                candidate['resume_text'],
                job_desc,
                candidate['score'],
                candidate['category'],
                candidate['analysis']
            ))
        self.conn.commit()

    def get_historical_results(self, limit=50):
        return pd.read_sql(
            """SELECT name, score, category, analysis, timestamp 
               FROM candidates 
               ORDER BY timestamp DESC 
               LIMIT ?""",
            self.conn,
            params=(limit,)
        )

    def __del__(self):
        self.conn.close()