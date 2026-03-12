from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.database_sqlite import Database
import os

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@router.get("/download/{material_id}")
async def download_material(material_id: str):
    """Serve a study material PDF for download"""
    rows = Database.execute_query(
        "SELECT * FROM study_materials WHERE material_id = ?", (material_id,)
    )
    if not rows:
        raise HTTPException(status_code=404, detail="Material not found")

    material = rows[0]
    file_path = os.path.join(BASE_DIR, material["file_path"])

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found on server")

    # Increment download count
    Database.execute_insert(
        "UPDATE study_materials SET downloads = downloads + 1 WHERE material_id = ?",
        (material_id,)
    )

    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename=material["file_name"],
        headers={"Content-Disposition": f"attachment; filename={material['file_name']}"}
    )

@router.get("/list")
async def list_materials(department: str = None, subject: str = None):
    """List all available study materials"""
    query = "SELECT * FROM study_materials WHERE 1=1"
    params = []
    if department:
        query += " AND (department = ? OR department = 'ALL')"
        params.append(department.upper())
    if subject:
        query += " AND LOWER(subject) LIKE ?"
        params.append(f"%{subject.lower()}%")
    rows = Database.execute_query(query, tuple(params))
    return {"materials": [dict(r) for r in rows]}

@router.get("/search/{keyword}")
async def search_materials(keyword: str):
    """Search materials by keyword"""
    kw = f"%{keyword.lower()}%"
    rows = Database.execute_query(
        """SELECT * FROM study_materials
           WHERE LOWER(subject) LIKE ? OR LOWER(description) LIKE ?
              OR LOWER(topic) LIKE ? OR LOWER(department) LIKE ?""",
        (kw, kw, kw, kw)
    )
    return {"materials": [dict(r) for r in rows]}

@router.get("/timetable/{dept}/{year}")
async def get_timetable(dept: str, year: int):
    """Serve timetable image for a department and year"""
    dept_upper = dept.upper()
    valid_depts = ["CSE", "IT", "AIDS", "CYBER", "MECH"]
    if dept_upper not in valid_depts:
        raise HTTPException(status_code=404, detail=f"Department {dept} not found")
    if year not in [1, 2, 3, 4]:
        raise HTTPException(status_code=404, detail="Year must be 1, 2, 3, or 4")

    file_path = os.path.join(BASE_DIR, "materials", "timetables",
                             f"{dept_upper.lower()}_year{year}_timetable.png")

    # Debug: print exact path being checked (you'll see this in your terminal)
    print(f"[TIMETABLE] Looking for: {file_path}")
    print(f"[TIMETABLE] File exists: {os.path.exists(file_path)}")
    print(f"[TIMETABLE] BASE_DIR is: {BASE_DIR}")

    if not os.path.exists(file_path):
        # List what IS in the timetables folder (if it exists)
        tt_dir = os.path.join(BASE_DIR, "materials", "timetables")
        if os.path.exists(tt_dir):
            files = os.listdir(tt_dir)
            raise HTTPException(status_code=404, detail=f"File not found: {file_path}. Available files: {files[:5]}")
        else:
            raise HTTPException(status_code=404, detail=f"Timetables folder does not exist: {tt_dir}. Run generate_timetables.py first.")

    return FileResponse(
        path=file_path,
        media_type="image/png",
        filename=f"{dept_upper}_Year{year}_Timetable.png"
    )