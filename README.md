cacsh chay :uvicorn main:app --reload


###1.venv (virtual environment)
        python3 -m venv venv (cai moi truong ao)
        source venv/bin/activate (vao moi truong ao)
###2.dotenv
    pip install python-dotenv
###3.request
    pip install requests
###4.pandas
    pip install pandas
###5.clickhouse
    pip install clickhouse-connect
###6. fastapi
    pip install fastapi uvicorn
    pip install pydantic

uvicorn main:app --reload --port 8001 (doi cong)

pip install -r requirements.txt (cai tat ca thu vien)