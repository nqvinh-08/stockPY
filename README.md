## Project description

    Du an thuc hanh lam bang python:
    - CRUD API
    - system(docker)
    - auth (JWT)
    - data analysis(find: fromdate --> todate)
## Tech Stack

    - Backend: Python(FastAPI)
    - Database: ClickHouse
    - Container: Docker, Docker Compose
    - Frontend: HTML, JS
## Project Structure

    project/
    |   
    │── api/                # api
    │── models/             # cau truc cua db
    │── static/             # js,css
    │── config/             # lien ket db
    │
    ├── schemas/            #
    │
    ├── services/           # logic
    │
    ├── views/              # FE(html)
    ├── dockerfile/         # cach buil app
    ├── docker-compose.yml  # he thong
    ├── requirements.txt    # thu vien
    └── main.py             # app     
## Installation

    ### 1. Clone project
        git clone https://github.com/nqvinh-08/stockPY.git
    ### 2. Install dependencies
        pip install -r requirements.txt
    ### 3. Setup virtual environment
        python3 -m venv venv
        source venv/bin/activate (join venv)
    ### 4. Run with Docker
        docker compose up --build
        docker compose up -d --build(chay nen)
    ### 5.Stop with Docker
        docker compose down

