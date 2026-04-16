from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from models import MessageCreate
from auth_utils import get_current_user
from database import get_db

router = APIRouter(prefix="/api/messages", tags=["留言"])


class MessageUpdate(BaseModel):
    is_read: Optional[int] = None


@router.get("/stats")
def get_message_stats(current_user: dict = Depends(get_current_user)):
    """留言統計：總數 + 未讀數（需認證）"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as total FROM messages")
    total = cursor.fetchone()["total"]
    cursor.execute("SELECT COUNT(*) as unread FROM messages WHERE is_read = 0")
    unread = cursor.fetchone()["unread"]
    conn.close()

    return {
        "success": True,
        "data": {"total": total, "unread": unread},
        "message": "取得留言統計成功"
    }


@router.get("")
def get_messages(current_user: dict = Depends(get_current_user)):
    """取得所有留言（需認證）"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM messages ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()

    messages = [dict(row) for row in rows]
    return {"success": True, "data": messages, "message": "取得留言列表成功"}


@router.get("/{message_id}")
def get_message(message_id: int, current_user: dict = Depends(get_current_user)):
    """取得單筆留言（需認證）"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM messages WHERE id = ?", (message_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="留言不存在")

    return {"success": True, "data": dict(row), "message": "取得留言成功"}


@router.post("")
def create_message(message: MessageCreate):
    """新增留言（公開，給訪客用）"""
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO messages (name, email, content) VALUES (?, ?, ?)",
            (message.name, message.email, message.content)
        )
        conn.commit()
        new_id = cursor.lastrowid
        cursor.execute("SELECT * FROM messages WHERE id = ?", (new_id,))
        new_msg = dict(cursor.fetchone())
        conn.close()
        return {"success": True, "data": new_msg, "message": "留言送出成功"}
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{message_id}")
def update_message(message_id: int, update: MessageUpdate, current_user: dict = Depends(get_current_user)):
    """更新留言狀態（需認證）"""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM messages WHERE id = ?", (message_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="留言不存在")

    if update.is_read is not None:
        cursor.execute("UPDATE messages SET is_read = ? WHERE id = ?", (update.is_read, message_id))

    conn.commit()
    cursor.execute("SELECT * FROM messages WHERE id = ?", (message_id,))
    updated = dict(cursor.fetchone())
    conn.close()

    return {"success": True, "data": updated, "message": "更新留言成功"}


@router.delete("/{message_id}")
def delete_message(message_id: int, current_user: dict = Depends(get_current_user)):
    """刪除留言（需認證）"""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM messages WHERE id = ?", (message_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="留言不存在")

    cursor.execute("DELETE FROM messages WHERE id = ?", (message_id,))
    conn.commit()
    conn.close()

    return {"success": True, "data": None, "message": "刪除留言成功"}
