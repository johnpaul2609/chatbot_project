"""
generate_timetables.py
======================
Run this ONCE from your Backend folder:
    python generate_timetables.py

It will create all 20 timetable images in:
    Backend/materials/timetables/
"""

import subprocess, sys

# Auto-install Pillow if missing
try:
    from PIL import Image
except ImportError:
    print("Installing Pillow...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
    print("Pillow installed!")

from PIL import Image, ImageDraw, ImageFont
import os

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "materials", "timetables")
os.makedirs(BASE, exist_ok=True)

# Colors
BG       = (245, 247, 252)
HEADER   = (30,  64, 175)   # blue-800
SUBHEAD  = (239, 246, 255)  # blue-50
ROW_ALT  = (248, 250, 255)
BORDER   = (191, 219, 254)  # blue-200
TXT_W    = (255, 255, 255)
TXT_DK   = (15,  23,  42)
TXT_GREY = (100, 116, 139)
BREAK_BG = (254, 243, 199)  # amber-100
BREAK_TX = (146,  64,  14)  # amber-800
LAB_BG   = (220, 252, 231)  # green-100
LAB_TX   = (21, 128,  61)   # green-700

# Period timing slots
PERIODS = [
    ("8:45–9:40",   "Period 1"),
    ("9:40–10:35",  "Period 2"),
    ("10:35–10:45", "BREAK"),
    ("10:45–11:40", "Period 3"),
    ("11:40–12:35", "Period 4"),
    ("12:35–1:15",  "LUNCH"),
    ("1:15–2:10",   "Period 5"),
    ("2:10–3:05",   "Period 6"),
    ("3:05–4:00",   "Period 7"),
]

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

