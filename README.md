# Portfolio Website - 個人履歷網站

一個使用 **FastAPI + 原生 HTML/CSS/JS** 打造的全端個人履歷網站，具備精美深色主題、GSAP 動畫效果、完整的後台管理系統。

## 功能特色

### 前台（5 個頁面）
- **首頁** — 全螢幕 Hero + 打字機效果 + 漸層標題 + 精選作品
- **作品集** — Grid 卡片排列 + hover 發光效果 + API 動態載入
- **關於我** — 個人介紹 + 技能列表 + 經歷時間軸 + 學歷
- **聯絡我** — 表單送出留言 + 聯絡資訊卡片
- **登入頁** — JWT 認證登入 + 跳轉後台

### 後台管理（4 個頁面）
- **儀表板** — 作品總數 / 留言統計 / 未讀留言數
- **作品管理** — CRUD 操作（新增 / 編輯 / 刪除）+ Modal 彈窗
- **留言管理** — 查看 / 標記已讀 / 刪除留言
- **個人資料** — 編輯個人資訊（顯示於前台「關於我」）

### 後端 API
- FastAPI + SQLite + JWT 認證
- RESTful 設計，統一 JSON 回傳格式
- bcrypt 密碼雜湊 + 24 小時 token 有效期

## 技術棧

| 層級 | 技術 |
|------|------|
| 前端 | HTML5, Tailwind CSS (CDN), GSAP + ScrollTrigger |
| 後端 | Python, FastAPI, SQLite3, PyJWT, bcrypt |
| 設計 | 深色主題 (slate-900), Glassmorphism, 漸層色 |
| 動畫 | GSAP ScrollTrigger, 打字機效果, 視差滾動 |

## 快速開始

### 1. 安裝後端相依套件

```bash
cd backend
pip install -r requirements.txt
```

### 2. 初始化資料庫 & 測試資料

```bash
cd backend
python seed.py
```

### 3. 啟動後端伺服器

```bash
cd backend
uvicorn main:app --reload --port 8000
```

### 4. 啟動前端伺服器

```bash
cd frontend
python -m http.server 8080
```

### 5. 開啟瀏覽器

- 前台首頁：http://localhost:8080/index.html
- 後台管理：http://localhost:8080/admin/dashboard.html
- API 文件：http://localhost:8000/docs

### 預設管理員帳號

```
帳號：admin
密碼：admin123
```

> 首次使用請先呼叫 `POST /api/auth/init` 或執行 `python seed.py` 建立管理員帳號。

## 專案結構

```
portfolio-website/
├── frontend/               ← 前台頁面
│   ├── index.html           首頁
│   ├── projects.html        作品集
│   ├── about.html           關於我
│   ├── contact.html         聯絡我
│   ├── login.html           登入
│   ├── css/
│   │   └── performance.css  效能優化 CSS
│   ├── admin/               ← 後台管理
│   │   ├── dashboard.html   儀表板
│   │   ├── projects.html    作品管理
│   │   ├── messages.html    留言管理
│   │   ├── profile.html     個人資料
│   │   └── js/
│   │       └── auth.js      認證共用模組
│   ├── js/
│   └── images/
├── backend/                 ← FastAPI 後端
│   ├── main.py              主程式入口
│   ├── database.py          資料庫模組
│   ├── models.py            Pydantic Models
│   ├── auth_utils.py        JWT + bcrypt 認證
│   ├── seed.py              測試資料腳本
│   ├── requirements.txt     Python 套件
│   └── routers/
│       ├── auth.py          認證路由
│       ├── projects.py      作品 CRUD
│       ├── messages.py      留言 CRUD
│       └── profile.py       個人資料
└── .gitignore
```

## API 端點

| 方法 | 路徑 | 說明 | 認證 |
|------|------|------|------|
| GET | `/` | API 狀態 | 不需要 |
| POST | `/api/auth/init` | 建立管理員 | 不需要 |
| POST | `/api/auth/login` | 登入 | 不需要 |
| GET | `/api/auth/me` | 當前使用者 | 需要 |
| GET | `/api/projects` | 作品列表 | 不需要 |
| GET | `/api/projects/{id}` | 單筆作品 | 不需要 |
| POST | `/api/projects` | 新增作品 | 需要 |
| PUT | `/api/projects/{id}` | 更新作品 | 需要 |
| DELETE | `/api/projects/{id}` | 刪除作品 | 需要 |
| GET | `/api/messages` | 留言列表 | 需要 |
| POST | `/api/messages` | 新增留言 | 不需要 |
| PUT | `/api/messages/{id}` | 更新留言 | 需要 |
| DELETE | `/api/messages/{id}` | 刪除留言 | 需要 |
| GET | `/api/messages/stats` | 留言統計 | 需要 |
| GET | `/api/profile` | 個人資料 | 不需要 |
| PUT | `/api/profile` | 更新資料 | 需要 |

## License

MIT
