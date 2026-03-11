import sqlite3

conn = sqlite3.connect('college_chatbot.db')
cursor = conn.cursor()

print("Creating database...")

for table in ["conversations","study_materials","intent_responses","intent_patterns",
              "intents","faqs","scholarships","placements","facilities","subjects",
              "departments","programs","colleges"]:
    cursor.execute(f"DROP TABLE IF EXISTS {table}")

cursor.execute("""CREATE TABLE colleges (
    id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL,
    location TEXT, established INTEGER, affiliation TEXT, type TEXT,
    phone TEXT, email TEXT, website TEXT, address TEXT,
    naac_grade TEXT, aicte_approved INTEGER DEFAULT 1,
    total_students INTEGER, total_faculty INTEGER, campus_area_acres REAL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP)""")

cursor.execute("""CREATE TABLE departments (
    id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL,
    code TEXT, hod TEXT, phone TEXT, email TEXT)""")

cursor.execute("""CREATE TABLE programs (
    id INTEGER PRIMARY KEY AUTOINCREMENT, college_id INTEGER,
    name TEXT NOT NULL, short_name TEXT, department TEXT,
    degree_type TEXT, duration INTEGER, seats INTEGER,
    fees_per_year REAL, total_fees REAL,
    description TEXT, eligibility TEXT, highlights TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (college_id) REFERENCES colleges(id))""")

cursor.execute("""CREATE TABLE scholarships (
    id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL,
    type TEXT, eligibility TEXT, amount REAL, description TEXT)""")

cursor.execute("""CREATE TABLE facilities (
    id INTEGER PRIMARY KEY AUTOINCREMENT, college_id INTEGER,
    name TEXT NOT NULL, category TEXT, description TEXT,
    capacity INTEGER, fees REAL, available INTEGER DEFAULT 1,
    FOREIGN KEY (college_id) REFERENCES colleges(id))""")

cursor.execute("""CREATE TABLE placements (
    id INTEGER PRIMARY KEY AUTOINCREMENT, college_id INTEGER,
    year INTEGER, department TEXT, total_students INTEGER,
    placed_students INTEGER, placement_percentage REAL,
    avg_package REAL, highest_package REAL, top_recruiters TEXT,
    FOREIGN KEY (college_id) REFERENCES colleges(id))""")

cursor.execute("""CREATE TABLE subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT, department TEXT,
    year INTEGER, semester INTEGER, subject_name TEXT)""")

cursor.execute("""CREATE TABLE faqs (
    id INTEGER PRIMARY KEY AUTOINCREMENT, category TEXT,
    question TEXT, answer TEXT)""")

cursor.execute("""CREATE TABLE intents (
    id INTEGER PRIMARY KEY AUTOINCREMENT, tag TEXT UNIQUE NOT NULL,
    context TEXT, description TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP)""")

cursor.execute("""CREATE TABLE intent_patterns (
    id INTEGER PRIMARY KEY AUTOINCREMENT, intent_id INTEGER,
    pattern TEXT NOT NULL,
    FOREIGN KEY (intent_id) REFERENCES intents(id) ON DELETE CASCADE)""")

cursor.execute("""CREATE TABLE intent_responses (
    id INTEGER PRIMARY KEY AUTOINCREMENT, intent_id INTEGER,
    response TEXT NOT NULL, priority INTEGER DEFAULT 1,
    FOREIGN KEY (intent_id) REFERENCES intents(id) ON DELETE CASCADE)""")

cursor.execute("""CREATE TABLE conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT NOT NULL,
    message TEXT NOT NULL, processed_message TEXT, intent TEXT,
    response TEXT, confidence REAL, session_id TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP)""")

cursor.execute("""CREATE TABLE study_materials (
    id INTEGER PRIMARY KEY AUTOINCREMENT, material_id TEXT UNIQUE NOT NULL,
    subject TEXT NOT NULL, topic TEXT NOT NULL, file_name TEXT NOT NULL,
    file_path TEXT NOT NULL, description TEXT, department TEXT,
    semester INTEGER, file_size INTEGER, upload_date TEXT DEFAULT CURRENT_TIMESTAMP,
    downloads INTEGER DEFAULT 0, tags TEXT)""")

cursor.execute("CREATE INDEX idx_conv_user ON conversations(user_id)")
cursor.execute("CREATE INDEX idx_conv_date ON conversations(created_at)")

print("Tables created!")

