import sqlite3

conn = sqlite3.connect("college_chatbot.db")
cursor = conn.cursor()

print("Training academic support...")

intents = [
("academic_departments","academic","Departments"),
("academic_subjects","academic","Subjects"),
("academic_faculty","academic","Faculty information"),
("academic_library","academic","Library information"),
("academic_labs","academic","Lab information")
]

cursor.executemany(
"INSERT INTO intents (tag,context,description) VALUES (?,?,?)",
intents
)

responses = [
("academic_departments","Departments include IT, AI&DS, CSE, Cyber Security and CSC."),
("academic_subjects","Subjects include programming, AI, machine learning, networking and databases."),
("academic_faculty","Our college has experienced faculty members in each department."),
("academic_library","Yes, the college has a central library with many technical books."),
("academic_labs","Yes, the college provides modern laboratories for each department.")
]

for tag,response in responses:
    cursor.execute(
        "SELECT id FROM intents WHERE tag=?",
        (tag,)
    )
    intent_id = cursor.fetchone()[0]

    cursor.execute(
        "INSERT INTO intent_responses (intent_id,response) VALUES (?,?)",
        (intent_id,response)
    )

conn.commit()
conn.close()

print("Academic training added successfully")