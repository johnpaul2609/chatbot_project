import sqlite3

conn = sqlite3.connect('college_chatbot.db')
cursor = conn.cursor()

print("🔄 Creating database tables...")

# Drop existing tables
cursor.execute("DROP TABLE IF EXISTS conversations")
cursor.execute("DROP TABLE IF EXISTS study_materials")
cursor.execute("DROP TABLE IF EXISTS intent_responses")
cursor.execute("DROP TABLE IF EXISTS intent_patterns")
cursor.execute("DROP TABLE IF EXISTS intents")
cursor.execute("DROP TABLE IF EXISTS placements")
cursor.execute("DROP TABLE IF EXISTS facilities")
cursor.execute("DROP TABLE IF EXISTS programs")
cursor.execute("DROP TABLE IF EXISTS colleges")

# Create tables
cursor.execute("""CREATE TABLE colleges (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    location TEXT,
    established INTEGER,
    affiliation TEXT,
    type TEXT,
    phone TEXT,
    email TEXT,
    website TEXT,
    address TEXT,
    naac_grade TEXT,
    aicte_approved INTEGER DEFAULT 1,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
)""")

cursor.execute("""CREATE TABLE programs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    college_id INTEGER,
    name TEXT NOT NULL,
    department TEXT,
    degree_type TEXT,
    duration INTEGER,
    seats INTEGER,
    fees_per_year REAL,
    description TEXT,
    eligibility TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (college_id) REFERENCES colleges(id)
)""")

cursor.execute("""CREATE TABLE facilities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    college_id INTEGER,
    name TEXT NOT NULL,
    category TEXT,
    description TEXT,
    capacity INTEGER,
    fees REAL,
    available INTEGER DEFAULT 1,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (college_id) REFERENCES colleges(id)
)""")

cursor.execute("""CREATE TABLE placements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    college_id INTEGER,
    year INTEGER NOT NULL,
    department TEXT,
    total_students INTEGER,
    placed_students INTEGER,
    placement_percentage REAL,
    avg_package REAL,
    highest_package REAL,
    lowest_package REAL,
    top_recruiters TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (college_id) REFERENCES colleges(id)
)""")

cursor.execute("""CREATE TABLE intents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tag TEXT UNIQUE NOT NULL,
    context TEXT,
    description TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
)""")

cursor.execute("""CREATE TABLE intent_patterns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    intent_id INTEGER,
    pattern TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (intent_id) REFERENCES intents(id) ON DELETE CASCADE
)""")

cursor.execute("""CREATE TABLE intent_responses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    intent_id INTEGER,
    response TEXT NOT NULL,
    priority INTEGER DEFAULT 1,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (intent_id) REFERENCES intents(id) ON DELETE CASCADE
)""")

cursor.execute("""CREATE TABLE conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    message TEXT NOT NULL,
    processed_message TEXT,
    intent TEXT,
    response TEXT,
    confidence REAL,
    session_id TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
)""")

cursor.execute("CREATE INDEX idx_conv_user ON conversations(user_id)")
cursor.execute("CREATE INDEX idx_conv_date ON conversations(created_at)")

cursor.execute("""CREATE TABLE study_materials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    material_id TEXT UNIQUE NOT NULL,
    subject TEXT NOT NULL,
    topic TEXT NOT NULL,
    file_name TEXT NOT NULL,
    file_path TEXT NOT NULL,
    description TEXT,
    department TEXT,
    semester INTEGER,
    file_size INTEGER,
    upload_date TEXT DEFAULT CURRENT_TIMESTAMP,
    downloads INTEGER DEFAULT 0,
    tags TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
)""")

cursor.execute("CREATE INDEX idx_mat_subject ON study_materials(subject)")
cursor.execute("CREATE INDEX idx_mat_dept ON study_materials(department)")

print("✅ Tables created!")
print("📚 Inserting sample data...")