# Department × Year → weekly schedule
# Format: day → [p1, p2, p3, p4, p5, p6, p7]  (BREAK & LUNCH auto-inserted)
SCHEDULES = {
    ("CSE", 1): {
        "Monday":    ["Eng. Maths-I",  "Eng. Physics",   "Eng. Chemistry", "Problem Solving", "Basic Electrical", "—",            "—"],
        "Tuesday":   ["Eng. Physics",  "Eng. Maths-I",   "Problem Solving","Eng. Chemistry",  "—",                "Lab (Physics)", "Lab (Physics)"],
        "Wednesday": ["Eng. Chemistry","Problem Solving", "Eng. Maths-I",   "Basic Electrical","Eng. Physics",     "—",            "—"],
        "Thursday":  ["Basic Electrical","Eng. Maths-I", "Eng. Chemistry", "Problem Solving", "—",                "Lab (Chem)",   "Lab (Chem)"],
        "Friday":    ["Problem Solving","Eng. Physics",  "Basic Electrical","Eng. Maths-I",   "Eng. Chemistry",   "Seminar",      "—"],
        "Saturday":  ["Revision",      "Tutorial",       "—",              "—",               "—",                "—",            "—"],
    },
    ("CSE", 2): {
        "Monday":    ["Data Structures","OOP (Java)",    "Web Technologies","Digital Principles","—",             "Lab (DS)",     "Lab (DS)"],
        "Tuesday":   ["OOP (Java)",    "Data Structures","Digital Principles","Eng. Maths-II", "Web Tech",        "—",            "—"],
        "Wednesday": ["Web Technologies","Eng. Maths-II","OOP (Java)",     "Data Structures", "—",               "Lab (OOP)",    "Lab (OOP)"],
        "Thursday":  ["Digital Principles","OOP (Java)", "Eng. Maths-II",  "Web Tech",        "Data Structures", "—",            "—"],
        "Friday":    ["Eng. Maths-II", "Data Structures","Digital Principles","OOP (Java)",   "Web Tech",        "Seminar",      "—"],
        "Saturday":  ["Tutorial",      "Lab (Web)",      "Lab (Web)",      "—",               "—",               "—",            "—"],
    },
    ("CSE", 3): {
        "Monday":    ["DBMS",          "OOP / Java",     "Design of Algo", "Computer Org",    "—",               "Lab (DBMS)",   "Lab (DBMS)"],
        "Tuesday":   ["Computer Nets", "OS",             "Discrete Maths", "Design of Algo",  "DBMS",            "—",            "—"],
        "Wednesday": ["OS",            "DBMS",           "Computer Nets",  "Discrete Maths",  "—",               "Lab (OS)",     "Lab (OS)"],
        "Thursday":  ["Discrete Maths","Design of Algo", "OS",             "Computer Nets",   "DBMS",            "—",            "—"],
        "Friday":    ["Computer Nets", "Discrete Maths", "DBMS",           "OS",              "Design of Algo",  "Seminar",      "—"],
        "Saturday":  ["Tutorial",      "Lab (Networks)", "Lab (Networks)", "—",               "—",               "—",            "—"],
    },
    ("CSE", 4): {
        "Monday":    ["Theory of Comp","Computer Nets",  "Software Engg",  "Microprocessors", "—",               "Lab (Micro)",  "Lab (Micro)"],
        "Tuesday":   ["Software Engg", "Theory of Comp", "Microprocessors","Computer Nets",   "Prof. Elective",  "—",            "—"],
        "Wednesday": ["Computer Nets", "Software Engg",  "Theory of Comp", "Prof. Elective",  "—",               "Lab (Networks)","Lab (Networks)"],
        "Thursday":  ["Microprocessors","Prof. Elective","Software Engg",  "Theory of Comp",  "Computer Nets",   "—",            "—"],
        "Friday":    ["Prof. Elective","Microprocessors","Computer Nets",  "Software Engg",   "Theory of Comp",  "Seminar",      "—"],
        "Saturday":  ["Tutorial",      "Mini Project",   "Mini Project",   "—",               "—",               "—",            "—"],
    },
    ("IT", 1): {
        "Monday":    ["Eng. Maths-I",  "Eng. Physics",   "Eng. Chemistry", "Problem Solving", "Basic Electrical","—",            "—"],
        "Tuesday":   ["Eng. Physics",  "Eng. Maths-I",   "Problem Solving","Eng. Chemistry",  "—",               "Lab (Physics)","Lab (Physics)"],
        "Wednesday": ["Eng. Chemistry","Problem Solving", "Eng. Maths-I",   "Basic Electrical","Eng. Physics",    "—",            "—"],
        "Thursday":  ["Basic Electrical","Eng. Maths-I", "Eng. Chemistry", "Problem Solving", "—",               "Lab (Chem)",   "Lab (Chem)"],
        "Friday":    ["Problem Solving","Eng. Physics",  "Basic Electrical","Eng. Maths-I",   "Eng. Chemistry",  "Seminar",      "—"],
        "Saturday":  ["Revision",      "Tutorial",       "—",              "—",               "—",               "—",            "—"],
    },
    ("IT", 2): {
        "Monday":    ["Data Structures","OOP (Java)",    "Web Technologies","Digital Principles","—",             "Lab (DS)",     "Lab (DS)"],
        "Tuesday":   ["OOP (Java)",    "Data Structures","Digital Principles","Eng. Maths-II", "Web Tech",        "—",            "—"],
        "Wednesday": ["Web Technologies","Eng. Maths-II","OOP (Java)",     "Data Structures", "—",               "Lab (OOP)",    "Lab (OOP)"],
        "Thursday":  ["Digital Principles","OOP (Java)", "Eng. Maths-II",  "Web Tech",        "Data Structures", "—",            "—"],
        "Friday":    ["Eng. Maths-II", "Data Structures","Digital Principles","OOP (Java)",   "Web Tech",        "Seminar",      "—"],
        "Saturday":  ["Tutorial",      "Lab (Web)",      "Lab (Web)",      "—",               "—",               "—",            "—"],
    },
    ("IT", 3): {
        "Monday":    ["Computer Nets", "OS",             "Linux Admin",    "Database Systems", "—",              "Lab (Networks)","Lab (Networks)"],
        "Tuesday":   ["Software Engg", "Computer Nets",  "OS",             "Linux Admin",      "Database Sys",   "—",            "—"],
        "Wednesday": ["Database Sys",  "Software Engg",  "Computer Nets",  "OS",               "—",              "Lab (DB)",     "Lab (DB)"],
        "Thursday":  ["OS",            "Database Sys",   "Software Engg",  "Computer Nets",    "Linux Admin",    "—",            "—"],
        "Friday":    ["Linux Admin",   "OS",             "Database Sys",   "Software Engg",    "Computer Nets",  "Seminar",      "—"],
        "Saturday":  ["Tutorial",      "Lab (Linux)",    "Lab (Linux)",    "—",                "—",              "—",            "—"],
    },
    ("IT", 4): {
        "Monday":    ["Cloud Computing","Network Sec",   "Mobile Computing","Data Warehousing","—",              "Lab (Cloud)",  "Lab (Cloud)"],
        "Tuesday":   ["Network Sec",   "Cloud Computing","Data Warehousing","Mobile Computing", "Prof. Elective", "—",           "—"],
        "Wednesday": ["Mobile Computing","Data Warehouse","Cloud Computing","Network Sec",      "—",              "Lab (Mobile)","Lab (Mobile)"],
        "Thursday":  ["Prof. Elective","Mobile Computing","Network Sec",   "Cloud Computing",  "Data Warehouse", "—",           "—"],
        "Friday":    ["Data Warehouse", "Network Sec",   "Prof. Elective", "Cloud Computing",  "Mobile Computing","Seminar",    "—"],
        "Saturday":  ["Tutorial",       "Mini Project",  "Mini Project",   "—",               "—",               "—",          "—"],
    },
    ("AIDS", 1): {
        "Monday":    ["Eng. Maths-I",  "Eng. Physics",   "Problem Solving","Eng. Chemistry",  "Basic Electrical","—",           "—"],
        "Tuesday":   ["Eng. Physics",  "Problem Solving","Eng. Maths-I",   "Eng. Chemistry",  "—",               "Lab (Physics)","Lab (Physics)"],
        "Wednesday": ["Eng. Chemistry","Eng. Maths-I",   "Basic Electrical","Problem Solving", "—",              "Lab (Chem)",   "Lab (Chem)"],
        "Thursday":  ["Problem Solving","Basic Electrical","Eng. Chemistry","Eng. Maths-I",   "Eng. Physics",    "—",            "—"],
        "Friday":    ["Basic Electrical","Eng. Chemistry","Eng. Physics",  "Problem Solving", "Eng. Maths-I",    "Seminar",      "—"],
        "Saturday":  ["Revision",      "Tutorial",       "—",              "—",               "—",               "—",            "—"],
    },
    ("AIDS", 2): {
        "Monday":    ["Prob & Statistics","Data Structures","Programming in R","Database Mgmt","—",             "Lab (DS)",     "Lab (DS)"],
        "Tuesday":   ["Data Structures","Prob & Statistics","Database Mgmt", "Programming R",  "Eng. Maths-II", "—",           "—"],
        "Wednesday": ["Programming R",  "Database Mgmt",  "Prob & Statistics","Data Structures","—",            "Lab (R)",      "Lab (R)"],
        "Thursday":  ["Database Mgmt",  "Eng. Maths-II",  "Data Structures","Prob & Statistics","Programming R","—",           "—"],
        "Friday":    ["Eng. Maths-II",  "Programming R",  "Data Structures","Database Mgmt",  "Prob & Statistics","Seminar",   "—"],
        "Saturday":  ["Tutorial",       "Lab (DB)",       "Lab (DB)",       "—",               "—",               "—",         "—"],
    },
    ("AIDS", 3): {
        "Monday":    ["Machine Learning","Data Visualization","Business Intel","Linear Algebra","—",            "Lab (ML)",     "Lab (ML)"],
        "Tuesday":   ["Data Visualization","Machine Learning","Linear Algebra","Business Intel","ML",           "—",            "—"],
        "Wednesday": ["Business Intel", "Linear Algebra", "Machine Learning","Data Viz",       "—",             "Lab (DataViz)","Lab (DataViz)"],
        "Thursday":  ["Linear Algebra", "Business Intel", "Data Viz",       "Machine Learning","Business Intel","—",           "—"],
        "Friday":    ["Machine Learning","Linear Algebra", "Business Intel", "Data Viz",       "ML",            "Seminar",      "—"],
        "Saturday":  ["Tutorial",       "Mini Project",   "Mini Project",   "—",               "—",              "—",          "—"],
    },
    ("AIDS", 4): {
        "Monday":    ["Deep Learning",  "NLP",            "Computer Vision","Cloud AI",        "—",              "Lab (DL)",     "Lab (DL)"],
        "Tuesday":   ["NLP",            "Deep Learning",  "Cloud AI",       "Computer Vision", "Prof. Elective", "—",           "—"],
        "Wednesday": ["Computer Vision","Cloud AI",       "Deep Learning",  "NLP",             "—",              "Lab (NLP)",   "Lab (NLP)"],
        "Thursday":  ["Prof. Elective", "Computer Vision","NLP",            "Deep Learning",   "Cloud AI",       "—",           "—"],
        "Friday":    ["Cloud AI",       "NLP",            "Prof. Elective", "Deep Learning",   "Computer Vision","Seminar",     "—"],
        "Saturday":  ["Tutorial",       "Project Work",   "Project Work",   "—",               "—",              "—",          "—"],
    },
    ("CYBER", 1): {
        "Monday":    ["Eng. Maths-I",  "Eng. Physics",   "Problem Solving","Eng. Chemistry",  "Basic Electrical","—",          "—"],
        "Tuesday":   ["Eng. Physics",  "Problem Solving","Eng. Maths-I",   "Eng. Chemistry",  "—",               "Lab (Physics)","Lab (Physics)"],
        "Wednesday": ["Eng. Chemistry","Eng. Maths-I",   "Basic Electrical","Problem Solving", "—",              "Lab (Chem)",  "Lab (Chem)"],
        "Thursday":  ["Problem Solving","Basic Electrical","Eng. Chemistry","Eng. Maths-I",   "Eng. Physics",    "—",           "—"],
        "Friday":    ["Basic Electrical","Eng. Chemistry","Eng. Physics",  "Problem Solving", "Eng. Maths-I",    "Seminar",     "—"],
        "Saturday":  ["Revision",      "Tutorial",       "—",              "—",               "—",               "—",          "—"],
    },
    ("CYBER", 2): {
        "Monday":    ["Data Structures","Computer Nets", "Programming",    "Digital Principles","—",             "Lab (DS)",    "Lab (DS)"],
        "Tuesday":   ["Computer Nets", "Data Structures","Digital Principles","Programming",   "Eng. Maths-II",  "—",          "—"],
        "Wednesday": ["Programming",   "Digital Principles","Computer Nets","Data Structures", "—",              "Lab (Nets)", "Lab (Nets)"],
        "Thursday":  ["Digital Principles","Programming","Data Structures","Computer Nets",   "Eng. Maths-II",  "—",          "—"],
        "Friday":    ["Eng. Maths-II", "Computer Nets", "Digital Principles","Programming",   "Data Structures", "Seminar",   "—"],
        "Saturday":  ["Tutorial",      "Lab (Prog)",    "Lab (Prog)",     "—",               "—",               "—",          "—"],
    },
    ("CYBER", 3): {
        "Monday":    ["Network Security","Cryptography", "Linux & Shell",  "Database Security","—",             "Lab (Kali)",  "Lab (Kali)"],
        "Tuesday":   ["Cryptography",   "Network Security","Database Sec", "Linux & Shell",   "Network Sec",    "—",          "—"],
        "Wednesday": ["Database Sec",   "Linux & Shell", "Cryptography",   "Network Security", "—",             "Lab (DB Sec)","Lab (DB Sec)"],
        "Thursday":  ["Linux & Shell",  "Database Sec",  "Network Security","Cryptography",   "Database Sec",   "—",          "—"],
        "Friday":    ["Cryptography",   "Network Security","Linux & Shell","Database Sec",    "Cryptography",    "Seminar",   "—"],
        "Saturday":  ["Tutorial",       "Lab (Crypto)",  "Lab (Crypto)",   "—",               "—",              "—",         "—"],
    },
    ("CYBER", 4): {
        "Monday":    ["Ethical Hacking","Pen Testing",   "Cyber Laws",     "Malware Analysis", "—",             "Lab (Hack)", "Lab (Hack)"],
        "Tuesday":   ["Pen Testing",   "Ethical Hacking","Malware Analysis","Cyber Laws",      "Prof. Elective", "—",         "—"],
        "Wednesday": ["Cyber Laws",    "Malware Analysis","Ethical Hacking","Pen Testing",     "—",             "Lab (Forensics)","Lab (Forensics)"],
        "Thursday":  ["Prof. Elective","Cyber Laws",     "Pen Testing",    "Ethical Hacking",  "Malware Anal",  "—",         "—"],
        "Friday":    ["Malware Anal",  "Pen Testing",    "Prof. Elective", "Ethical Hacking",  "Cyber Laws",    "Seminar",   "—"],
        "Saturday":  ["Tutorial",      "CTF Practice",   "CTF Practice",   "—",               "—",              "—",         "—"],
    },
    ("MECH", 1): {
        "Monday":    ["Eng. Maths-I",  "Eng. Physics",   "Eng. Chemistry", "Eng. Graphics",   "Workshop",       "—",         "—"],
        "Tuesday":   ["Eng. Physics",  "Eng. Maths-I",   "Eng. Graphics",  "Eng. Chemistry",  "—",              "Lab (Physics)","Lab (Physics)"],
        "Wednesday": ["Eng. Chemistry","Eng. Graphics",  "Eng. Maths-I",   "Workshop",        "Eng. Physics",   "—",         "—"],
        "Thursday":  ["Eng. Graphics", "Workshop",       "Eng. Chemistry", "Eng. Maths-I",    "—",              "Workshop Lab","Workshop Lab"],
        "Friday":    ["Workshop",      "Eng. Chemistry", "Eng. Physics",   "Eng. Graphics",   "Eng. Maths-I",   "Seminar",   "—"],
        "Saturday":  ["Revision",      "Tutorial",       "—",              "—",               "—",              "—",         "—"],
    },
    ("MECH", 2): {
        "Monday":    ["Thermodynamics","Fluid Mechanics","Manufacturing",  "Strength of Mat",  "—",              "Lab (FM)",  "Lab (FM)"],
        "Tuesday":   ["Fluid Mechanics","Thermodynamics","Strength of Mat","Manufacturing",   "Eng. Maths-II",  "—",         "—"],
        "Wednesday": ["Manufacturing", "Strength of Mat","Thermodynamics", "Fluid Mechanics",  "—",             "Workshop",  "Workshop"],
        "Thursday":  ["Strength of Mat","Eng. Maths-II", "Fluid Mechanics","Thermodynamics",  "Manufacturing",  "—",         "—"],
        "Friday":    ["Eng. Maths-II", "Manufacturing",  "Thermodynamics", "Strength of Mat",  "Fluid Mechanics","Seminar",  "—"],
        "Saturday":  ["Tutorial",      "Lab (Thermo)",   "Lab (Thermo)",   "—",               "—",              "—",        "—"],
    },
    ("MECH", 3): {
        "Monday":    ["Heat Transfer", "Kinematics",     "Mfg Processes",  "Metrology",        "—",             "Lab (Heat)","Lab (Heat)"],
        "Tuesday":   ["Kinematics",    "Heat Transfer",  "Metrology",      "Mfg Processes",    "Heat Transfer",  "—",        "—"],
        "Wednesday": ["Mfg Processes", "Metrology",      "Heat Transfer",  "Kinematics",       "—",             "Lab (Mfg)", "Lab (Mfg)"],
        "Thursday":  ["Metrology",     "Mfg Processes",  "Kinematics",     "Heat Transfer",    "Metrology",     "—",        "—"],
        "Friday":    ["Heat Transfer", "Kinematics",     "Mfg Processes",  "Metrology",        "Kinematics",    "Seminar",  "—"],
        "Saturday":  ["Tutorial",      "CAD Lab",        "CAD Lab",        "—",                "—",             "—",        "—"],
    },
    ("MECH", 4): {
        "Monday":    ["Machine Design","FEA",            "Mechatronics",   "Robotics",         "—",             "Lab (FEA)", "Lab (FEA)"],
        "Tuesday":   ["FEA",           "Machine Design", "Robotics",       "Mechatronics",     "Prof. Elective","—",        "—"],
        "Wednesday": ["Mechatronics",  "Robotics",       "Machine Design", "FEA",              "—",             "Lab (Robot)","Lab (Robot)"],
        "Thursday":  ["Prof. Elective","Mechatronics",   "FEA",            "Machine Design",   "Robotics",      "—",        "—"],
        "Friday":    ["Robotics",      "Machine Design", "Prof. Elective", "Mechatronics",     "FEA",           "Seminar",  "—"],
        "Saturday":  ["Tutorial",      "Project Work",   "Project Work",   "—",               "—",              "—",       "—"],
    },
}

