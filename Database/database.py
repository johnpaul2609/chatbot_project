import sqlite3
from datetime import datetime

# Create database file
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

# Create colleges table
cursor.execute("""
CREATE TABLE colleges (
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
)
""")

# Create programs table
cursor.execute("""
CREATE TABLE programs (
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
)
""")

# Create facilities table
cursor.execute("""
CREATE TABLE facilities (
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
)
""")

# Create placements table
cursor.execute("""
CREATE TABLE placements (
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
)
""")

# Create intents table
cursor.execute("""
CREATE TABLE intents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tag TEXT UNIQUE NOT NULL,
    context TEXT,
    description TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
)
""")

# Create intent_patterns table
cursor.execute("""
CREATE TABLE intent_patterns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    intent_id INTEGER,
    pattern TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (intent_id) REFERENCES intents(id) ON DELETE CASCADE
)
""")

# Create intent_responses table
cursor.execute("""
CREATE TABLE intent_responses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    intent_id INTEGER,
    response TEXT NOT NULL,
    priority INTEGER DEFAULT 1,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (intent_id) REFERENCES intents(id) ON DELETE CASCADE
)
""")

# Create conversations table
cursor.execute("""
CREATE TABLE conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    message TEXT NOT NULL,
    processed_message TEXT,
    intent TEXT,
    response TEXT,
    confidence REAL,
    session_id TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
)
""")

# Create indexes
cursor.execute("CREATE INDEX idx_conv_user ON conversations(user_id)")
cursor.execute("CREATE INDEX idx_conv_date ON conversations(created_at)")

# Create study_materials table
cursor.execute("""
CREATE TABLE study_materials (
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
)
""")

cursor.execute("CREATE INDEX idx_mat_subject ON study_materials(subject)")
cursor.execute("CREATE INDEX idx_mat_dept ON study_materials(department)")

print("✅ Tables created!")

# Insert sample data
print("📚 Inserting sample data...")

