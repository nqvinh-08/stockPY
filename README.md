## Project description

    Du an thuc hanh quan ly dlieu stock lam bang python:
    - CRUD API
    - system(docker)
    - auth (JWT)
    - data analysis(find: fromdate --> todate)
## Tech Stack

    - Backend: Python(FastAPI)
    - Database: ClickHouse
    - Container: Docker, Docker Compose
    - Frontend: HTML, JS
    - Authentication: JWT(cookie)

## Project Structure

    project/  
        api/
        │    ├── config/database.py      → kết nối ClickHouse
        │    ├── models/                 → định nghĩa bảng (user, stock)
        │    ├── schemas/                → Pydantic schema (validate request/response)
        │    ├── services/stock_service.py → logic: query DB, hash password...
        │    ├── router/stock_router.py  → định nghĩa API endpoints (/login, /stocks...)
        │    └── main.py                 → khởi động FastAPI, gắn router
        │
        app/
        │    ├── views/                  → HTML templates (Jinja2)
        │    │   ├── login.html
        │    │   ├── register.html
        │    │   └── index.html
        │    ├── static/script.js        → JS chạy trên browser
        │    ├── router/stock_router.py  → nhận request từ browser, gọi sang api
        │    └── main.py                 → khởi động FastAPI, gắn router
        │
        ├── dockerfile.app/         # cach build app
        ├── dockerfile.api/         # cach build api
        ├── docker-compose.yml      # he thong
        ├── requirements.txt        # thu vien
        ├── .env.example/           # bien moi truong


## Features

    ### 1.CRUD API
    ### 2.Authentication(JWT)
        + Register User
        + Login User
        + Tao JWT token
        + Luu vao cookie
        + Het han token
    ### 3.Data Analysis
        + query stock: fromDate --> toDate
    ### 4.Docker System
        + Container he thong
        + chay dong bo API + Database

## Installation

    ### 1. Clone project
        git clone https://github.com/nqvinh-08/stockPY.git
    ### 2. Cau hinh env

    #### Cach chay bang docker:
        ### 1. Run with Docker
            docker compose up --build
            docker compose up -d --build(chay nen)
        ### 2.Stop with Docker
            docker compose down

    #### Cach chay local:
        ### 1. Install dependencies
            pip install -r requirements.txt
        ### 2. Setup virtual environment
            python3 -m venv venv
            source venv/bin/activate (join venv)
        ### 3. lenh chay:
            uvicorn main:app --host 0.0.0.0 --port 8000 



