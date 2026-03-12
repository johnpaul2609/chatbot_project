"""
academic_classifier.py
=======================
Handles all Academic Support queries:
- Syllabus (by department + semester)
- Notes / study materials
- Timetable (by department + year)
- Exam schedule / internal marks calendar
- Faculty info per department
- General academic queries
"""

import random

# ── Keyword → intent map ──────────────────────────────────────────────────────
ACADEMIC_KEYWORDS = {
    "syllabus_cse":     ["cse syllabus","computer science syllabus","cse subjects","subjects in cse","cse curriculum","cse sem","cse semester subjects"],
    "syllabus_it":      ["it syllabus","information technology syllabus","it subjects","subjects in it","it curriculum","it semester"],
    "syllabus_aids":    ["aids syllabus","ai syllabus","data science syllabus","aids subjects","ai ds syllabus","artificial intelligence syllabus"],
    "syllabus_cyber":   ["cyber syllabus","cyber security syllabus","cyber subjects","security syllabus"],
    "syllabus_mech":    ["mech syllabus","mechanical syllabus","mech subjects","mechanical subjects","mech curriculum"],
    "syllabus_general": ["syllabus","curriculum","subject list","what subjects","which subjects","anna university syllabus","regulation"],

    "notes_general":    ["notes","study material","study materials","lecture notes","pdf notes","download notes","get notes","unit notes","chapter notes","i need","send me","give me notes","share notes"],
    "notes_cse":        ["cse notes","computer science notes","cse study material","cse pdf"],
    "notes_it":         ["it notes","information technology notes","it study material"],
    "notes_aids":       ["ai notes","aids notes","data science notes","ml notes","machine learning notes"],
    "notes_cyber":      ["cyber notes","cyber security notes","security notes"],
    "notes_mech":       ["mech notes","mechanical notes","mechanical study material"],

    "timetable_general":["timetable","time table","class schedule","class timing","lecture schedule","when is class","which period","daily schedule"],
    "timetable_cse":    ["cse timetable","cse time table","cse class schedule","cse schedule"],
    "timetable_it":     ["it timetable","it time table","it class schedule"],
    "timetable_aids":   ["aids timetable","ai timetable","data science timetable"],
    "timetable_cyber":  ["cyber timetable","cyber security timetable"],
    "timetable_mech":   ["mech timetable","mechanical timetable"],

    "exam_schedule":    ["exam schedule","exam timetable","exam date","when is exam","upcoming exam","exam calendar","end semester exam","ese date","theory exam"],
    "internal_exam":    ["internal exam","internal assessment","cat exam","cat 1","cat 2","internal marks","model exam","internal test","unit test"],
    "exam_results":     ["result","results","marks","grade","cgpa","gpa","how to check result","anna university result","exam result"],
    "exam_pattern":     ["exam pattern","question paper pattern","marks distribution","how many marks","how many questions","passing marks","minimum marks to pass"],

    "faculty_general":  ["faculty","professor","teacher","staff","hod","head of department","who teaches","subject teacher","lecturer"],
    "faculty_cse":      ["cse faculty","cse professor","cse teacher","who teaches cse","cse hod","cse staff"],
    "faculty_it":       ["it faculty","it professor","it teacher","it hod"],
    "faculty_aids":     ["aids faculty","ai faculty","data science faculty","aids professor"],
    "faculty_cyber":    ["cyber faculty","cyber security faculty","cyber professor"],
    "faculty_mech":     ["mech faculty","mechanical faculty","mechanical professor"],

    "academic_calendar":["academic calendar","college calendar","holiday list","holidays","semester start","semester end","when does semester start","academic year"],
    "attendance":       ["attendance","attendance percentage","minimum attendance","attendance requirement","proxy","how much attendance","attendance shortage"],
    "library_academic": ["library","borrow book","library timing","issue book","library card","how to use library","digital library"],
    "lab_sessions":     ["lab","practical","lab session","lab timing","which lab","how to access lab","lab work"],
    "project":          ["project","final year project","mini project","project guide","project submission","how to choose project","ieee project"],
    "internship":       ["internship","internship opportunity","how to get internship","internship company","summer internship","internship certificate"],

    # Download / PDF requests — catch all natural phrases
    "download_ds":   ["data structure notes","data structures notes","ds notes","ds pdf","data structure pdf",
                      "i need data structure","i need ds","send ds notes","download ds","get ds notes",
                      "datastructure notes","give me ds","share ds notes","data structure material",
                      "need data structure","want ds notes","ds study material"],
    "download_cn":   ["computer network notes","computer networks notes","cn notes","cn pdf","network notes pdf",
                      "i need cn","i need computer network","send cn notes","download cn","get cn notes",
                      "give me cn","share cn notes","computer network material","network study material",
                      "need cn notes","want cn notes"],
    "download_dbms": ["dbms notes","database notes","database management notes","dbms pdf","database pdf",
                      "i need dbms","i need database","send dbms notes","download dbms","get dbms notes",
                      "give me dbms","share dbms notes","db notes","database study material",
                      "need dbms notes","want dbms notes","dbms material"],
    "download_os":   ["operating system notes","os notes","os pdf","operating system pdf",
                      "i need os","i need operating system","send os notes","download os","get os notes",
                      "give me os","share os notes","os study material","need os notes","want os notes",
                      "operating systems notes","os material"],
    "download_ml":   ["machine learning notes","ml notes","ml pdf","machine learning pdf",
                      "i need ml","i need machine learning","send ml notes","download ml","get ml notes",
                      "give me ml","share ml notes","ml study material","need ml notes","want ml notes",
                      "machine learning material","ai notes","deep learning notes"],
    "download_math": ["engineering mathematics notes","engineering maths notes","maths notes","math notes",
                      "em notes","em pdf","maths pdf","math pdf","engineering mathematics pdf",
                      "i need maths","i need math","send maths notes","download math","get maths notes",
                      "give me maths","share maths","need maths notes","want maths notes",
                      "engineering math material","em study material"],

    "academic_greeting":["hi","hello","hey","good morning","good afternoon","help","academic support","what can you do","what can you help"],
}

