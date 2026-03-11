import sqlite3

conn = sqlite3.connect("college_chatbot.db")
cursor = conn.cursor()

print("Training admission support...")

# Admission intents
intents = [
("admission_courses","admission","Courses information"),
("admission_fees","admission","Fee structure"),
("admission_hostel","admission","Hostel facility"),
("admission_placements","admission","Placement information"),
("admission_location","admission","College location")
]

cursor.executemany(
    "INSERT OR IGNORE INTO intents (tag,context,description) VALUES (?,?,?)",
    intents
)

# Admission patterns
patterns = [
("admission_courses","what courses are available"),
("admission_courses","list of courses"),
("admission_courses","what programs do you offer"),
("admission_courses","engineering branches"),

("admission_fees","what are the fees"),
("admission_fees","fee structure"),
("admission_fees","how much is the tuition fee"),

("admission_hostel","do you have hostel"),
("admission_hostel","hostel facility"),
("admission_hostel","boys hostel"),
("admission_hostel","girls hostel"),

("admission_placements","placement record"),
("admission_placements","companies visiting"),
("admission_placements","placement support"),

("admission_location","where is the college"),
("admission_location","college location"),
("admission_location","address of the college")
]

for tag,pattern in patterns:
    cursor.execute(
        "SELECT id FROM intents WHERE tag=?",
        (tag,)
    )
    intent_id = cursor.fetchone()[0]

    cursor.execute(
        "INSERT INTO intent_patterns (intent_id,pattern) VALUES (?,?)",
        (intent_id,pattern)
    )

# Admission responses
responses = [
("admission_courses","Our college offers B.Tech IT, AI&DS, CSE, Cyber Security and CSC."),
("admission_fees","The annual tuition fee is ₹60,000."),
("admission_hostel","Yes, hostel facilities are available for boys and girls."),
("admission_placements","Yes, our college provides placement support."),
("admission_location","St Lourdes Engineering College is located in Anagaputhur.")
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

print("Admission training added successfully")