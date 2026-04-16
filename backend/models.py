from pydantic import BaseModel
from typing import Optional


# === 認證相關 ===
class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# === 作品集相關 ===
class ProjectCreate(BaseModel):
    title: str
    description: Optional[str] = ""
    tech_stack: Optional[str] = ""
    image_url: Optional[str] = ""
    demo_url: Optional[str] = ""
    github_url: Optional[str] = ""


class ProjectResponse(BaseModel):
    id: int
    title: str
    description: str
    tech_stack: str
    image_url: str
    demo_url: str
    github_url: str
    created_at: str


# === 留言相關 ===
class MessageCreate(BaseModel):
    name: str
    email: str
    content: str


class MessageResponse(BaseModel):
    id: int
    name: str
    email: str
    content: str
    is_read: int
    created_at: str


# === 個人資料相關 ===
class ProfileUpdate(BaseModel):
    name: Optional[str] = ""
    title: Optional[str] = ""
    bio: Optional[str] = ""
    avatar_url: Optional[str] = ""
    email: Optional[str] = ""
    github: Optional[str] = ""
    linkedin: Optional[str] = ""


class ProfileResponse(BaseModel):
    id: int
    name: str
    title: str
    bio: str
    avatar_url: str
    email: str
    github: str
    linkedin: str
    updated_at: str