ACADEMIC_SUGGESTIONS = {
    "syllabus_general":  ["CSE Syllabus?", "IT Syllabus?", "AI&DS Syllabus?", "Exam schedule?"],
    "syllabus_cse":      ["CSE Notes?", "CSE Timetable?", "Exam schedule?", "Faculty info?"],
    "syllabus_it":       ["IT Notes?", "IT Timetable?", "Exam schedule?"],
    "syllabus_aids":     ["AI&DS Notes?", "AI&DS Timetable?", "Exam schedule?"],
    "syllabus_cyber":    ["Cyber Notes?", "Cyber Timetable?", "Exam schedule?"],
    "syllabus_mech":     ["Mech Notes?", "Mech Timetable?", "Exam schedule?"],
    "notes_general":     ["CSE Notes?", "IT Notes?", "AI&DS Notes?", "Mech Notes?"],
    "notes_cse":         ["CSE Syllabus?", "CSE Timetable?", "Exam schedule?"],
    "notes_it":          ["IT Syllabus?", "IT Timetable?", "Exam schedule?"],
    "notes_aids":        ["AI&DS Syllabus?", "AI&DS Timetable?", "Exam schedule?"],
    "notes_cyber":       ["Cyber Syllabus?", "Cyber Timetable?", "Exam schedule?"],
    "notes_mech":        ["Mech Syllabus?", "Mech Timetable?", "Exam schedule?"],
    "timetable_general": ["CSE Timetable?", "IT Timetable?", "Exam schedule?", "Academic calendar?"],
    "timetable_cse":     ["CSE Syllabus?", "CSE Notes?", "Exam schedule?"],
    "timetable_it":      ["IT Syllabus?", "IT Notes?", "Exam schedule?"],
    "timetable_aids":    ["AI&DS Syllabus?", "AI&DS Notes?", "Exam schedule?"],
    "timetable_cyber":   ["Cyber Syllabus?", "Cyber Notes?", "Exam schedule?"],
    "timetable_mech":    ["Mech Syllabus?", "Mech Notes?", "Exam schedule?"],
    "exam_schedule":     ["Internal exam dates?", "Exam pattern?", "How to check results?", "Attendance rules?"],
    "internal_exam":     ["End semester exam?", "Exam pattern?", "Attendance rules?"],
    "exam_results":      ["Exam schedule?", "CGPA calculation?", "Attendance rules?"],
    "exam_pattern":      ["Exam schedule?", "Internal exam?", "Passing marks?"],
    "faculty_general":   ["CSE Faculty?", "IT Faculty?", "Mech Faculty?", "Contact faculty?"],
    "faculty_cse":       ["CSE Syllabus?", "CSE Timetable?", "HOD contact?"],
    "faculty_it":        ["IT Syllabus?", "IT Timetable?", "HOD contact?"],
    "faculty_aids":      ["AI&DS Syllabus?", "AI&DS Timetable?", "HOD contact?"],
    "faculty_cyber":     ["Cyber Syllabus?", "Cyber Timetable?", "HOD contact?"],
    "faculty_mech":      ["Mech Syllabus?", "Mech Timetable?", "HOD contact?"],
    "academic_calendar": ["Exam schedule?", "Holiday list?", "Semester dates?"],
    "attendance":        ["Exam schedule?", "Academic calendar?", "Faculty contact?"],
    "library_academic":  ["Lab sessions?", "Notes?", "Academic calendar?"],
    "lab_sessions":      ["Library?", "Timetable?", "Notes?"],
    "project":           ["Internship?", "Faculty guide?", "Academic calendar?"],
    "internship":        ["Project?", "Faculty contact?", "Academic calendar?"],
    "academic_greeting": ["Syllabus?", "Notes?", "Timetable?", "Exam schedule?"],
}

