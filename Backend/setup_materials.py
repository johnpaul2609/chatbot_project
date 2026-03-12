"""
Run this ONCE from your Backend folder:
    python setup_materials.py

It will:
1. Create the materials/ folders and PDF files
2. Insert the material records into college_chatbot.db
"""

import sqlite3
import os

# ── Step 1: Generate PDFs ─────────────────────────────────────────────────────
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
    from reportlab.lib.enums import TA_CENTER
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False
    print("reportlab not installed — installing now...")
    os.system("pip install reportlab")
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
    from reportlab.lib.enums import TA_CENTER

BASE = os.path.dirname(os.path.abspath(__file__))

NOTES = {
    "materials/ds/data_structures.pdf": {
        "title": "Data Structures & Algorithms",
        "dept": "CSE / IT", "semester": "Semester 3",
        "content": [
            ("1. Introduction", ["Data structure = way to organize data efficiently.",
                "Types: Linear (Array, Linked List, Stack, Queue), Non-Linear (Tree, Graph).",
                "Time Complexity: O(1) constant | O(n) linear | O(log n) log | O(n²) quadratic."]),
            ("2. Arrays", ["Stores same-type elements in contiguous memory. Access: O(1).",
                "Search O(n) | Insert/Delete O(n) due to shifting.",
                "Applications: Sorting, matrix ops, lookup tables."]),
            ("3. Linked List", ["Nodes with data + pointer to next node. Dynamic size.",
                "Singly: one direction | Doubly: both directions | Circular: last→first.",
                "Insert at head O(1) | Search O(n) | No random access."]),
            ("4. Stack (LIFO)", ["push() add to top | pop() remove from top | peek() view top. All O(1).",
                "Applications: Function calls, undo, expression evaluation, backtracking."]),
            ("5. Queue (FIFO)", ["enqueue() add to rear | dequeue() remove from front.",
                "Types: Simple, Circular, Priority, Dequeue.",
                "Applications: CPU scheduling, BFS traversal, printer queue."]),
            ("6. Trees", ["Hierarchical structure. Binary Tree: max 2 children per node.",
                "BST: left < root < right. Search/Insert O(log n) average.",
                "Traversals: Inorder (LNR) | Preorder (NLR) | Postorder (LRN).",
                "AVL Tree: self-balancing BST. Height difference ≤ 1."]),
            ("7. Graphs", ["G = (V, E). Directed/Undirected, Weighted/Unweighted.",
                "BFS: uses Queue, O(V+E) | DFS: uses Stack/Recursion, O(V+E).",
                "Dijkstra: shortest path | Kruskal/Prim: minimum spanning tree."]),
            ("8. Sorting", ["Bubble O(n²) | Selection O(n²) | Insertion O(n²) best O(n).",
                "Merge Sort O(n log n) always, stable | Quick Sort O(n log n) avg.",
                "Heap Sort O(n log n) in-place."]),
            ("9. Searching", ["Linear Search O(n) | Binary Search O(log n) — array must be sorted.",
                "Hashing O(1) avg. Collision: Chaining or Open Addressing."]),
            ("Key Formulas", ["Max nodes in binary tree height h: 2^(h+1) - 1",
                "Min height for n nodes: floor(log2 n)",
                "Anna Univ R2021: 2 marks = define/state | 13 marks = explain with diagram"]),
        ]
    },
    "materials/cn/computer_networks.pdf": {
        "title": "Computer Networks",
        "dept": "CSE / IT", "semester": "Semester 4",
        "content": [
            ("1. OSI Model (7 Layers)", ["Physical: raw bits over medium (cables, radio).",
                "Data Link: frames, MAC addresses, CRC error detection.",
                "Network: routing, IP addressing. Protocol: IP, ICMP.",
                "Transport: TCP (reliable, ordered) | UDP (fast, no guarantee).",
                "Session, Presentation, Application: HTTP, FTP, SMTP, DNS, DHCP."]),
            ("2. TCP/IP Model", ["4 layers: Network Access, Internet, Transport, Application.",
                "IPv4: 32-bit (e.g. 192.168.1.1) | IPv6: 128-bit.",
                "TCP 3-way handshake: SYN → SYN-ACK → ACK.",
                "UDP: connectionless, used in streaming, DNS, gaming."]),
            ("3. Network Devices", ["Hub: broadcasts to all (Layer 1) | Switch: uses MAC table (Layer 2).",
                "Router: routes using IP (Layer 3) | Firewall: filters traffic.",
                "Gateway: connects different-protocol networks."]),
            ("4. DNS & DHCP", ["DNS: domain → IP address. Hierarchy: Root → TLD → Authoritative.",
                "DHCP: auto-assigns IP, subnet mask, gateway.",
                "DHCP process: DISCOVER → OFFER → REQUEST → ACK."]),
            ("5. HTTP & Web", ["HTTP: stateless. Methods: GET, POST, PUT, DELETE.",
                "HTTPS: HTTP + TLS. Port 443. Status: 200 OK | 404 Not Found | 500 Error.",
                "REST API uses HTTP methods for CRUD."]),
            ("6. Network Security", ["Threats: DoS, MitM, Phishing, SQL Injection.",
                "SSL/TLS: encrypts data in transit. VPN: encrypted tunnel.",
                "IDS/IPS: intrusion detection and prevention."]),
        ]
    },
    "materials/dbms/database_management.pdf": {
        "title": "Database Management Systems (DBMS)",
        "dept": "CSE / IT", "semester": "Semester 3",
        "content": [
            ("1. Introduction", ["DBMS: software to manage databases. Examples: MySQL, Oracle, SQLite, PostgreSQL.",
                "Advantages: reduced redundancy, data integrity, concurrent access, security.",
                "3-tier architecture: External (user) | Conceptual (logical) | Internal (physical)."]),
            ("2. ER Model", ["Entity: real-world object. Attribute: property of entity.",
                "Relationship: association between entities. Cardinality: 1:1, 1:N, M:N.",
                "Primary Key: uniquely identifies record. Foreign Key: references another table."]),
            ("3. SQL", ["DDL: CREATE, ALTER, DROP, TRUNCATE.",
                "DML: SELECT, INSERT, UPDATE, DELETE.",
                "DCL: GRANT, REVOKE | TCL: COMMIT, ROLLBACK, SAVEPOINT.",
                "Example: SELECT name FROM students WHERE dept='CSE' ORDER BY name;",
                "Joins: INNER, LEFT, RIGHT, FULL OUTER. Aggregates: COUNT, SUM, AVG, MIN, MAX."]),
            ("4. Normalization", ["1NF: atomic values, no repeating groups.",
                "2NF: 1NF + no partial dependency.",
                "3NF: 2NF + no transitive dependency.",
                "BCNF: stricter 3NF — every determinant must be a candidate key."]),
            ("5. Transactions & ACID", ["ACID: Atomicity, Consistency, Isolation, Durability.",
                "Concurrency problems: Dirty Read, Non-repeatable Read, Phantom Read.",
                "Locking: Shared (read) | Exclusive (write).",
                "Deadlock: circular wait. Resolution: timeout or detection + rollback."]),
            ("6. Indexing", ["Index speeds up search. B+ Tree: all data in leaves, O(log n).",
                "Hashing: O(1) avg. Types: Primary, Secondary, Clustered, Non-clustered."]),
        ]
    },
    "materials/os/operating_systems.pdf": {
        "title": "Operating Systems",
        "dept": "CSE / IT", "semester": "Semester 4",
        "content": [
            ("1. Introduction", ["OS manages hardware and software resources.",
                "Functions: process mgmt, memory mgmt, file system, I/O, security.",
                "Types: Batch, Time-sharing, Real-time, Distributed, Mobile."]),
            ("2. Process Management", ["Process: program in execution. Has own memory space.",
                "States: New → Ready → Running → Waiting → Terminated.",
                "PCB stores process state, PC, registers, memory info.",
                "Thread: lightweight process, shares memory with parent."]),
            ("3. CPU Scheduling", ["FCFS: simple, non-preemptive, convoy effect.",
                "SJF: optimal average wait, can cause starvation.",
                "Round Robin: time quantum, fair, high context switching.",
                "Priority: highest priority first. Aging fixes starvation."]),
            ("4. Memory Management", ["Paging: fixed-size pages, no external fragmentation.",
                "Segmentation: variable-size, has external fragmentation.",
                "Virtual Memory: disk as RAM extension. Page replacement: FIFO, LRU, Optimal."]),
            ("5. Deadlock", ["Conditions: Mutual Exclusion, Hold & Wait, No Preemption, Circular Wait.",
                "Prevention: deny one condition. Avoidance: Banker's Algorithm.",
                "Detection & Recovery: kill process or preempt resource."]),
            ("6. File Systems", ["File allocation: Contiguous (fast) | Linked | Indexed.",
                "FAT: old Windows | NTFS: modern Windows | ext4: Linux.",
                "UNIX permissions: rwx for Owner, Group, Others. chmod command."]),
        ]
    },
    "materials/ml/machine_learning.pdf": {
        "title": "Machine Learning",
        "dept": "CSE / AIDS", "semester": "Semester 5",
        "content": [
            ("1. Introduction", ["ML: systems that learn from data without explicit programming.",
                "Types: Supervised (labeled) | Unsupervised (unlabeled) | Reinforcement (reward).",
                "Libraries: scikit-learn, TensorFlow, PyTorch, NumPy, Pandas, Matplotlib."]),
            ("2. Supervised Learning", ["Regression: predict continuous output (e.g. house price).",
                "Linear Regression: y = mx + b. Logistic Regression: uses sigmoid, output 0-1.",
                "Decision Tree: if-else rules. Random Forest: ensemble of trees.",
                "SVM: finds optimal hyperplane to separate classes."]),
            ("3. Unsupervised Learning", ["K-Means: assign to k clusters by minimizing distance to centroid.",
                "Hierarchical: builds dendrogram. PCA: dimensionality reduction.",
                "Association Rules: Apriori algorithm, used in recommendations."]),
            ("4. Model Evaluation", ["Train/Test split: 80/20 or 70/30. K-fold cross validation.",
                "Accuracy | Precision = TP/(TP+FP) | Recall = TP/(TP+FN) | F1 = harmonic mean.",
                "Confusion Matrix: TP, TN, FP, FN.",
                "Overfitting fix: more data, regularization, dropout."]),
            ("5. Neural Networks", ["Input → Hidden → Output layers. Neuron: weighted sum + activation.",
                "Activations: ReLU max(0,x) | Sigmoid 1/(1+e^-x) | Tanh.",
                "Backpropagation: calculates gradient, updates weights via gradient descent.",
                "CNN: for images (filters/kernels). RNN/LSTM: sequential data."]),
        ]
    },
    "materials/math/engineering_mathematics.pdf": {
        "title": "Engineering Mathematics",
        "dept": "All Departments", "semester": "Semester 1 & 2",
        "content": [
            ("1. Matrices", ["Types: Square, Identity, Diagonal, Symmetric.",
                "Determinant 2×2: |A| = ad - bc. Inverse: A⁻¹ = Adj(A)/|A|.",
                "Eigenvalues λ: det(A - λI) = 0. Rank: max linearly independent rows."]),
            ("2. Differential Calculus", ["d/dx[xⁿ] = nxⁿ⁻¹ | Chain: f'(g(x))·g'(x) | Product: (uv)' = u'v+uv'.",
                "Critical points: f'(x)=0. Max: f''<0 | Min: f''>0.",
                "Taylor Series: f(x) = f(a) + f'(a)(x-a) + f''(a)(x-a)²/2! + ..."]),
            ("3. Integral Calculus", ["∫xⁿ dx = xⁿ⁺¹/(n+1)+C | ∫eˣdx = eˣ+C | ∫sin x dx = -cos x+C.",
                "Definite Integral: ∫[a,b] f(x)dx = F(b)-F(a).",
                "Integration by Parts: ∫u dv = uv - ∫v du."]),
            ("4. Differential Equations", ["1st Order: dy/dx + Py = Q → integrating factor e^∫P dx.",
                "2nd Order: ar²+br+c=0 characteristic equation.",
                "Laplace: L{1}=1/s | L{t}=1/s² | L{eᵃᵗ}=1/(s-a) | L{sin at}=a/(s²+a²)."]),
            ("5. Statistics & Probability", ["Mean=Σx/n | Variance σ²=Σ(x-μ)²/n | Std Dev=√Variance.",
                "P(A∪B) = P(A)+P(B)-P(A∩B). Bayes: P(A|B)=P(B|A)P(A)/P(B).",
                "Distributions: Normal (bell curve), Binomial, Poisson."]),
        ]
    },
}

