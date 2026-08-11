FROM stock-python-base

WORKDIR /app

COPY app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn","main_app:app","--host","0.0.0.0","--port","8000"]   