ACADEMIC_RESPONSES = {
    "academic_greeting": [
        "Hello! Welcome to St Lourdes Academic Support Assistant!\n\nI can help you with:\n- Syllabus (all departments)\n- Study notes and materials\n- Class timetable\n- Exam schedule and dates\n- Faculty information\n- Attendance rules\n- Library and lab info\n- Projects and internships\n\nWhat would you like to know? Try: 'CSE syllabus' or 'exam schedule'",
    ],

    # ── SYLLABUS ─────────────────────────────────────────────────────────────
    "syllabus_general": [
        "Syllabus - St Lourdes Engineering College\nRegulation: Anna University (R2021)\n\nSelect your department for detailed syllabus:\n- CSE (Computer Science Engineering)\n- IT (Information Technology)\n- AIDS (Artificial Intelligence & Data Science)\n- CYBER (Cyber Security)\n- MECH (Mechanical Engineering)\n\nType: 'CSE syllabus' or 'IT syllabus' for semester-wise details.\n\nFull syllabus PDF: www.stlourdes.edu/academics/syllabus",
    ],
    "syllabus_cse": [
        "CSE Syllabus - Anna University R2021\n\nSemester 1:\n- Engineering Mathematics I\n- Engineering Physics\n- Engineering Chemistry\n- Problem Solving & Python Programming\n- Basic Electrical Engineering\n\nSemester 2:\n- Engineering Mathematics II\n- Data Structures\n- Digital Principles & System Design\n- Object Oriented Programming (Java)\n- Web Technologies\n\nSemester 3:\n- Discrete Mathematics\n- Computer Organization\n- Database Management Systems\n- Operating Systems\n- Design & Analysis of Algorithms\n\nSemester 4:\n- Theory of Computation\n- Computer Networks\n- Software Engineering\n- Microprocessors & Interfacing\n- Professional Elective I\n\nSemester 5:\n- Compiler Design\n- Machine Learning\n- Cloud Computing\n- Internet of Things\n- Professional Elective II\n\nSemester 6:\n- Artificial Intelligence\n- Mobile Application Development\n- Cyber Security\n- Big Data Analytics\n- Open Elective I\n\nSemester 7 & 8:\n- Deep Learning\n- Blockchain Technology\n- Project Work (2 semesters)\n- Professional Electives III & IV\n\nFull PDF: www.stlourdes.edu/academics/cse-syllabus",
    ],
    "syllabus_it": [
        "IT Syllabus - Anna University R2021\n\nSemester 1 & 2 (Common with all departments):\n- Engineering Mathematics I & II\n- Physics, Chemistry\n- Problem Solving & Python\n- Web Technologies\n\nSemester 3:\n- Data Structures\n- Object Oriented Programming\n- Database Systems\n- Digital Principles\n\nSemester 4:\n- Computer Networks\n- Operating Systems\n- Software Engineering\n- Linux Administration\n\nSemester 5:\n- Cloud Computing\n- Network Security\n- Mobile Computing\n- Data Warehousing\n\nSemester 6:\n- Cyber Security\n- IoT and Embedded Systems\n- Big Data\n- AI Fundamentals\n\nSemester 7 & 8:\n- Advanced Networking\n- Project Work\n- Professional Electives\n\nFull PDF: www.stlourdes.edu/academics/it-syllabus",
    ],
    "syllabus_aids": [
        "AI & Data Science Syllabus - R2021\n\nSemester 1 & 2 (Common):\n- Engineering Mathematics I & II\n- Physics, Chemistry\n- Problem Solving & Python\n\nSemester 3:\n- Statistics & Probability\n- Data Structures\n- Database Management\n- Programming in R\n\nSemester 4:\n- Machine Learning\n- Data Visualization\n- Business Intelligence\n- Linear Algebra\n\nSemester 5:\n- Deep Learning\n- Natural Language Processing\n- Big Data Analytics (Spark, Hadoop)\n- Computer Vision\n\nSemester 6:\n- Reinforcement Learning\n- AI Ethics & Governance\n- Time Series Analysis\n- Cloud AI Platforms\n\nSemester 7 & 8:\n- Advanced Deep Learning\n- Capstone Project\n- Professional Electives\n\nFull PDF: www.stlourdes.edu/academics/aids-syllabus",
    ],
    "syllabus_cyber": [
        "Cyber Security Syllabus - R2021\n\nSemester 1 & 2 (Common):\n- Engineering Mathematics I & II\n- Physics, Chemistry, Python\n\nSemester 3:\n- Data Structures\n- Computer Networks\n- Operating Systems\n- Programming Fundamentals\n\nSemester 4:\n- Network Security\n- Cryptography & Steganography\n- Linux & Shell Scripting\n- Database Security\n\nSemester 5:\n- Ethical Hacking\n- Penetration Testing\n- Cyber Laws & Forensics\n- Malware Analysis\n\nSemester 6:\n- Security Operations (SOC)\n- Intrusion Detection Systems\n- Cloud Security\n- Risk Management & Compliance\n\nSemester 7 & 8:\n- Advanced Ethical Hacking\n- Incident Response\n- Project Work\n\nFull PDF: www.stlourdes.edu/academics/cyber-syllabus",
    ],
    "syllabus_mech": [
        "Mechanical Engineering Syllabus - R2021\n\nSemester 1 & 2 (Common):\n- Engineering Mathematics I & II\n- Physics, Chemistry\n- Engineering Graphics\n- Workshop Practice\n\nSemester 3:\n- Engineering Thermodynamics\n- Fluid Mechanics\n- Manufacturing Technology\n- Strength of Materials\n\nSemester 4:\n- Heat & Mass Transfer\n- Kinematics of Machinery\n- Manufacturing Processes\n- Metrology & Measurements\n\nSemester 5:\n- Design of Machine Elements\n- Dynamics of Machinery\n- CAD/CAM\n- Industrial Engineering\n\nSemester 6:\n- Finite Element Analysis\n- Mechatronics\n- Robotics\n- Quality Engineering\n\nSemester 7 & 8:\n- Automation\n- Project Work\n- Professional Electives\n\nFull PDF: www.stlourdes.edu/academics/mech-syllabus",
    ],

    # ── NOTES ────────────────────────────────────────────────────────────────
    "notes_general": [
        "Study Notes & Materials - St Lourdes\n\nAvailable resources:\n\n1. Department Google Drive Links:\n   - CSE Notes: drive.stlourdes.edu/cse-notes\n   - IT Notes: drive.stlourdes.edu/it-notes\n   - AIDS Notes: drive.stlourdes.edu/aids-notes\n   - Cyber Notes: drive.stlourdes.edu/cyber-notes\n   - Mech Notes: drive.stlourdes.edu/mech-notes\n\n2. NPTEL Courses: nptel.ac.in (Free online lectures)\n\n3. College LMS (Learning Portal): lms.stlourdes.edu\n   Login with your college ID and password\n\n4. Library: Physical notes and reference books available\n   Timing: Mon-Sat 8 AM - 8 PM\n\nType department name for specific notes (e.g. 'CSE notes')",
    ],
    "notes_cse": [
        "CSE Study Notes & Materials:\n\nOnline Portal: lms.stlourdes.edu\n(Login with college ID)\n\nPopular Downloads:\n- Data Structures & Algorithms notes\n- DBMS complete notes with SQL\n- Computer Networks (unit-wise)\n- Operating Systems notes\n- Machine Learning notes (Python)\n- Cloud Computing notes\n- Object Oriented Programming (Java)\n\nDepartment Drive: drive.stlourdes.edu/cse-notes\nFaculty Contact: cse@stlourdes.edu\n\nTip: NPTEL (nptel.ac.in) has free video courses for all these subjects!",
    ],
    "notes_it": [
        "IT Study Notes & Materials:\n\nOnline Portal: lms.stlourdes.edu\n(Login with college ID)\n\nPopular Downloads:\n- Computer Networks complete notes\n- Network Security notes\n- Cloud Computing & AWS notes\n- Web Technologies (HTML, CSS, JS)\n- Mobile Computing notes\n- Linux Administration notes\n\nDepartment Drive: drive.stlourdes.edu/it-notes\nFaculty Contact: it@stlourdes.edu",
    ],
    "notes_aids": [
        "AI & Data Science Study Notes:\n\nOnline Portal: lms.stlourdes.edu\n(Login with college ID)\n\nPopular Downloads:\n- Machine Learning notes (sklearn, Python)\n- Deep Learning notes (TensorFlow, PyTorch)\n- NLP notes and tutorials\n- Data Visualization (Matplotlib, Seaborn)\n- Big Data notes (Hadoop, Spark)\n- Computer Vision notes (OpenCV)\n- Statistics & Probability notes\n\nDepartment Drive: drive.stlourdes.edu/aids-notes\nFaculty Contact: aids@stlourdes.edu\n\nTip: Kaggle.com has excellent free datasets and notebooks for practice!",
    ],
    "notes_cyber": [
        "Cyber Security Study Notes:\n\nOnline Portal: lms.stlourdes.edu\n(Login with college ID)\n\nPopular Downloads:\n- Ethical Hacking notes (CEH prep)\n- Cryptography notes\n- Network Security notes\n- Kali Linux command reference\n- Cyber Laws & Digital Forensics notes\n- Penetration Testing guide\n\nDepartment Drive: drive.stlourdes.edu/cyber-notes\nFaculty Contact: cyber@stlourdes.edu\n\nTip: TryHackMe and HackTheBox are great free platforms to practice!",
    ],
    "notes_mech": [
        "Mechanical Engineering Study Notes:\n\nOnline Portal: lms.stlourdes.edu\n(Login with college ID)\n\nPopular Downloads:\n- Thermodynamics notes with problems\n- Fluid Mechanics notes\n- Strength of Materials notes\n- CAD/CAM notes (AutoCAD guide)\n- Machine Design notes\n- Manufacturing Processes notes\n\nDepartment Drive: drive.stlourdes.edu/mech-notes\nFaculty Contact: mech@stlourdes.edu",
    ],

    # ── TIMETABLE ────────────────────────────────────────────────────────────
    "timetable_general": [
        "Class Timetable - St Lourdes Engineering College\n\nGeneral Schedule:\nMonday to Friday: 8:45 AM - 4:30 PM\nSaturday: 8:45 AM - 1:00 PM\n\nPeriod Timings:\n1st Period : 8:45 AM - 9:40 AM\n2nd Period : 9:40 AM - 10:35 AM\nBreak      : 10:35 AM - 10:45 AM\n3rd Period : 10:45 AM - 11:40 AM\n4th Period : 11:40 AM - 12:35 PM\nLunch      : 12:35 PM - 1:15 PM\n5th Period : 1:15 PM - 2:10 PM\n6th Period : 2:10 PM - 3:05 PM\n7th Period : 3:05 PM - 4:00 PM\n\nDepartment-specific timetables are shared by your class coordinator at the start of each semester.\n\nLMS Portal: lms.stlourdes.edu\nType 'CSE timetable' for department-specific info.",
    ],
    "timetable_cse": [
        "CSE Class Timetable:\n\nGeneral Timing: 8:45 AM - 4:30 PM (Mon-Fri)\nSaturday: 8:45 AM - 1:00 PM\n\nSample Weekly Schedule (3rd Semester CSE):\n\nMonday    : DBMS | OOP | Design of Algorithms | Lab (OOP)\nTuesday   : Computer Networks | OS | Discrete Maths | Lab (DBMS)\nWednesday : DBMS | OOP | Design of Algorithms | Library Hour\nThursday  : OS | Computer Networks | Discrete Maths | Lab (Networks)\nFriday    : All Subjects Rotation + Seminar\nSaturday  : Revision | Tutorials | Club Activities\n\nActual timetable for your semester is shared by:\n- Your class coordinator on Day 1 of semester\n- LMS Portal: lms.stlourdes.edu\n- WhatsApp class group\n\nCSE Office: +91-44-12345679",
    ],
    "timetable_it": [
        "IT Class Timetable:\n\nGeneral Timing: 8:45 AM - 4:30 PM (Mon-Fri)\nSaturday: 8:45 AM - 1:00 PM\n\nSample Weekly Schedule (4th Semester IT):\n\nMonday    : Computer Networks | OS | Linux Admin | Lab (Networks)\nTuesday   : Software Engineering | Networks | OS | Lab (Linux)\nWednesday : All theory subjects rotation\nThursday  : Lab sessions (2 periods)\nFriday    : Seminars | Tutorials | Revision\nSaturday  : Club activities | Sports\n\nActual timetable shared by class coordinator at semester start.\nLMS Portal: lms.stlourdes.edu\nIT Office: +91-44-12345680",
    ],
    "timetable_aids": [
        "AI & Data Science Timetable:\n\nGeneral Timing: 8:45 AM - 4:30 PM (Mon-Fri)\n\nSample Weekly Schedule (5th Semester AIDS):\n\nMonday    : Deep Learning | NLP | Big Data | Python Lab\nTuesday   : Computer Vision | DL | NLP | Big Data Lab\nWednesday : Deep Learning | NLP | Data Viz | Research Reading\nThursday  : Computer Vision | Big Data | AI Ethics | Lab\nFriday    : Guest Lecture | Seminar | Project Discussion\nSaturday  : Mini-project work | Tutorials\n\nLMS Portal: lms.stlourdes.edu\nAIDS Office: +91-44-12345681",
    ],
    "timetable_cyber": [
        "Cyber Security Timetable:\n\nGeneral Timing: 8:45 AM - 4:30 PM (Mon-Fri)\n\nSample Weekly Schedule (5th Semester Cyber):\n\nMonday    : Ethical Hacking | Crypto | Cyber Laws | Kali Lab\nTuesday   : Penetration Testing | Network Security | Malware | Lab\nWednesday : Ethical Hacking | Cyber Laws | Forensics | Theory\nThursday  : Pen Testing | Network Security | Lab sessions\nFriday    : CTF Practice | Seminars | Revision\nSaturday  : Cyber club activities | Competitions\n\nLMS Portal: lms.stlourdes.edu\nCyber Office: +91-44-12345682",
    ],
    "timetable_mech": [
        "Mechanical Engineering Timetable:\n\nGeneral Timing: 8:45 AM - 4:30 PM (Mon-Fri)\n\nSample Weekly Schedule (4th Semester MECH):\n\nMonday    : Heat Transfer | Kinematics | Manufacturing | Drawing Lab\nTuesday   : Thermodynamics | Fluid Mech | Kinematics | Workshop\nWednesday : Heat Transfer | Manufacturing | Metrology | Lab\nThursday  : All theory + Workshop Lab\nFriday    : Seminar | Guest Lecture | Revision\nSaturday  : CAD Lab | Project Work | Sports\n\nLMS Portal: lms.stlourdes.edu\nMech Office: +91-44-12345683",
    ],

    # ── EXAM SCHEDULE ────────────────────────────────────────────────────────
    "exam_schedule": [
        "Exam Schedule - 2024-25:\n\nEND SEMESTER EXAMINATIONS (ESE):\nOdd Semester (Nov/Dec 2024):\n- Practical Exams      : 11 Nov - 20 Nov 2024\n- Theory Exams         : 25 Nov - 14 Dec 2024\n\nEven Semester (Apr/May 2025):\n- Practical Exams      : 14 Apr - 25 Apr 2025\n- Theory Exams         : 28 Apr - 17 May 2025\n\nResults: Usually declared 45-60 days after exam.\n\nDetailed timetable published by Anna University:\n- Website: annauniv.edu\n- College notice board\n- LMS Portal: lms.stlourdes.edu\n\nFor revaluation / arrears: Apply through college exam cell.\nExam Cell Contact: exam@stlourdes.edu | +91-44-12345690",
    ],
    "internal_exam": [
        "Internal Assessments - 2024-25:\n\nCAT (Continuous Assessment Tests):\n\nOdd Semester (Jul - Nov 2024):\n- CAT 1 : 2nd week of August 2024\n- CAT 2 : 1st week of October 2024\n- Model Exam : 2nd week of November 2024\n\nEven Semester (Jan - May 2025):\n- CAT 1 : 2nd week of February 2025\n- CAT 2 : 1st week of April 2025\n- Model Exam : 2nd week of April 2025\n\nInternal Marks Weightage:\n- CAT 1 + CAT 2 : 40 marks (20 each)\n- Assignments    : 10 marks\n- Attendance     : 5 marks\n- Total Internal : 100 marks (scaled to 20)\n\nInternal marks portal: marks.stlourdes.edu\nFor queries: academic@stlourdes.edu",
    ],
    "exam_results": [
        "How to Check Exam Results:\n\n1. Anna University Official Site:\n   coe1.annauniv.edu or aucoe.annauniv.edu\n   Enter your Register Number and Date of Birth\n\n2. College Portal:\n   results.stlourdes.edu\n   Login with college ID\n\n3. SMS Service:\n   Send 'RESULT <Register No>' to 56263\n\nResults published:\n- Usually 45-60 days after last exam\n- Check Anna University website for exact date\n\nFor Revaluation / Photocopy:\n- Apply within 15 days of result\n- Fee: Rs. 750 per subject (revaluation)\n- Contact: exam@stlourdes.edu",
    ],
    "exam_pattern": [
        "Exam Pattern - Anna University R2021:\n\nEND SEMESTER EXAM (100 marks -> scaled to 80):\n\nPart A : 10 x 2 marks = 20 marks (Short answers, all compulsory)\nPart B : 5 x 13 marks = 65 marks (Either/Or type, 5 questions)\nPart C : 1 x 15 marks = 15 marks (Open book / case study - optional)\n\nTotal: 100 marks (External)\n\nPassing Criteria:\n- Minimum 50% overall (Internal + External combined)\n- Minimum 30 marks in external exam (out of 80)\n- Internal: 20 marks | External: 80 marks\n\nFor Lab Exams:\n- Record: 20 marks\n- Viva: 20 marks\n- Experiment: 60 marks\n- Total: 100 marks\n\nNote: Pattern may vary by subject. Always check with your faculty.",
    ],

    # ── FACULTY ──────────────────────────────────────────────────────────────
    "faculty_general": [
        "Faculty Information - St Lourdes Engineering College:\n\nTotal Faculty: 120+\n40%+ are PhD holders\n\nDepartment HODs:\n- CSE  : Dr. S. Ramesh    | +91-44-12345679 | cse@stlourdes.edu\n- IT   : Dr. P. Kavitha   | +91-44-12345680 | it@stlourdes.edu\n- AIDS : Dr. R. Priya     | +91-44-12345681 | aids@stlourdes.edu\n- CYBER: Dr. K. Suresh    | +91-44-12345682 | cyber@stlourdes.edu\n- MECH : Dr. M. Vijay     | +91-44-12345683 | mech@stlourdes.edu\n\nFor subject-specific faculty, contact your class coordinator or HOD.\n\nType 'CSE faculty' for department-specific info.",
    ],
    "faculty_cse": [
        "CSE Department Faculty:\n\nHOD: Dr. S. Ramesh (PhD - IIT Madras)\nSpecialization: Machine Learning, Data Mining\n\nSenior Faculty:\n- Dr. A. Pradeep     | AI & Neural Networks\n- Prof. B. Meena     | Data Structures, Algorithms\n- Dr. C. Rajan       | Computer Networks\n- Prof. D. Lakshmi   | DBMS, Software Engineering\n- Dr. E. Kumar       | Cloud Computing, DevOps\n- Prof. F. Divya     | Web Technologies, Full Stack\n\nFaculty-Student Ratio: 1:20\nContact: cse@stlourdes.edu | +91-44-12345679\nOffice Hours: Mon-Fri 9 AM - 5 PM",
    ],
    "faculty_it": [
        "IT Department Faculty:\n\nHOD: Dr. P. Kavitha (PhD - Anna University)\nSpecialization: Network Security, Cloud Computing\n\nSenior Faculty:\n- Dr. G. Senthil      | Networking, Cyber Security\n- Prof. H. Anitha     | Web Technologies, Mobile App\n- Dr. I. Rajesh       | Database, Data Warehousing\n- Prof. J. Priya      | Linux, Cloud Platforms\n\nContact: it@stlourdes.edu | +91-44-12345680",
    ],
    "faculty_aids": [
        "AI & Data Science Faculty:\n\nHOD: Dr. R. Priya (PhD - IIT Bombay)\nSpecialization: Deep Learning, NLP\n\nSenior Faculty:\n- Dr. K. Arjun        | Machine Learning, Python\n- Prof. L. Nithya     | Data Visualization, R\n- Dr. M. Balamurugan  | Computer Vision, OpenCV\n- Prof. N. Swetha     | Big Data, Spark/Hadoop\n\nContact: aids@stlourdes.edu | +91-44-12345681",
    ],
    "faculty_cyber": [
        "Cyber Security Faculty:\n\nHOD: Dr. K. Suresh (PhD - BITS Pilani)\nSpecialization: Ethical Hacking, Network Security\n\nSenior Faculty:\n- Dr. O. Venkat       | Penetration Testing\n- Prof. P. Sindhu     | Cryptography, Forensics\n- Dr. Q. Karthik      | SOC, Incident Response\n- Prof. R. Gayathri   | Cyber Laws, Compliance\n\nContact: cyber@stlourdes.edu | +91-44-12345682",
    ],
    "faculty_mech": [
        "Mechanical Engineering Faculty:\n\nHOD: Dr. M. Vijay (PhD - NIT Trichy)\nSpecialization: CAD/CAM, Robotics\n\nSenior Faculty:\n- Dr. S. Murugan       | Thermodynamics, Heat Transfer\n- Prof. T. Kavya       | Manufacturing, Metrology\n- Dr. U. Dinesh        | Fluid Mechanics\n- Prof. V. Ramya       | Machine Design, FEA\n\nContact: mech@stlourdes.edu | +91-44-12345683",
    ],

    # ── OTHER ACADEMIC ───────────────────────────────────────────────────────
    "academic_calendar": [
        "Academic Calendar 2024-25:\n\nODD SEMESTER (July - November 2024):\n- College Reopens    : 15 July 2024\n- CAT 1              : 2nd week of August\n- CAT 2              : 1st week of October\n- Last Working Day   : 15 November 2024\n- Practical Exams    : 11 - 20 November\n- End Semester Exams : 25 Nov - 14 Dec 2024\n\nEVEN SEMESTER (January - May 2025):\n- College Reopens    : 6 January 2025\n- CAT 1              : 2nd week of February\n- CAT 2              : 1st week of April\n- Last Working Day   : 20 April 2025\n- Practical Exams    : 14 - 25 April\n- End Semester Exams : 28 Apr - 17 May 2025\n\nHolidays: As per Anna University and Tamil Nadu Govt.\n\nDetailed calendar: lms.stlourdes.edu | academic@stlourdes.edu",
    ],
    "attendance": [
        "Attendance Policy - St Lourdes Engineering College:\n\nMinimum Required Attendance: 75%\n(This is an Anna University mandatory requirement)\n\nCondonation:\n- 65% to 74%: Medical or valid reason condonation possible\n- Below 65%: Detained from exams (not eligible to appear)\n\nHow Attendance is Calculated:\n- Total classes held vs Total classes attended\n- Separate for theory and practical subjects\n\nInternal Marks for Attendance:\n- 95%+ : 5 marks\n- 90-94%: 4 marks\n- 85-89%: 3 marks\n- 80-84%: 2 marks\n- 75-79%: 1 mark\n- Below 75%: 0 marks\n\nCheck your attendance: attendance.stlourdes.edu\nContact: academic@stlourdes.edu if any discrepancy",
    ],
    "library_academic": [
        "Library - Academic Resources:\n\nLibrary Timings:\n- Monday to Saturday: 8 AM - 8 PM\n- Sunday: 10 AM - 5 PM\n\nHow to Borrow Books:\n1. Get your Library Card from the librarian (1st year)\n2. Present card + student ID\n3. Maximum 3 books at a time\n4. Return period: 14 days (renewable once)\n\nAvailable Resources:\n- 15,000+ technical books\n- IEEE digital library access\n- NPTEL online courses\n- Elsevier & Springer e-journals\n- Previous year question papers\n\nLibrary Portal: library.stlourdes.edu\nLibrarian: library@stlourdes.edu | +91-44-12345691",
    ],
    "lab_sessions": [
        "Lab Sessions - St Lourdes Engineering College:\n\nLab Timings: 9:00 AM - 5:00 PM (Mon-Fri)\n\nLab Allocation (Department-wise):\n- CSE/IT: Computer Lab 1-4 (200 systems)\n- AIDS: AI Lab (GPU servers, Python environment)\n- Cyber: Cyber Security Lab (Kali, Wireshark)\n- MECH: Mechanical Workshop + CAD Lab\n\nHow to Access Labs:\n1. Lab sessions are part of your timetable (2 periods each)\n2. Free lab access (after hours): Get permission from HOD\n3. For project work: Book via lab coordinator\n\nLab Rules:\n- No food/drinks inside labs\n- Log in with college ID\n- Save work on personal drive or USB\n\nLab Coordinator: lab@stlourdes.edu",
    ],
    "project": [
        "Project Guidelines - St Lourdes Engineering College:\n\nFinal Year Project (7th & 8th Semester):\n\nProcess:\n1. Choose guide (faculty) from your department\n2. Submit project proposal (Week 2 of 7th sem)\n3. Phase 1 Review: End of 7th semester\n4. Phase 2 Review: Mid of 8th semester\n5. Final Viva + Demonstration: End of 8th semester\n\nTips for Good Projects:\n- Choose from IEEE recent papers (2022-2024)\n- Use trending tech: AI/ML, IoT, Blockchain, Cloud\n- Register on GitHub for version control\n\nMini Project (5th/6th Semester):\n- Small team (2-3 students)\n- Submit report + demo\n\nProject Portal: project.stlourdes.edu\nFor guidance: academic@stlourdes.edu",
    ],
    "internship": [
        "Internship Opportunities - St Lourdes Engineering College:\n\nTypes of Internships:\n1. Summer Internship (after 2nd year): 30-45 days\n2. In-Plant Training (after 3rd year): 30 days\n3. Placement Internship (7th semester): Some companies offer PPO\n\nHow to Find Internships:\n1. College Placement Cell: placement@stlourdes.edu\n2. Company portals: TCS iON, Infosys Springboard, AMCAT\n3. Platforms: Internshala, LinkedIn, Indeed\n4. NPTEL Internships: nptel.ac.in/internships\n\nCertification:\n- Submit offer letter + completion certificate to dept.\n- It is counted as value-added course (internal marks)\n\nFor opportunities: placement@stlourdes.edu | +91-44-12345692\nPlacement Cell: Mon-Fri 10 AM - 4 PM",
    ],
}

