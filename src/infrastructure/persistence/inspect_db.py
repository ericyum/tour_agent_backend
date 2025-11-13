import sqlite3
import os

# Auto-detect sibling database directory
backend_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
parent_dir = os.path.dirname(backend_root)
default_database_path = os.path.join(parent_dir, "tour_agent_database")

# Use environment variable if set, otherwise use auto-detected path
DATABASE_PATH = os.getenv("DATABASE_PATH", default_database_path)
db_path = os.path.join(DATABASE_PATH, "tour.db")

print(f"Inspecting database at: {db_path}")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("Schema for 'festivals' table:")
cursor.execute("PRAGMA table_info(festivals)")
for row in cursor.fetchall():
    print(row)

conn.close()