# ── College ──────────────────────────────────────────────────────────────────
cursor.execute("""INSERT INTO colleges
  (name,location,established,affiliation,type,phone,email,website,address,
   naac_grade,aicte_approved,total_students,total_faculty,campus_area_acres)
  VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", (
    'St Lourdes Engineering College',
    'Anagaputhur, Chennai, Tamil Nadu',
    2005, 'Anna University', 'Private Engineering College',
    '+91-44-12345678', 'admissions@stlourdes.edu', 'www.stlourdes.edu',
    'Anagaputhur, Chennai - 600069, Tamil Nadu, India',
    'A', 1, 2500, 120, 15.5))

# ── Departments ──────────────────────────────────────────────────────────────
cursor.executemany("INSERT INTO departments (name,code,hod,phone,email) VALUES (?,?,?,?,?)", [
    ("Computer Science Engineering","CSE","Dr. S. Ramesh","+91-44-12345679","cse@stlourdes.edu"),
    ("Information Technology","IT","Dr. P. Kavitha","+91-44-12345680","it@stlourdes.edu"),
    ("Artificial Intelligence and Data Science","AIDS","Dr. R. Priya","+91-44-12345681","aids@stlourdes.edu"),
    ("Cyber Security","CYBER","Dr. K. Suresh","+91-44-12345682","cyber@stlourdes.edu"),
    ("Mechanical Engineering","MECH","Dr. M. Vijay","+91-44-12345683","mech@stlourdes.edu"),
])

# ── Programs ─────────────────────────────────────────────────────────────────
cursor.executemany("""INSERT INTO programs
  (college_id,name,short_name,department,degree_type,duration,seats,
   fees_per_year,total_fees,description,eligibility,highlights)
  VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""", [
    (1,"B.E Computer Science Engineering","CSE","CSE","UG",4,180,60000,240000,
     "4-year program covering algorithms, AI, ML, cloud, web development and software engineering.",
     "12th with Physics, Chemistry, Mathematics. Minimum 50% aggregate. TNEA counseling.",
     "90% placement | AI/ML labs | Top recruiters"),
    (1,"B.Tech Information Technology","B.Tech IT","IT","UG",4,120,60000,240000,
     "Focuses on networking, databases, web technologies, cybersecurity and enterprise software.",
     "12th with PCM. Minimum 50% aggregate. TNEA counseling.",
     "85% placement | Cloud computing focus | Industry projects"),
    (1,"B.E Artificial Intelligence and Data Science","AIDS","AIDS","UG",4,120,60000,240000,
     "Combines AI, data analytics, machine learning, deep learning and big data technologies.",
     "12th with PCM. Minimum 50% aggregate. TNEA counseling.",
     "80% placement | GPU servers | Data science projects"),
    (1,"B.E Cyber Security","CYBER","CYBER","UG",4,120,60000,240000,
     "Covers ethical hacking, network security, cryptography, digital forensics and security ops.",
     "12th with PCM. Minimum 50% aggregate. TNEA counseling.",
     "75% placement | Cyber lab | CEH prep"),
    (1,"B.E Mechanical Engineering","MECH","MECH","UG",4,120,60000,240000,
     "Covers thermodynamics, manufacturing, CAD/CAM, automation and robotics.",
     "12th with PCM. Minimum 45% aggregate. TNEA counseling.",
     "70% placement | CNC workshop | Core companies"),
])

# ── Scholarships ─────────────────────────────────────────────────────────────
cursor.executemany("INSERT INTO scholarships (name,type,eligibility,amount,description) VALUES (?,?,?,?,?)", [
    ("Merit Scholarship","Merit","90%+ in 12th board exams",12000,"Tuition fee waiver of Rs.12,000 per year."),
    ("SC/ST Government Scholarship","Government","SC/ST category, income below Rs.2.5 LPA",60000,"Full tuition covered under Tamil Nadu govt scheme."),
    ("OBC Scholarship","Government","OBC category, income below Rs.1.5 LPA",30000,"Partial fee coverage under government OBC scheme."),
    ("First Graduate Scholarship","Institution","First in family to attend college",10000,"Rs.10,000 per year for first-generation students."),
    ("Sports Scholarship","Sports","State/National level sports certificate required",15000,"Rs.15,000 per year for sports achievers."),
])

# ── Facilities ───────────────────────────────────────────────────────────────
cursor.executemany("""INSERT INTO facilities (college_id,name,category,description,capacity,fees,available)
  VALUES (?,?,?,?,?,?,?)""", [
    (1,"Central Library","Library","15,000+ books, e-journals, NPTEL access, reading rooms, Wi-Fi",500,0,1),
    (1,"Computer Lab","Laboratory","200+ systems, 24/7 internet, licensed software",200,0,1),
    (1,"AI & Data Science Lab","Laboratory","GPU servers, Python/R, Jupyter, TensorFlow, PyTorch",60,0,1),
    (1,"Cyber Security Lab","Laboratory","Kali Linux, Wireshark, ethical hacking tools",40,0,1),
    (1,"Mechanical Workshop","Laboratory","CNC machines, lathes, AutoCAD, 3D printer",80,0,1),
    (1,"Boys Hostel","Hostel","AC/non-AC rooms, 24/7 security, Wi-Fi, mess with 3 meals/day",400,48000,1),
    (1,"Girls Hostel","Hostel","AC/non-AC rooms, 24/7 security, Wi-Fi, mess with 3 meals/day",300,48000,1),
    (1,"College Canteen","Canteen","Multi-cuisine cafeteria, affordable pricing",300,0,1),
    (1,"Sports Complex","Sports","Cricket, football, basketball, volleyball, indoor games",1000,0,1),
    (1,"Medical Centre","Health","On-campus clinic, nurse 24/7, doctor 9am-5pm",20,0,1),
    (1,"Transport","Transport","Bus service covering 25+ routes across Chennai",1000,15000,1),
    (1,"Seminar Hall","Academic","500-seat air-conditioned hall with AV equipment",500,0,1),
    (1,"Wi-Fi Campus","Technology","High-speed 1 Gbps Wi-Fi across all buildings",2500,0,1),
    (1,"Placement Cell","Career","Dedicated placement office, interview rooms, mock drives",100,0,1),
])

# ── Placements ───────────────────────────────────────────────────────────────
cursor.executemany("""INSERT INTO placements
  (college_id,year,department,total_students,placed_students,
   placement_percentage,avg_package,highest_package,top_recruiters)
  VALUES (?,?,?,?,?,?,?,?,?)""", [
    (1,2024,"CSE",180,162,90.0,480000,1400000,"TCS, Infosys, Wipro, Cognizant, Zoho, Amazon, HCL"),
    (1,2024,"IT",120,102,85.0,440000,1000000,"TCS, Infosys, Tech Mahindra, Capgemini, Accenture"),
    (1,2024,"AIDS",120,96,80.0,520000,1800000,"Amazon, Flipkart, Mu Sigma, Tiger Analytics, Accenture"),
    (1,2024,"CYBER",120,90,75.0,500000,1200000,"IBM, Deloitte, KPMG, Wipro Cyber, EY"),
    (1,2024,"MECH",120,84,70.0,380000,900000,"Ashok Leyland, TVS, L&T, Hyundai, Bosch"),
])

# ── Subjects ─────────────────────────────────────────────────────────────────
cursor.executemany("INSERT INTO subjects (department,year,semester,subject_name) VALUES (?,?,?,?)", [
    ("CSE",1,1,"Engineering Mathematics I"),("CSE",1,1,"Engineering Physics"),
    ("CSE",1,2,"Programming in C"),("CSE",1,2,"Data Structures"),
    ("CSE",2,3,"Object Oriented Programming"),("CSE",2,3,"Database Management"),
    ("CSE",2,4,"Operating Systems"),("CSE",2,4,"Computer Networks"),
    ("CSE",3,5,"Machine Learning"),("CSE",3,5,"Cloud Computing"),
    ("CSE",3,6,"Artificial Intelligence"),("CSE",3,6,"Cyber Security"),
    ("CSE",4,7,"Deep Learning"),("CSE",4,8,"Project Work"),
])

# ── FAQs ─────────────────────────────────────────────────────────────────────
cursor.executemany("INSERT INTO faqs (category,question,answer) VALUES (?,?,?)", [
    ("admission","When does admission start?","Admissions begin in May each year after TNEA rank list release."),
    ("fees","Are there hidden fees?","No hidden fees. You pay tuition, exam fee, and optional hostel/transport."),
    ("fees","Can fees be paid in installments?","Yes. Annual fee split into two per semester."),
    ("hostel","Is hostel compulsory?","No, hostel is optional. Day scholars are welcome."),
])

# ── INTENTS ──────────────────────────────────────────────────────────────────
intents_data = [
    ("greeting","greeting","User greets"),
    ("college_overview","college","General college info"),
    ("admission_process","admission","How to get admission"),
    ("eligibility","admission","Eligibility criteria"),
    ("important_dates","admission","Key dates"),
    ("management_quota","admission","Direct/management admission"),
    ("fees_general","fees","General fee queries"),
    ("fees_breakdown","fees","Detailed fee breakdown"),
    ("scholarships","fees","Scholarship info"),
    ("fees_installment","fees","Payment options"),
    ("programs_overview","programs","All programs"),
    ("program_cse","programs","CSE details"),
    ("program_it","programs","IT details"),
    ("program_aids","programs","AI&DS details"),
    ("program_cyber","programs","Cyber Security details"),
    ("program_mech","programs","Mechanical details"),
    ("placements_overview","placements","Placement info"),
    ("placements_companies","placements","Recruiting companies"),
    ("placements_package","placements","Salary packages"),
    ("hostel","facilities","Hostel info"),
    ("transport","facilities","Bus/transport"),
    ("facilities_overview","facilities","All facilities"),
    ("library","facilities","Library details"),
    ("labs","facilities","Lab info"),
    ("sports","facilities","Sports facilities"),
    ("faculty","college","Faculty info"),
    ("contact","contact","Contact details"),
    ("naac_accreditation","college","NAAC grade"),
    ("affiliation","college","University affiliation"),
    ("campus","college","Campus and location"),
    ("thanks","","Thanks"),
    ("goodbye","","Bye"),
]
cursor.executemany("INSERT INTO intents (tag,context,description) VALUES (?,?,?)", intents_data)

def iid(tag):
    cursor.execute("SELECT id FROM intents WHERE tag=?", (tag,))
    return cursor.fetchone()[0]

# ── PATTERNS ─────────────────────────────────────────────────────────────────
patterns = {
    "greeting":             ["hi","hello","hey","good morning","good afternoon","good evening","hai","howdy","greetings"],
    "college_overview":     ["tell me about this college","about college","college information","about st lourdes","college details","college profile","overview"],
    "admission_process":    ["how do i apply","admission process","how to get admission","how can i join","application procedure","admission steps","how to apply","joining process","how to enroll","admission guidance"],
    "eligibility":          ["eligibility","am i eligible","who can apply","eligibility criteria","minimum marks","cutoff marks","required marks","12th percentage","qualifying marks","what is the minimum percentage","pcm required","can i apply","marks required"],
    "important_dates":      ["when to apply","application date","admission deadline","last date","when does admission start","admission dates","important dates","tnea date","counseling date","when does college start","application deadline"],
    "management_quota":     ["management quota","direct admission","without tnea","management seat","direct seat","nri quota","spot admission","direct join","paid seat"],
    "fees_general":         ["what are the fees","fees","fee structure","how much is the fee","tuition fee","yearly fee","annual fee","college fee","cost of studying","how much does it cost","total fee","fees details"],
    "fees_breakdown":       ["detailed fee","fee breakdown","complete fee structure","all fees","fee list","what fees are charged","total cost","full fee details"],
    "scholarships":         ["scholarship","fee waiver","merit scholarship","government scholarship","sc st scholarship","obc scholarship","free seat","financial aid","can i get scholarship","scholarship amount"],
    "fees_installment":     ["installment","emi","pay in parts","fee installment","partial payment","can i pay fees in two parts","fee payment options","how to pay fees"],
    "programs_overview":    ["what courses","programs offered","list of courses","engineering branches","available programs","all courses","what can i study","which departments","courses available","branch list"],
    "program_cse":          ["cse","computer science","be cse","b.e computer science","cse course details","about cse","computer science engineering","cse branch","cse subjects","cse seats","cse fees"],
    "program_it":           ["it course","information technology","btech it","it branch","about it course","it department","information technology details","it seats","it fees","it subjects"],
    "program_aids":         ["ai and data science","aids","artificial intelligence","data science course","aids branch","ai course","ml course","machine learning branch","data science details","aids fees"],
    "program_cyber":        ["cyber security","cybersecurity","cyber course","ethical hacking course","security branch","cyber security details","cyber fees","cyber seats"],
    "program_mech":         ["mechanical","mech","mechanical engineering","be mech","mech course","mechanical details","mech fees","mech seats"],
    "placements_overview":  ["placements","placement record","job after college","placement statistics","how are placements","campus placement","how many get placed","placement percentage","placement rate","jobs"],
    "placements_companies": ["which companies","top recruiters","companies visiting","who comes for placement","placement companies","mnc companies","it companies recruiting","list of companies","which mnc"],
    "placements_package":   ["salary","package","lpa","ctc","average package","highest package","how much salary","what package","placement package","salary offered","average ctc"],
    "hostel":               ["hostel","do you have hostel","accommodation","boys hostel","girls hostel","hostel facility","hostel fees","hostel cost","room and board","stay on campus","hostel available"],
    "transport":            ["transport","bus","college bus","transportation","how to reach college","bus routes","bus service","commute","bus facility","bus fee"],
    "facilities_overview":  ["facilities","infrastructure","what facilities","college infrastructure","campus facilities","amenities","what does college provide"],
    "library":              ["library","books","e library","reading room","digital library","library facility","how many books","nptel","library hours"],
    "labs":                 ["labs","laboratory","computer lab","which labs","lab facility","lab equipment","ai lab","cyber lab"],
    "sports":               ["sports","sports facility","cricket ground","football","basketball","gymnasium","gym","sports complex","extra curricular"],
    "faculty":              ["faculty","teachers","professors","teaching staff","how many faculty","faculty qualification","phd faculty","experienced teachers","faculty members"],
    "contact":              ["contact","phone number","email id","college address","how to contact","helpline","admission office","contact details","call college","office number","reach college","college email"],
    "naac_accreditation":   ["naac","accreditation","naac grade","naac rating","grade","approved","aicte approved","recognized","accredited college"],
    "affiliation":          ["affiliation","affiliated to","anna university","university","which university","affiliated university"],
    "campus":               ["campus","where is college","college location","address","area","campus area","college size","how big is campus","located where"],
    "thanks":               ["thanks","thank you","thank u","thx","thanks a lot","very helpful","great help","helpful","appreciate it"],
    "goodbye":              ["bye","goodbye","see you","cya","take care","see ya","quit","exit","done"],
}

for tag, plist in patterns.items():
    intent_id = iid(tag)
    cursor.executemany("INSERT INTO intent_patterns (intent_id,pattern) VALUES (?,?)",
                       [(intent_id, p) for p in plist])

# ── RESPONSES ────────────────────────────────────────────────────────────────
responses = {
    "greeting": [
        "Hello! Welcome to St Lourdes Engineering College Admission Assistant!\n\nI can help you with:\n- Admission process and eligibility\n- Fee structure and scholarships\n- Courses and programs\n- Hostel and facilities\n- Placement records\n\nWhat would you like to know?",
        "Hi there! Welcome to St Lourdes Engineering College!\n\nI am your Admission Assistant. Ask me anything about admissions, fees, courses, or facilities!",
    ],
    "college_overview": [
        "St Lourdes Engineering College\n\nLocation: Anagaputhur, Chennai, Tamil Nadu\nEstablished: 2005\nAffiliation: Anna University\nNAAC Grade: A | AICTE Approved\n\nStudents: 2,500+ | Faculty: 120+\nCampus: 15.5 acres\n\nWe offer 5 UG engineering programs with strong industry connections and excellent placement support.",
    ],
    "admission_process": [
        "Admission Process at St Lourdes Engineering College:\n\nStep 1: Pass Class 12 with Physics, Chemistry, Mathematics\nStep 2: Register for TNEA at tneaonline.org\nStep 3: TNEA rank is calculated based on 12th marks (no entrance exam)\nStep 4: Attend counseling as per your rank\nStep 5: Choose our college and your preferred department\nStep 6: Pay fees and submit documents\n\nManagement Quota seats are also available directly.\n\nContact us:\nPhone: +91-44-12345678\nEmail: admissions@stlourdes.edu\nOffice Hours: Monday to Saturday, 9 AM to 5 PM",
    ],
    "eligibility": [
        "Eligibility Criteria:\n\nGeneral / OBC Category:\n- Pass 12th with Physics, Chemistry, Mathematics\n- Minimum 50% aggregate in PCM\n\nSC / ST Category:\n- Minimum 45% aggregate in PCM\n\nMechanical Engineering:\n- Minimum 45% aggregate in PCM\n\nAge Limit:\n- Born on or after July 1, 2003 (for 2024 admission)\n\nAdmission is through TNEA rank based on 12th marks. No separate entrance exam required for Tamil Nadu students.",
    ],
    "important_dates": [
        "Important Admission Dates (2024-25):\n\n- TNEA Registration Opens: May 2024\n- TNEA Rank List Published: June 2024\n- Counseling Rounds: July to August 2024\n- Management Quota Admissions: June to August 2024\n- Classes Begin: August 2024\n\nDates may vary. Always check tneaonline.org or contact us at +91-44-12345678",
    ],
    "management_quota": [
        "Management Quota Admissions:\n\nSeats are available directly through the college without TNEA rank.\n\nWho can apply:\n- Students with 50%+ in 12th PCM\n- Any state board or CBSE/ICSE students\n- NRI candidates\n\nProcess:\n1. Visit admissions office or call us\n2. Submit application form\n3. Documents verification\n4. Seat allotment and fee payment\n\nPhone: +91-44-12345678\nEmail: admissions@stlourdes.edu\nOffice Hours: Monday to Saturday, 9 AM to 5 PM",
    ],
    "fees_general": [
        "Fee Structure (2024-25):\n\nAnnual Tuition Fee: Rs. 60,000 per year\nTotal for 4 Years: Rs. 2,40,000\n\nAdditional Fees:\n- University Exam Fee: Rs. 1,000 per semester\n- Hostel Fee: Rs. 48,000 per year (optional)\n- Transport Fee: Rs. 15,000 per year (optional)\n- Caution Deposit: Rs. 5,000 (refundable at end of course)\n\nScholarships are available for eligible students!\nType 'scholarship' to know more.",
    ],
    "fees_breakdown": [
        "Complete Fee Breakdown (per year):\n\nTuition Fee          : Rs. 60,000\nUniversity Exam Fee  : Rs. 2,000 (Rs.1000 per semester)\nLibrary Fee          : Rs. 500\nLab Fee              : Rs. 1,500\nCaution Deposit      : Rs. 5,000 (paid once, refundable)\n\nOptional:\nHostel               : Rs. 48,000 per year (includes 3 meals/day)\nTransport            : Rs. 15,000 per year\n\nFees can be paid in 2 installments - one per semester.",
    ],
    "scholarships": [
        "Scholarships Available at St Lourdes:\n\n1. Merit Scholarship\n   For students scoring 90%+ in 12th\n   Benefit: Rs. 12,000 per year fee waiver\n\n2. SC/ST Government Scholarship\n   Full tuition covered by Tamil Nadu Government\n   Requirement: Family income below Rs. 2.5 LPA\n\n3. OBC Scholarship\n   Partial fee coverage by Government\n   Requirement: Family income below Rs. 1.5 LPA\n\n4. First Graduate Scholarship\n   For first person in family to attend college\n   Benefit: Rs. 10,000 per year\n\n5. Sports Scholarship\n   For state or national level athletes\n   Benefit: Rs. 15,000 per year\n\nApply at the admissions office with relevant documents.\nPhone: +91-44-12345678",
    ],
    "fees_installment": [
        "Fee Payment Options:\n\nFees can be paid in 2 installments per year:\n- 1st Installment: At the time of admission (beginning of odd semester)\n- 2nd Installment: Beginning of even semester (January)\n\nPayment Methods Accepted:\n- Online Bank Transfer (NEFT/IMPS)\n- Demand Draft in favour of St Lourdes Engineering College\n- Online payment portal: pay.stlourdes.edu\n\nFor education loans, students can apply directly to their bank. We provide supporting documents.",
    ],
    "programs_overview": [
        "Programs Offered - UG (4 Year B.E / B.Tech):\n\n1. B.E Computer Science Engineering (CSE)   - 180 seats\n2. B.Tech Information Technology (IT)        - 120 seats\n3. B.E Artificial Intelligence & DS (AIDS)   - 120 seats\n4. B.E Cyber Security                        - 120 seats\n5. B.E Mechanical Engineering (MECH)         - 120 seats\n\nFee: Rs. 60,000 per year for all programs\nAffiliation: Anna University\n\nType any course name (CSE, IT, AIDS, Cyber, MECH) for full details!",
    ],
    "program_cse": [
        "B.E Computer Science Engineering (CSE)\n\nDuration: 4 Years | Seats: 180 | Fee: Rs. 60,000 per year\n\nWhat you will learn:\n- Data Structures and Algorithms\n- Object Oriented Programming\n- Database Management Systems\n- Computer Networks\n- Machine Learning and AI\n- Cloud Computing and DevOps\n- Software Engineering\n- Web and Mobile Development\n\nEligibility: 12th PCM with minimum 50%\nPlacement: 90% placed (Avg: Rs. 4.8 LPA, Highest: Rs. 14 LPA)\nTop Recruiters: TCS, Infosys, Wipro, Amazon, Zoho, Cognizant",
    ],
    "program_it": [
        "B.Tech Information Technology (IT)\n\nDuration: 4 Years | Seats: 120 | Fee: Rs. 60,000 per year\n\nWhat you will learn:\n- Networking and Security\n- Database Systems\n- Web Technologies\n- Cloud and DevOps\n- Enterprise Software\n- Cybersecurity Fundamentals\n\nEligibility: 12th PCM with minimum 50%\nPlacement: 85% placed (Avg: Rs. 4.4 LPA, Highest: Rs. 10 LPA)\nTop Recruiters: TCS, Infosys, Tech Mahindra, Capgemini, Accenture",
    ],
    "program_aids": [
        "B.E Artificial Intelligence and Data Science (AIDS)\n\nDuration: 4 Years | Seats: 120 | Fee: Rs. 60,000 per year\n\nWhat you will learn:\n- Python and R Programming\n- Machine Learning\n- Deep Learning and Neural Networks\n- Big Data (Hadoop, Spark)\n- Data Visualization\n- Natural Language Processing\n- Computer Vision\n\nEligibility: 12th PCM with minimum 50%\nPlacement: 80% placed (Avg: Rs. 5.2 LPA, Highest: Rs. 18 LPA)\nTop Recruiters: Amazon, Flipkart, Mu Sigma, Tiger Analytics, Accenture",
    ],
    "program_cyber": [
        "B.E Cyber Security\n\nDuration: 4 Years | Seats: 120 | Fee: Rs. 60,000 per year\n\nWhat you will learn:\n- Network Security\n- Ethical Hacking\n- Cryptography\n- Digital Forensics\n- Security Operations\n- Penetration Testing\n- Risk Management\n\nEligibility: 12th PCM with minimum 50%\nPlacement: 75% placed (Avg: Rs. 5 LPA, Highest: Rs. 12 LPA)\nTop Recruiters: IBM, Deloitte, KPMG, Wipro Cyber, EY",
    ],
    "program_mech": [
        "B.E Mechanical Engineering (MECH)\n\nDuration: 4 Years | Seats: 120 | Fee: Rs. 60,000 per year\n\nWhat you will learn:\n- Engineering Mechanics\n- Thermodynamics\n- Manufacturing Processes\n- CAD/CAM (AutoCAD, SolidWorks)\n- Robotics and Automation\n- Heat Transfer\n- Fluid Mechanics\n\nEligibility: 12th PCM with minimum 45%\nPlacement: 70% placed (Avg: Rs. 3.8 LPA, Highest: Rs. 9 LPA)\nTop Recruiters: Ashok Leyland, TVS, L&T, Hyundai, Bosch",
    ],
    "placements_overview": [
        "Placement Record 2024:\n\nOverall Placement Rate: 82%\n\nCSE  : 90% placed | Avg Rs. 4.8 LPA | Highest Rs. 14 LPA\nIT   : 85% placed | Avg Rs. 4.4 LPA | Highest Rs. 10 LPA\nAIDS : 80% placed | Avg Rs. 5.2 LPA | Highest Rs. 18 LPA\nCYBER: 75% placed | Avg Rs. 5.0 LPA | Highest Rs. 12 LPA\nMECH : 70% placed | Avg Rs. 3.8 LPA | Highest Rs. 9 LPA\n\nWe have a dedicated placement cell with pre-placement training, mock interviews, and resume workshops.",
    ],
    "placements_companies": [
        "Top Recruiting Companies:\n\nIT and Software:\nTCS, Infosys, Wipro, Cognizant, HCL, Capgemini, Tech Mahindra, Accenture, Zoho, Freshworks\n\nProduct and Tech:\nAmazon, Flipkart, IBM\n\nAnalytics and Data:\nMu Sigma, Tiger Analytics, Fractal Analytics\n\nCybersecurity:\nDeloitte, KPMG, EY, Wipro Cyber\n\nCore Engineering:\nAshok Leyland, TVS, L&T, Hyundai, Bosch\n\n400+ students placed every year!",
    ],
    "placements_package": [
        "Salary Packages (2024 Batch):\n\nAI and Data Science : Avg Rs. 5.2 LPA | Highest Rs. 18 LPA\nCyber Security      : Avg Rs. 5.0 LPA | Highest Rs. 12 LPA\nCSE                 : Avg Rs. 4.8 LPA | Highest Rs. 14 LPA\nIT                  : Avg Rs. 4.4 LPA | Highest Rs. 10 LPA\nMechanical          : Avg Rs. 3.8 LPA | Highest Rs. 9 LPA\n\nPackage has grown 15% year-on-year.\nBest offer in 2024: Rs. 18 LPA (AI&DS student).",
    ],
    "hostel": [
        "Hostel Facilities:\n\nBoys Hostel: 400 seats\nGirls Hostel: 300 seats\n\nWhat is included in Rs. 48,000 per year:\n- Furnished room (2 to 3 sharing)\n- 3 meals per day (breakfast, lunch, dinner)\n- 24/7 security and CCTV\n- High-speed Wi-Fi\n- Hot water facility\n- Common room with TV\n- Study rooms\n- Laundry facility nearby\n\nAC rooms available at extra charge.\nHostel is optional. Day scholars are welcome.\n\nHostel Office: +91-44-12345685",
    ],
    "transport": [
        "Transport Facilities:\n\n- 25+ bus routes covering Chennai and suburbs\n- Areas covered: Tambaram, Chromepet, Pallavaram, Vandalur, Porur, Guindy, Perungalathur and more\n- Annual fee: Rs. 15,000 per year\n- AC and Non-AC buses available\n- Morning pickup: 7:30 AM\n- Evening drop: 6:00 PM\n\nTransport is optional. Students can commute independently.\n\nTransport Office: +91-44-12345686",
    ],
    "facilities_overview": [
        "Campus Facilities at St Lourdes:\n\nAcademic:\n- Central Library (15,000+ books, NPTEL access)\n- Modern Labs (CSE, IT, AI, Cyber, Mechanical)\n\nLiving:\n- Boys Hostel (400 seats) and Girls Hostel (300 seats)\n- College Canteen with multi-cuisine food\n\nSports:\n- Cricket, Football, Basketball, Volleyball\n- Indoor games and Gymnasium\n\nHealth and Safety:\n- On-campus medical clinic\n- 24/7 CCTV security\n\nConnectivity:\n- 1 Gbps Wi-Fi campus-wide\n- 25+ bus routes\n\nCareer:\n- Placement Cell with interview rooms and training",
    ],
    "library": [
        "Central Library:\n\n- 15,000+ books (technical and non-technical)\n- E-journals and digital resources\n- NPTEL video lecture access\n- Separate reading rooms\n- High-speed Wi-Fi inside\n- Online catalogue system\n\nLibrary Timings:\nMonday to Saturday: 8 AM to 8 PM\nSunday: 10 AM to 5 PM",
    ],
    "labs": [
        "Laboratory Facilities:\n\nCSE/IT Labs: 200+ systems with licensed software\nAI and Data Science Lab: GPU servers, TensorFlow, PyTorch, Jupyter\nCyber Security Lab: Kali Linux, Wireshark, penetration testing tools\nNetworking Lab: Cisco routers, switches, packet tracer\nMechanical Workshop: CNC machines, AutoCAD, 3D printer\nElectronics Lab: Microprocessors, embedded systems\n\nAll labs open from 9 AM to 6 PM. Extended hours during project season.",
    ],
    "sports": [
        "Sports and Extra-Curricular Activities:\n\nOutdoor Sports:\n- Cricket ground (full-size)\n- Football field\n- Basketball court\n- Volleyball court\n\nIndoor Activities:\n- Table Tennis, Chess, Carrom\n- Gymnasium (separate for boys and girls)\n\nEvents:\n- Annual Sports Meet\n- Inter-college tournaments\n\nSports scholarship available for state or national level athletes!",
    ],
    "faculty": [
        "Faculty at St Lourdes Engineering College:\n\n- 120+ faculty members\n- 40%+ are PhD holders\n- Many faculty have 5 to 15 years of industry experience\n- Visiting professors from IIT and Anna University\n- Faculty to student ratio: 1:20\n\nEach department has a dedicated HOD and experienced teaching staff.\nFor specific faculty details, contact the department directly.",
    ],
    "contact": [
        "Contact St Lourdes Engineering College:\n\nAdmissions Office:\nPhone: +91-44-12345678\nEmail: admissions@stlourdes.edu\nOffice Hours: Monday to Saturday, 9 AM to 5 PM\n\nWebsite: www.stlourdes.edu\n\nAddress:\nSt Lourdes Engineering College\nAnagaputhur, Chennai - 600069\nTamil Nadu, India\n\nHow to Reach:\n- By Train: Anagaputhur or Chrompet station (2 km away)\n- By Bus: Routes 47, 47A, 47B stop nearby",
    ],
    "naac_accreditation": [
        "Accreditation and Recognition:\n\n- NAAC Grade: A\n- AICTE Approved: Yes\n- Affiliated to Anna University, Chennai\n- ISO Certified: Yes\n\nAll degrees are recognized by UGC and the Government of India.",
    ],
    "affiliation": [
        "University Affiliation:\n\nSt Lourdes Engineering College is affiliated to:\n\nAnna University, Chennai\n- One of India's premier technical universities\n- Ranked among top 10 universities in India (NIRF)\n- Degrees are recognized nationally and internationally\n\nAll examinations, mark sheets and degrees are issued by Anna University.",
    ],
    "campus": [
        "Campus Information:\n\nLocation: Anagaputhur, Chennai - 600069, Tamil Nadu\nCampus Area: 15.5 acres\nBuildings: 5 academic blocks plus hostels and sports complex\n\nCampus Features:\n- Green and pollution-free environment\n- 1 Gbps Wi-Fi throughout campus\n- 24/7 CCTV security\n- Separate zones for academics, sports, and residence\n\nNearest Station: Anagaputhur or Chrompet (2 km away)",
    ],
    "thanks": [
        "You are welcome! Feel free to ask anything else about admissions, fees, or courses!",
        "Happy to help! If you have more questions about St Lourdes, I am here!",
        "Glad I could help! Best wishes for your admission journey!",
    ],
    "goodbye": [
        "Goodbye! Best of luck with your admission! Feel free to come back anytime.",
        "See you! Wishing you the very best for your engineering journey at St Lourdes!",
    ],
}

for tag, rlist in responses.items():
    intent_id = iid(tag)
    cursor.executemany("INSERT INTO intent_responses (intent_id,response) VALUES (?,?)",
                       [(intent_id, r) for r in rlist])

cursor.executemany("""INSERT INTO study_materials
  (material_id,subject,topic,file_name,file_path,description,department,semester,file_size,tags)
  VALUES (?,?,?,?,?,?,?,?,?,?)""", [
    ("mat_001","Computer Networks","OSI Model","CN_OSI.pdf","materials/cn/osi.pdf","OSI notes","CSE",3,2458624,"networking"),
    ("mat_002","Data Structures","Trees","DS_Trees.pdf","materials/ds/trees.pdf","Tree algorithms","CSE",3,3145728,"trees"),
])

conn.commit()

print("\nDatabase created successfully!")
for table in ["programs","intents","intent_patterns","intent_responses","facilities","scholarships","placements"]:
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    print(f"  {table}: {cursor.fetchone()[0]} rows")

conn.close()
print("\ncollege_chatbot.db is ready!")