# ── Department signals ───────────────────────────────────────────────────────
DEPT_SIGNALS = {
    "cse":   ["cse","computer science","cs ","c.s.e"],
    "aids":  ["aids","ai and data","data science","ai ds","artificial intelligence","a.i"],
    "cyber": ["cyber","cybersecurity","cyber security","ethical hacking"],
    "mech":  ["mech","mechanical","m.e ","be mech"],
}

# ── Topic signals ─────────────────────────────────────────────────────────────
TOPIC_SIGNALS = {
    "syllabus":  ["syllabus","subject","curriculum","semester","1st year","2nd year","3rd year","4th year",
                  "year syllabus","1 year","2 year","3 year","4 year","first year","second year","third year",
                  "fourth year","sem1","sem2","sem3","sem4","sem5","sem6","sem7","sem8","regulation","r2021"],
    "notes":     ["notes","study material","lecture notes","pdf","download notes","unit notes","chapter notes"],
    "timetable": ["timetable","time table","schedule","timing","period","class time","when is class","daily schedule"],
    "faculty":   ["faculty","professor","teacher","staff","hod","who teaches","lecturer","head of"],
}

import re as _re

def _detect_dept(text: str):
    """Detect department from text. IT handled carefully to avoid false matches."""
    # IT: must be a standalone word or clear phrase
    if _re.search(r"\bit\b", text) or "information technology" in text or "btech it" in text or "b.tech it" in text:
        return "it"
    for dept, signals in DEPT_SIGNALS.items():
        for sig in signals:
            if sig in text:
                return dept
    return None