# Insert college
cursor.execute("""
INSERT INTO colleges (name, location, established, affiliation, type, phone, email, website, address, naac_grade)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    'St Lourdes Engineering College',
    'Chennai, Tamil Nadu, India',
    2005,
    'Anna University',
    'Private Engineering College',
    '+91-44-12345678',
    'admissions@stlourdes.edu',
    'www.stlourdes.edu',
    'St Lourdes Engineering College, Chennai - 600001',
    'A'
))

# Insert programs
programs_data = [
    (1, 'Computer Science and Engineering', 'CSE', 'UG', 4, 180, 85000,
     'Master programming, AI, machine learning, and software development',
     'Passed 12th with PCM, minimum 50% marks'),
    (1, 'Electronics and Communication Engineering', 'ECE', 'UG', 4, 120, 80000,
     'Learn about circuits, communication systems, embedded systems',
     'Passed 12th with PCM, minimum 50% marks'),
    (1, 'Mechanical Engineering', 'Mechanical', 'UG', 4, 120, 75000,
     'Study thermodynamics, manufacturing, robotics',
     'Passed 12th with PCM, minimum 50% marks'),
    (1, 'Civil Engineering', 'Civil', 'UG', 4, 60, 70000,
     'Focus on construction, structural design, infrastructure',
     'Passed 12th with PCM, minimum 50% marks'),
]

cursor.executemany("""
INSERT INTO programs (college_id, name, department, degree_type, duration, seats, 
                     fees_per_year, description, eligibility)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", programs_data)

# Insert facilities
facilities_data = [
    (1, 'Central Library', 'Library', '15,000+ books and digital resources', 500, 0, 1),
    (1, 'Computer Lab', 'Laboratory', 'Latest hardware and software', 60, 0, 1),
    (1, 'Electronics Lab', 'Laboratory', 'Advanced electronics lab', 50, 0, 1),
    (1, 'Boys Hostel', 'Hostel', 'Mess and 24/7 security', 300, 50000, 1),
    (1, 'Girls Hostel', 'Hostel', 'Mess and 24/7 security', 200, 50000, 1),
    (1, 'Sports Complex', 'Sports', 'Cricket, football, basketball', 1000, 0, 1),
]

cursor.executemany("""
INSERT INTO facilities (college_id, name, category, description, capacity, fees, available)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", facilities_data)

# Insert placement data
cursor.execute("""
INSERT INTO placements (college_id, year, department, total_students, placed_students,
                       placement_percentage, avg_package, highest_package, top_recruiters)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (1, 2025, 'CSE', 180, 160, 88.89, 450000, 1200000, 'TCS,Infosys,Wipro,Cognizant,Amazon,Accenture'))

# Insert intents
intents_data = [
    ('greeting', 'greeting', 'User greets the bot'),
    ('admission_process', 'admission', 'Questions about admission'),
    ('eligibility', 'admission', 'Questions about eligibility'),
    ('fees', 'fees', 'Questions about fees'),
    ('programs_offered', 'programs', 'Questions about programs'),
    ('cse_details', 'programs', 'CSE program details'),
    ('placements', 'placements', 'Questions about placements'),
    ('facilities', 'facilities', 'Questions about facilities'),
    ('hostel', 'facilities', 'Questions about hostel'),
    ('faculty', 'faculty', 'Questions about faculty'),
    ('contact', 'contact', 'Contact information'),
    ('important_dates', 'admission', 'Admission dates'),
    ('thanks', '', 'User thanks the bot'),
    ('goodbye', '', 'User ends conversation'),
    ('request_notes', 'notes', 'User requests study materials'),
]

cursor.executemany("""
INSERT INTO intents (tag, context, description) VALUES (?, ?, ?)
""", intents_data)

# Insert intent patterns
patterns = [
    (1, 'Hi'), (1, 'Hello'), (1, 'Hey'), (1, 'Good morning'),
    (2, 'How do I apply?'), (2, 'Admission process'), (2, 'How to get admission?'),
    (3, 'Eligibility criteria'), (3, 'Am I eligible?'), (3, 'What marks needed?'),
    (4, 'What are the fees?'), (4, 'Fee structure'), (4, 'How much cost?'),
    (5, 'What courses?'), (5, 'Available programs'), (5, 'Which branches?'),
    (6, 'Tell me about CSE'), (6, 'Computer Science details'),
    (7, 'Placements?'), (7, 'Placement records'), (7, 'Job opportunities'),
    (8, 'What facilities?'), (8, 'Infrastructure'), (8, 'Campus facilities'),
    (9, 'Hostel available?'), (9, 'Accommodation'), (9, 'Hostel details'),
    (10, 'Faculty details'), (10, 'About teachers'), (10, 'How are professors?'),
    (11, 'Contact details'), (11, 'Phone number'), (11, 'How to contact?'),
    (12, 'When can I apply?'), (12, 'Application dates'), (12, 'Important dates'),
    (13, 'Thanks'), (13, 'Thank you'), (13, 'Thanks a lot'),
    (14, 'Bye'), (14, 'Goodbye'), (14, 'See you later'),
    (15, 'I need notes'), (15, 'Study material'), (15, 'Send me notes'),
]

cursor.executemany("""
INSERT INTO intent_patterns (intent_id, pattern) VALUES (?, ?)
""", patterns)

# Insert responses
responses = [
    (1, 'Hello! Welcome to St Lourdes Engineering College. How can I assist you today?'),
    (2, 'Admissions are based on TNEA counseling. Applications open in May. Would you like to know about eligibility?'),
    (3, 'For UG: Passed 12th with PCM, minimum 50% marks. For PG: B.E/B.Tech with 50% marks.'),
    (4, 'UG fees: ₹70,000-₹85,000/year. PG: ₹60,000/year. Hostel: ₹50,000/year. Would you like details?'),
    (5, 'We offer CSE (180 seats), ECE (120 seats), Mechanical (120 seats), Civil (60 seats). Which interests you?'),
    (6, 'CSE is a 4-year program with 180 seats. Fees: ₹85,000/year. Covers AI, ML, software development.'),
    (7, '85% placement rate. Average: 4.5 LPA, Highest: 12 LPA. Top recruiters: TCS, Infosys, Amazon.'),
    (8, 'We have library (15,000+ books), labs, hostels, sports facilities, and bus transport.'),
    (9, 'Yes! Separate hostels for boys and girls. ₹50,000/year includes accommodation and food.'),
    (10, 'We have 85 faculty members, including 32 PhD holders with 5-25 years experience.'),
    (11, 'Phone: +91-44-12345678, Email: admissions@stlourdes.edu, Address: Chennai - 600001'),
    (12, 'Applications open: May 2026, Deadline: June 2026, Classes begin: August 2026'),
    (13, 'You\'re welcome! Feel free to ask more questions.'),
    (14, 'Goodbye! Best of luck with your admission!'),
    (15, 'I can help with study materials. Which subject: Computer Networks, Data Structures, Math?'),
]

cursor.executemany("""
INSERT INTO intent_responses (intent_id, response) VALUES (?, ?)
""", responses)

# Insert study materials
materials = [
    ('mat_001', 'Computer Networks', 'OSI Model', 'CN_OSI_Model.pdf',
     'materials/cn/osi_model.pdf', '7-layer OSI Model notes', 'CSE', 3, 2458624,
     'networking,osi,protocols'),
    ('mat_002', 'Data Structures', 'Trees', 'DS_Trees.pdf',
     'materials/ds/trees.pdf', 'Binary trees, BST, AVL', 'CSE', 3, 3145728,
     'trees,algorithms,data structures'),
    ('mat_003', 'Mathematics', 'Calculus', 'Math_Calculus.pdf',
     'materials/math/calculus.pdf', 'Differentiation and integration', 'All', 1, 1835008,
     'calculus,math,integration'),
]

cursor.executemany("""
INSERT INTO study_materials (material_id, subject, topic, file_name, file_path,
                            description, department, semester, file_size, tags)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", materials)

conn.commit()

# Verify data
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
cursor.execute("SELECT COUNT(*) FROM study_materials")
print(f"Study Materials: {cursor.fetchone()[0]}")

print("\n✅ Database file created: college_chatbot.db")
print("You can now use this database with your chatbot!")

conn.close()