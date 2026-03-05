import sqlite3
import os

db_path = os.path.join('backend', 'instance', 'evaluation.db')
print(f"Updating {db_path}...")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check if evaluator_role exists
cursor.execute("PRAGMA table_info(marks)")
cols = [info[1] for info in cursor.fetchall()]

# Check if we need to update the constraint
cursor.execute("PRAGMA table_info(marks)")
cols = [info[1] for info in cursor.fetchall()]

if 'evaluator_role' not in cols or True: # Force update for constraint
    print("Recreating marks table with new constraint...")
    
    # 1. Create new table
    cursor.execute("""
        CREATE TABLE marks_new (
            id INTEGER PRIMARY KEY,
            answer_sheet_id INTEGER NOT NULL,
            question_paper_id INTEGER,
            question_number INTEGER NOT NULL,
            marks_awarded FLOAT NOT NULL,
            max_marks FLOAT NOT NULL,
            evaluator_role VARCHAR(50) NOT NULL DEFAULT 'teacher',
            created_at DATETIME,
            UNIQUE(answer_sheet_id, question_number, evaluator_role)
        )
    """)
    
    # 2. Copy data
    if 'evaluator_role' in cols:
        cursor.execute("INSERT INTO marks_new SELECT id, answer_sheet_id, question_paper_id, question_number, marks_awarded, max_marks, evaluator_role, created_at FROM marks")
    else:
        cursor.execute("INSERT INTO marks_new (id, answer_sheet_id, question_paper_id, question_number, marks_awarded, max_marks, created_at) SELECT id, answer_sheet_id, question_paper_id, question_number, marks_awarded, max_marks, created_at FROM marks")
    
    # 3. Drop old table
    cursor.execute("DROP TABLE marks")
    
    # 4. Rename new table
    cursor.execute("ALTER TABLE marks_new RENAME TO marks")
    
    print("Marks table recreated.")
else:
    print("Constraint already updated.")

conn.commit()
conn.close()
print("Migration done.")