def _detect_topic(text: str):
    """Detect topic category from text."""
    for topic, signals in TOPIC_SIGNALS.items():
        for sig in signals:
            if sig in text:
                return topic
    return None

# Subject → download intent mapping for smart detection
SUBJECT_DOWNLOAD_MAP = {
    "data structure": "download_ds",
    "datastructure":  "download_ds",
    "ds":             "download_ds",
    "computer network": "download_cn",
    "cn":             "download_cn",
    "networking":     "download_cn",
    "dbms":           "download_dbms",
    "database":       "download_dbms",
    "operating system": "download_os",
    "os":             "download_os",
    "machine learning": "download_ml",
    "ml":             "download_ml",
    "engineering math": "download_math",
    "engineering maths": "download_math",
    "maths":          "download_math",
    "em":             "download_math",
}

# Words that signal the user wants to receive/download something
WANT_WORDS = ["need","want","send","give","share","download","get","show","provide",
              "i need","i want","can i get","can you send","please send","please give"]


# ── Year detection for timetable requests ─────────────────────────────────────
YEAR_SIGNALS = {
    1: ["1st year","first year","year 1","year1","1 year","sem 1","sem 2","semester 1","semester 2","1st sem","2nd sem"],
    2: ["2nd year","second year","year 2","year2","2 year","sem 3","sem 4","semester 3","semester 4","3rd sem","4th sem"],
    3: ["3rd year","third year","year 3","year3","3 year","sem 5","sem 6","semester 5","semester 6","5th sem","6th sem"],
    4: ["4th year","fourth year","final year","year 4","year4","4 year","sem 7","sem 8","semester 7","semester 8","7th sem","8th sem"],
}

