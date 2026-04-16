from fastapi import APIRouter, Depends, HTTPException, status
from models import LoginRequest, TokenResponse
from auth_utils import hash_password, verify_password, create_token, get_current_user
from database import get_db

router = APIRouter(prefix="/api/auth", tags=["認證"])


@router.post("/login")
def login(req: LoginRequest):
    """登入並取得 JWT token"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (req.username,))
    user = cursor.fetchone()
    conn.close()

    if not user or not verify_password(req.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="帳號或密碼錯誤"
        )

    token = create_token({"sub": user["username"], "user_id": user["id"]})
    return {
        "success": True,
        "data": {"access_token": token, "token_type": "bearer"},
        "message": "登入成功"
    }


@router.post("/init")
def init_admin():
    """建立預設管理員帳號"""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", ("admin",))
    if cursor.fetchone():
        conn.close()
        return {"success": True, "message": "管理員帳號已存在"}

    hashed = hash_password("admin123")
    cursor.execute(
        "INSERT INTO users (username, password_hash) VALUES (?, ?)",
        ("admin", hashed)
    )
    conn.commit()
    conn.close()

    return {"success": True, "message": "預設管理員帳號建立成功（admin / admin123）"}


@router.get("/me")
def get_me(current_user: dict = Depends(get_current_user)):
    """取得當前登入的使用者資訊"""
    return {
        "success": True,
        "data": {
            "username": current_user["sub"],
            "user_id": current_user["user_id"]
        },
        "message": "取得使用者資訊成功"
    }
