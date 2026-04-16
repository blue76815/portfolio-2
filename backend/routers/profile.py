from fastapi import APIRouter, Depends, HTTPException
from models import ProfileUpdate
from auth_utils import get_current_user
from database import get_db

router = APIRouter(prefix="/api/profile", tags=["個人資料"])


@router.get("")
def get_profile():
    """取得個人資料（公開）"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM profile LIMIT 1")
    row = cursor.fetchone()
    conn.close()

    if not row:
        return {"success": True, "data": None, "message": "尚無個人資料"}

    return {"success": True, "data": dict(row), "message": "取得個人資料成功"}


@router.put("")
def update_profile(profile: ProfileUpdate, current_user: dict = Depends(get_current_user)):
    """更新個人資料（需認證）"""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM profile LIMIT 1")
    existing = cursor.fetchone()

    try:
        if existing:
            cursor.execute(
                """UPDATE profile SET name=?, title=?, bio=?, avatar_url=?, email=?, github=?, linkedin=?, updated_at=CURRENT_TIMESTAMP
                   WHERE id=?""",
                (profile.name, profile.title, profile.bio, profile.avatar_url, profile.email, profile.github, profile.linkedin, existing["id"])
            )
        else:
            cursor.execute(
                "INSERT INTO profile (name, title, bio, avatar_url, email, github, linkedin) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (profile.name, profile.title, profile.bio, profile.avatar_url, profile.email, profile.github, profile.linkedin)
            )
        conn.commit()

        cursor.execute("SELECT * FROM profile LIMIT 1")
        updated = dict(cursor.fetchone())
        conn.close()
        return {"success": True, "data": updated, "message": "更新個人資料成功"}
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=str(e))