TIMETABLE_WORDS = ["timetable","time table","schedule","class schedule","class timing","period","daily schedule","weekly schedule"]

BACKEND_URL_TT = "http://127.0.0.1:8000"

def _detect_year(text: str) -> int:
    """Returns year number 1-4 if found in text, else None"""
    for year, signals in YEAR_SIGNALS.items():
        for sig in signals:
            if sig in text:
                return year
    return None

def get_timetable_image_url(dept: str, year: int) -> str:
    """Returns the image URL for the given dept + year"""
    return f"{BACKEND_URL_TT}/api/materials/timetable/{dept.lower()}/{year}"

def _wants_download(text: str) -> bool:
    """Returns True if the user is asking to receive/download something"""
    return any(w in text for w in WANT_WORDS)

def get_timetable_info(intent: str, text: str) -> dict:
    """Returns timetable image info if intent is a timetable request"""
    if not intent.startswith("timetable_"):
        return None
    dept_tag = intent.replace("timetable_", "").upper()
    if dept_tag in ("GENERAL", ""):
        return None
    year = _detect_year(text.lower())
    if not year:
        year = 1  # default to 1st year if not specified
    return {
        "dept": dept_tag,
        "year": year,
        "image_url": get_timetable_image_url(dept_tag, year),
        "label": f"{dept_tag} {['1st','2nd','3rd','4th'][year-1]} Year Timetable",
    }

