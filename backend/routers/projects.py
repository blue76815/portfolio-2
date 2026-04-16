from fastapi import APIRouter, Depends, HTTPException, status
from models import ProjectCreate
from auth_utils import get_current_user
from database import get_db

router = APIRouter(prefix="/api/projects", tags=["作品集"])


@router.get("")
def get_projects():
    """取得所有作品（公開）"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM projects ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()

    projects = [dict(row) for row in rows]
    return {"success": True, "data": projects, "message": "取得作品列表成功"}


@router.get("/{project_id}")
def get_project(project_id: int):
    """取得單筆作品（公開）"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="作品不存在")

    return {"success": True, "data": dict(row), "message": "取得作品成功"}


@router.post("")
def create_project(project: ProjectCreate, current_user: dict = Depends(get_current_user)):
    """新增作品（需認證）"""
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO projects (title, description, tech_stack, image_url, demo_url, github_url) VALUES (?, ?, ?, ?, ?, ?)",
            (project.title, project.description, project.tech_stack, project.image_url, project.demo_url, project.github_url)
        )
        conn.commit()
        new_id = cursor.lastrowid
        cursor.execute("SELECT * FROM projects WHERE id = ?", (new_id,))
        new_project = dict(cursor.fetchone())
        conn.close()
        return {"success": True, "data": new_project, "message": "新增作品成功"}
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{project_id}")
def update_project(project_id: int, project: ProjectCreate, current_user: dict = Depends(get_current_user)):
    """更新作品（需認證）"""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="作品不存在")

    try:
        cursor.execute(
            "UPDATE projects SET title=?, description=?, tech_stack=?, image_url=?, demo_url=?, github_url=? WHERE id=?",
            (project.title, project.description, project.tech_stack, project.image_url, project.demo_url, project.github_url, project_id)
        )
        conn.commit()
        cursor.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
        updated = dict(cursor.fetchone())
        conn.close()
        return {"success": True, "data": updated, "message": "更新作品成功"}
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{project_id}")
def delete_project(project_id: int, current_user: dict = Depends(get_current_user)):
    """刪除作品（需認證）"""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="作品不存在")

    cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))
    conn.commit()
    conn.close()

    return {"success": True, "data": None, "message": "刪除作品成功"}
