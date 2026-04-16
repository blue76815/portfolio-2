"""建立測試資料的腳本"""
import sqlite3
import os
from auth_utils import hash_password

DB_PATH = os.path.join(os.path.dirname(__file__), "portfolio.db")


def seed():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 建立管理員帳號（如果不存在）
    cursor.execute("SELECT * FROM users WHERE username = ?", ("admin",))
    if not cursor.fetchone():
        hashed = hash_password("admin123")
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", ("admin", hashed))

    # 新增 3 筆範例作品
    projects = [
        ("電商購物平台", "完整的線上購物系統，包含商品瀏覽、購物車、結帳流程和後台訂單管理功能。", "React, Node.js, MongoDB, Stripe", "", "https://demo.example.com", "https://github.com/example/shop"),
        ("即時數據儀表板", "企業級即時數據視覺化儀表板，支援多種圖表類型、資料篩選和自動匯出 PDF 報表。", "Vue.js, Python, D3.js, WebSocket", "", "https://demo.example.com", "https://github.com/example/dashboard"),
        ("智慧聊天機器人", "整合 OpenAI API 的多輪對話系統，支援上下文記憶、知識庫搜尋和多語言回應。", "Python, FastAPI, OpenAI, Redis", "", "https://demo.example.com", "https://github.com/example/chatbot"),
    ]

    cursor.execute("SELECT COUNT(*) FROM projects")
    if cursor.fetchone()[0] == 0:
        for title, desc, tech, img, demo, github in projects:
            cursor.execute(
                "INSERT INTO projects (title, description, tech_stack, image_url, demo_url, github_url) VALUES (?, ?, ?, ?, ?, ?)",
                (title, desc, tech, img, demo, github)
            )

    # 新增 2 筆範例留言
    messages = [
        ("王小明", "ming@example.com", "你好！我對你的電商平台專案很有興趣，想了解更多技術細節，方便聊聊嗎？"),
        ("李美玲", "meiling@example.com", "你的作品集網站做得很漂亮，請問有接案的意願嗎？我們公司正在找前端工程師合作。"),
    ]

    cursor.execute("SELECT COUNT(*) FROM messages")
    if cursor.fetchone()[0] == 0:
        for name, email, content in messages:
            cursor.execute(
                "INSERT INTO messages (name, email, content) VALUES (?, ?, ?)",
                (name, email, content)
            )

    # 新增 1 筆個人資料
    cursor.execute("SELECT COUNT(*) FROM profile")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "INSERT INTO profile (name, title, bio, avatar_url, email, github, linkedin) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                "開發者",
                "全端工程師",
                "我是一位熱愛技術的全端工程師，擁有多年的前後端開發經驗。喜歡探索新技術，致力於打造高品質、優美且實用的數位產品。",
                "",
                "hello@example.com",
                "https://github.com/myprofile",
                "https://linkedin.com/in/myprofile"
            )
        )

    conn.commit()
    conn.close()
    print("測試資料建立完成！")


if __name__ == "__main__":
    seed()