def classify_academic(text: str):
    """
    Smart multi-pass classifier.
    Pass 0: timetable + dept + year detection (image response)
    Pass 1: detect subject + want-word → map to download intent
    Pass 2: exact keyword map
    Pass 3: dept + topic combination
    Pass 4: topic alone
    Pass 5: dept alone → syllabus default
    """
    text_lower = text.lower().strip()

    # Pass 0: timetable request detection
    if any(w in text_lower for w in TIMETABLE_WORDS):
        dept = _detect_dept(text_lower)
        if dept:
            return f"timetable_{dept}", 0.99
        return "timetable_general", 0.90

    # Pass 1: subject + want-word = download request
    # e.g. "i need data structure notes", "send me os notes", "give me ml pdf"
    if _wants_download(text_lower) or "notes" in text_lower or "pdf" in text_lower or "material" in text_lower:
        for subject_kw, dl_intent in SUBJECT_DOWNLOAD_MAP.items():
            if subject_kw in text_lower:
                return dl_intent, 0.99

    dept  = _detect_dept(text_lower)
    topic = _detect_topic(text_lower)

    # Pass 2: exact keyword map
    for intent_tag, keywords in ACADEMIC_KEYWORDS.items():
        for kw in keywords:
            if kw in text_lower:
                if intent_tag.endswith("_general") and dept:
                    topic_part = intent_tag.replace("_general", "")
                    specific = f"{topic_part}_{dept}"
                    if specific in ACADEMIC_RESPONSES:
                        return specific, 0.99
                return intent_tag, 0.99

    # Pass 3: dept + topic combination
    if dept and topic:
        intent = f"{topic}_{dept}"
        if intent in ACADEMIC_RESPONSES:
            return intent, 0.95

    # Pass 4: topic alone
    if topic:
        return f"{topic}_general", 0.80

    # Pass 5: dept alone → default to syllabus
    if dept:
        return f"syllabus_{dept}", 0.70

    return "academic_unknown", 0.0


