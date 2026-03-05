import sqlite3
import os

db_path = os.path.join('backend', 'instance', 'evaluation.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='marks'")
result = cursor.fetchone()
if result:
    print(result[0])
else:
    print("Table 'marks' not found")
conn.close()