# Insert college
cursor.execute("""INSERT INTO colleges (name, location, established, affiliation, type, phone, email, website, address, naac_grade)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (
    'St Lourdes Engineering College', 'Chennai, Tamil Nadu, India', 2005, 'Anna University',
    'Private Engineering College', '+91-44-12345678', 'admissions@stlourdes.edu',
    'www.stlourdes.edu', 'Chennai - 600001', 'A'
))

# Insert programs
programs_data = [
    (1, 'Computer Science and Engineering', 'CSE', 'UG', 4, 180, 85000,
     'Master programming, AI, ML, and software development', 'Passed 12th with PCM, 50% marks'),
    (1, 'Electronics and Communication', 'ECE', 'UG', 4, 120, 80000,
     'Circuits, communication systems, embedded systems', 'Passed 12th with PCM, 50% marks'),
    (1, 'Mechanical Engineering', 'Mechanical', 'UG', 4, 120, 75000,
     'Thermodynamics, manufacturing, robotics', 'Passed 12th with PCM, 50% marks'),
    (1, 'Civil Engineering', 'Civil', 'UG', 4, 60, 70000,
     'Construction, structural design', 'Passed 12th with PCM, 50% marks'),
]
cursor.executemany("""INSERT INTO programs (college_id, name, department, degree_type, duration, seats, 
                     fees_per_year, description, eligibility) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", programs_data)

# Insert facilities
facilities_data = [
    (1, 'Central Library', 'Library', '15,000+ books', 500, 0, 1),
    (1, 'Computer Lab', 'Laboratory', 'Latest hardware', 60, 0, 1),
    (1, 'Boys Hostel', 'Hostel', 'Mess and security', 300, 50000, 1),
    (1, 'Girls Hostel', 'Hostel', 'Mess and security', 200, 50000, 1),
    (1, 'Sports Complex', 'Sports', 'Cricket, football', 1000, 0, 1),
]
cursor.executemany("""INSERT INTO facilities (college_id, name, category, description, capacity, fees, available)
VALUES (?, ?, ?, ?, ?, ?, ?)""", facilities_data)

# Insert placements
cursor.execute("""INSERT INTO placements (college_id, year, department, total_students, placed_students,
                       placement_percentage, avg_package, highest_package, top_recruiters)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", (1, 2025, 'CSE', 180, 160, 88.89, 450000, 1200000, 'TCS,Infosys,Amazon'))

# Insert intents
intents_data = [
    ('greeting', 'greeting', 'User greets'), ('admission_process', 'admission', 'Admission questions'),
    ('eligibility', 'admission', 'Eligibility'), ('fees', 'fees', 'Fee questions'),
    ('programs_offered', 'programs', 'Programs'), ('cse_details', 'programs', 'CSE details'),
    ('placements', 'placements', 'Placements'), ('facilities', 'facilities', 'Facilities'),
    ('hostel', 'facilities', 'Hostel'), ('faculty', 'faculty', 'Faculty'),
    ('contact', 'contact', 'Contact'), ('important_dates', 'admission', 'Dates'),
    ('thanks', '', 'Thanks'), ('goodbye', '', 'Goodbye'), ('request_notes', 'notes', 'Notes'),
]
cursor.executemany("INSERT INTO intents (tag, context, description) VALUES (?, ?, ?)", intents_data)

# Insert patterns
patterns = [
    (1, 'Hi'), (1, 'Hello'), (1, 'Hey'), (2, 'How do I apply?'), (2, 'Admission process'),
    (3, 'Eligibility?'), (3, 'Am I eligible?'), (4, 'What are fees?'), (4, 'Fee structure'),
    (5, 'What courses?'), (5, 'Programs?'), (6, 'Tell me about CSE'), (7, 'Placements?'),
    (8, 'Facilities?'), (9, 'Hostel?'), (10, 'Faculty?'), (11, 'Contact?'),
    (12, 'When to apply?'), (13, 'Thanks'), (14, 'Bye'), (15, 'I need notes'),
]
cursor.executemany("INSERT INTO intent_patterns (intent_id, pattern) VALUES (?, ?)", patterns)

# Insert responses
responses = [
    (1, 'Hello! Welcome to St Lourdes Engineering College. How can I assist you?'),
    (2, 'Admissions are based on TNEA counseling. Applications open in May.'),
    (3, 'For UG: Passed 12th with PCM, 50% marks. For PG: B.E/B.Tech with 50% marks.'),
    (4, 'UG fees: ₹70,000-₹85,000/year. PG: ₹60,000/year. Hostel: ₹50,000/year.'),
    (5, 'We offer CSE (180 seats), ECE (120 seats), Mechanical (120 seats), Civil (60 seats).'),
    (6, 'CSE: 4-year program, 180 seats, ₹85,000/year. Covers AI, ML, software development.'),
    (7, '85% placement rate. Average: 4.5 LPA, Highest: 12 LPA. Top: TCS, Infosys, Amazon.'),
    (8, 'Library (15,000+ books), labs, hostels, sports facilities, bus transport.'),
    (9, 'Yes! Separate hostels for boys and girls. ₹50,000/year includes accommodation and food.'),
    (10, 'We have 85 faculty members, including 32 PhD holders with 5-25 years experience.'),
    (11, 'Phone: +91-44-12345678, Email: admissions@stlourdes.edu, Address: Chennai - 600001'),
    (12, 'Applications: May 2026, Deadline: June 2026, Classes: August 2026'),
    (13, 'You\'re welcome! Feel free to ask more questions.'),
    (14, 'Goodbye! Best of luck!'),
    (15, 'I can help with study materials. Which subject?'),
]
cursor.executemany("INSERT INTO intent_responses (intent_id, response) VALUES (?, ?)", responses)

# Insert materials
materials = [
    ('mat_001', 'Computer Networks', 'OSI Model', 'CN_OSI.pdf', 'materials/cn/osi.pdf', 
     'OSI Model notes', 'CSE', 3, 2458624, 'networking,osi'),
    ('mat_002', 'Data Structures', 'Trees', 'DS_Trees.pdf', 'materials/ds/trees.pdf',
     'Binary trees, BST', 'CSE', 3, 3145728, 'trees,algorithms'),
    ('mat_003', 'Mathematics', 'Calculus', 'Math_Calculus.pdf', 'materials/math/calc.pdf',
     'Calculus notes', 'All', 1, 1835008, 'calculus,math'),
]
cursor.executemany("""INSERT INTO study_materials (material_id, subject, topic, file_name, file_path,
                            description, department, semester, file_size, tags)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", materials)

conn.commit()

print("\n✅ Database created successfully!")
print("\n📊 Statistics:")
cursor.execute("SELECT COUNT(*) FROM programs")
print(f"Programs: {cursor.fetchone()[0]}")
cursor.execute("SELECT COUNT(*) FROM intents")
print(f"Intents: {cursor.fetchone()[0]}")
cursor.execute("SELECT COUNT(*) FROM intent_patterns")
print(f"Patterns: {cursor.fetchone()[0]}")
cursor.execute("SELECT COUNT(*) FROM facilities")
print(f"Facilities: {cursor.fetchone()[0]}")

print("\n✅ Database file: college_chatbot.db")
print("Ready to use!\n")

conn.close()