YEAR_NAMES = {1: "1st Year", 2: "2nd Year", 3: "3rd Year", 4: "4th Year"}
DEPT_FULL  = {"CSE": "Computer Science Engineering", "IT": "Information Technology",
              "AIDS": "AI & Data Science", "CYBER": "Cyber Security", "MECH": "Mechanical Engineering"}

def draw_timetable(dept, year, schedule):
    W, ROW_H, HDR_H = 1400, 44, 52
    COLS = [180, 165, 165, 10, 165, 165, 10, 165, 165, 165]  # day + 7 periods + 2 special

    # Full column layout: Day | P1 | P2 | BREAK | P3 | P4 | LUNCH | P5 | P6 | P7
    COL_WIDTHS = [160, 160, 160, 90, 160, 160, 90, 160, 160, 160]
    total_w = sum(COL_WIDTHS) + 20
    total_h = HDR_H*2 + ROW_H * len(DAYS) + 80
    H = total_h

    img = Image.new("RGB", (total_w, H), BG)
    draw = ImageDraw.Draw(img)

    try:
        font_title  = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
        font_sub    = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 13)
        font_hdr    = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 12)
        font_cell   = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
        font_time   = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 9)
        font_day    = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 12)
    except:
        font_title = font_sub = font_hdr = font_cell = font_time = font_day = ImageFont.load_default()

    # Title bar
    draw.rectangle([0, 0, total_w, HDR_H], fill=HEADER)
    title = f"St Lourdes Engineering College — {DEPT_FULL.get(dept, dept)} ({dept})"
    draw.text((total_w//2, HDR_H//2), title, fill=TXT_W, font=font_title, anchor="mm")

    # Sub-header
    y_sub = HDR_H
    draw.rectangle([0, y_sub, total_w, y_sub + HDR_H], fill=SUBHEAD)
    sub = f"{YEAR_NAMES[year]}  |  Anna University R2021  |  Mon–Fri: 8:45 AM – 4:30 PM  |  Sat: 8:45 AM – 1:00 PM"
    draw.text((total_w//2, y_sub + HDR_H//2), sub, fill=HEADER, font=font_sub, anchor="mm")

    # Column headers
    y_col = HDR_H * 2
    draw.rectangle([0, y_col, total_w, y_col + ROW_H], fill=HEADER)

    col_labels = ["Day", "Period 1\n8:45–9:40", "Period 2\n9:40–10:35", "BREAK\n10:35–10:45",
                  "Period 3\n10:45–11:40", "Period 4\n11:40–12:35", "LUNCH\n12:35–1:15",
                  "Period 5\n1:15–2:10", "Period 6\n2:10–3:05", "Period 7\n3:05–4:00"]

    x = 0
    for i, (label, cw) in enumerate(zip(col_labels, COL_WIDTHS)):
        cx = x + cw // 2
        cy = y_col + ROW_H // 2
        lines = label.split("\n")
        if len(lines) == 2:
            draw.text((cx, cy - 8), lines[0], fill=TXT_W, font=font_hdr, anchor="mm")
            draw.text((cx, cy + 8), lines[1], fill=(180, 210, 255), font=font_time, anchor="mm")
        else:
            draw.text((cx, cy), lines[0], fill=TXT_W, font=font_hdr, anchor="mm")
        if i < len(COL_WIDTHS) - 1:
            draw.line([x + cw, y_col, x + cw, y_col + ROW_H], fill=(100, 140, 220), width=1)
        x += cw

    # Rows
    for r_idx, day in enumerate(DAYS):
        y = y_col + ROW_H + r_idx * ROW_H
        row_bg = (255, 255, 255) if r_idx % 2 == 0 else ROW_ALT

        day_sched = schedule.get(day, ["—"] * 7)
        # Build full row: day, p1, p2, BREAK, p3, p4, LUNCH, p5, p6, p7
        cells = [day, day_sched[0], day_sched[1], "BREAK", day_sched[2],
                 day_sched[3], "LUNCH", day_sched[4], day_sched[5], day_sched[6]]

        x = 0
        for c_idx, (cell, cw) in enumerate(zip(cells, COL_WIDTHS)):
            # Background
            if cell == "BREAK":
                bg = BREAK_BG
            elif cell == "LUNCH":
                bg = (220, 252, 231)
            elif c_idx == 0:
                bg = SUBHEAD
            else:
                bg = row_bg
            draw.rectangle([x, y, x + cw, y + ROW_H], fill=bg)

            # Text
            cx, cy = x + cw // 2, y + ROW_H // 2
            if c_idx == 0:
                col = HEADER
                f = font_day
            elif cell in ("BREAK", "LUNCH"):
                col = BREAK_TX if cell == "BREAK" else LAB_TX
                f = font_hdr
            elif cell.startswith("Lab"):
                col = LAB_TX
                f = font_cell
            else:
                col = TXT_DK
                f = font_cell

            # Wrap long text
            if len(cell) > 16:
                words = cell.split()
                mid = len(words) // 2
                line1 = " ".join(words[:mid])
                line2 = " ".join(words[mid:])
                draw.text((cx, cy - 8), line1, fill=col, font=f, anchor="mm")
                draw.text((cx, cy + 8), line2, fill=col, font=f, anchor="mm")
            else:
                draw.text((cx, cy), cell, fill=col, font=f, anchor="mm")

            # Borders
            draw.line([x, y, x + cw, y], fill=BORDER, width=1)
            if c_idx < len(COL_WIDTHS) - 1:
                draw.line([x + cw, y, x + cw, y + ROW_H], fill=BORDER, width=1)
            x += cw

        # Right border
        draw.line([total_w - 1, y, total_w - 1, y + ROW_H], fill=BORDER, width=1)

    # Bottom border
    draw.line([0, y_col + ROW_H + len(DAYS)*ROW_H, total_w, y_col + ROW_H + len(DAYS)*ROW_H], fill=BORDER, width=2)

    # Footer
    y_foot = y_col + ROW_H + len(DAYS) * ROW_H + 8
    draw.text((total_w // 2, y_foot + 14), "St Lourdes Engineering College  |  Anna University Affiliated  |  lms.stlourdes.edu",
              fill=TXT_GREY, font=font_time, anchor="mm")

    return img

generated = []
for (dept, year), schedule in SCHEDULES.items():
    out_path = os.path.join(BASE, f"{dept.lower()}_year{year}_timetable.png")
    img = draw_timetable(dept, year, schedule)
    img.save(out_path, "PNG", optimize=True)
    size_kb = os.path.getsize(out_path) // 1024
    print(f"  Created: {dept} Year {year} → {os.path.basename(out_path)} ({size_kb} KB)")
    generated.append(out_path)

print(f"\nTotal: {len(generated)} timetable images generated!")

print("\n--- All 20 timetable images created successfully! ---")
print(f"Location: {BASE}")
print("\nRestart your backend server now (python run.py)")