# ── Material download info ────────────────────────────────────────────────────
MATERIAL_INFO = {
    "download_ds": {
        "material_id": "mat_ds_001",
        "subject": "Data Structures & Algorithms",
        "description": "Complete notes covering Arrays, Linked List, Stack, Queue, Trees, Graphs, Sorting & Searching.",
        "dept": "CSE / IT",
        "semester": "Semester 3",
        "pages": "~45 pages",
    },
    "download_cn": {
        "material_id": "mat_cn_001",
        "subject": "Computer Networks",
        "description": "OSI Model, TCP/IP, DNS, HTTP, Network Devices, Network Security.",
        "dept": "CSE / IT",
        "semester": "Semester 4",
        "pages": "~38 pages",
    },
    "download_dbms": {
        "material_id": "mat_db_001",
        "subject": "Database Management Systems (DBMS)",
        "description": "ER Model, SQL (DDL/DML/DCL), Normalization (1NF-BCNF), Transactions, Indexing.",
        "dept": "CSE / IT",
        "semester": "Semester 3",
        "pages": "~40 pages",
    },
    "download_os": {
        "material_id": "mat_os_001",
        "subject": "Operating Systems",
        "description": "Process Management, CPU Scheduling, Memory Management, Deadlock, File Systems.",
        "dept": "CSE / IT",
        "semester": "Semester 4",
        "pages": "~42 pages",
    },
    "download_ml": {
        "material_id": "mat_ml_001",
        "subject": "Machine Learning",
        "description": "Supervised/Unsupervised Learning, Neural Networks, Model Evaluation, scikit-learn.",
        "dept": "CSE / AIDS",
        "semester": "Semester 5",
        "pages": "~50 pages",
    },
    "download_math": {
        "material_id": "mat_ma_001",
        "subject": "Engineering Mathematics",
        "description": "Matrices, Differential & Integral Calculus, ODE, Laplace Transform, Statistics.",
        "dept": "All Departments",
        "semester": "Semester 1 & 2",
        "pages": "~55 pages",
    },
}

def get_material_download_info(intent: str) -> dict:
    """Returns material info dict if intent is a download intent, else None"""
    return MATERIAL_INFO.get(intent, None)

def get_academic_response(intent: str) -> str:
    if intent == "academic_unknown":
        return (
            "I'm not sure what you're looking for.\n\n"
            "I can help you with:\n"
            "- Syllabus (type: 'CSE syllabus' or 'IT syllabus')\n"
            "- Notes (type: 'CSE notes' or 'Mech notes')\n"
            "- Timetable (type: 'CSE timetable')\n"
            "- Exam schedule (type: 'exam schedule')\n"
            "- Internal exam dates (type: 'internal exam')\n"
            "- Faculty info (type: 'CSE faculty')\n"
            "- Attendance rules (type: 'attendance')\n"
            "- Library info (type: 'library')\n"
            "- Project guidance (type: 'project')\n"
            "- Internship info (type: 'internship')\n\n"
            "What would you like to know?"
        )
    responses = ACADEMIC_RESPONSES.get(intent, [])
    return random.choice(responses) if responses else get_academic_response("academic_unknown")

def get_academic_suggestions(intent: str) -> list:
    return ACADEMIC_SUGGESTIONS.get(intent, ["Syllabus?", "Notes?", "Timetable?", "Exam schedule?"])