title_style   = ParagraphStyle("t",  fontSize=18, fontName="Helvetica-Bold",
                                textColor=colors.HexColor("#1e40af"), alignment=TA_CENTER, spaceAfter=4)
meta_style    = ParagraphStyle("m",  fontSize=9,  fontName="Helvetica",
                                textColor=colors.HexColor("#6b7280"), alignment=TA_CENTER, spaceAfter=4)
heading_style = ParagraphStyle("h",  fontSize=12, fontName="Helvetica-Bold",
                                textColor=colors.HexColor("#1e3a8a"), spaceBefore=12, spaceAfter=4)
body_style    = ParagraphStyle("b",  fontSize=9.5,fontName="Helvetica",
                                textColor=colors.HexColor("#1f2937"), leading=15, spaceAfter=3, leftIndent=8)

print("\n--- Generating PDFs ---")
for rel_path, info in NOTES.items():
    full_path = os.path.join(BASE, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    doc = SimpleDocTemplate(full_path, pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)
    story = []
    story.append(Paragraph("St Lourdes Engineering College", meta_style))
    story.append(Paragraph(info["title"], title_style))
    story.append(Paragraph(f"Dept: {info['dept']}  |  {info['semester']}  |  Anna University R2021", meta_style))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#1e40af"), spaceAfter=10))

    for section_title, points in info["content"]:
        story.append(Paragraph(section_title, heading_style))
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#d1d5db"), spaceAfter=3))
        for point in points:
            story.append(Paragraph(f"• {point}", body_style))
        story.append(Spacer(1, 4))

    doc.build(story)
    kb = os.path.getsize(full_path) // 1024
    print(f"  Created: {rel_path} ({kb} KB)")


# ── Step 2: Update Database ───────────────────────────────────────────────────
print("\n--- Updating Database ---")
db_path = os.path.join(BASE, "college_chatbot.db")

if not os.path.exists(db_path):
    print(f"ERROR: Database not found at {db_path}")
    print("Please run create_database.py first.")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Add file_url column if missing
try:
    cursor.execute("ALTER TABLE study_materials ADD COLUMN file_url TEXT")
    print("  Added file_url column")
except:
    pass  # column already exists

# Clear old/dummy records and insert real ones
cursor.execute("DELETE FROM study_materials")

materials = [
    ("mat_ds_001",  "Data Structures",          "Complete Notes", "data_structures.pdf",
     "materials/ds/data_structures.pdf",
     "Arrays, Linked List, Stack, Queue, Trees, Graphs, Sorting & Searching",
     "CSE", 3, "/api/materials/download/mat_ds_001"),

    ("mat_cn_001",  "Computer Networks",         "Complete Notes", "computer_networks.pdf",
     "materials/cn/computer_networks.pdf",
     "OSI Model, TCP/IP, DNS, HTTP, Network Devices, Security",
     "CSE", 4, "/api/materials/download/mat_cn_001"),

    ("mat_db_001",  "DBMS",                      "Complete Notes", "database_management.pdf",
     "materials/dbms/database_management.pdf",
     "ER Model, SQL, Normalization, Transactions, Indexing",
     "CSE", 3, "/api/materials/download/mat_db_001"),

    ("mat_os_001",  "Operating Systems",         "Complete Notes", "operating_systems.pdf",
     "materials/os/operating_systems.pdf",
     "Process Management, CPU Scheduling, Memory, Deadlock, File Systems",
     "CSE", 4, "/api/materials/download/mat_os_001"),

    ("mat_ml_001",  "Machine Learning",          "Complete Notes", "machine_learning.pdf",
     "materials/ml/machine_learning.pdf",
     "Supervised, Unsupervised, Neural Networks, Model Evaluation",
     "CSE", 5, "/api/materials/download/mat_ml_001"),

    ("mat_ma_001",  "Engineering Mathematics",   "Complete Notes", "engineering_mathematics.pdf",
     "materials/math/engineering_mathematics.pdf",
     "Matrices, Calculus, ODE, Laplace Transform, Statistics",
     "ALL", 1, "/api/materials/download/mat_ma_001"),
]

cursor.executemany("""
    INSERT INTO study_materials
      (material_id, subject, topic, file_name, file_path,
       description, department, semester, file_url)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", materials)

conn.commit()

print("\n  Materials in database:")
cursor.execute("SELECT material_id, subject, file_name FROM study_materials")
for row in cursor.fetchall():
    print(f"    {row[0]}  |  {row[1]}  |  {row[2]}")

conn.close()
print("\nDone! Restart your backend server now.")