    FROM python:3.12
    WORKDIR /app
    COPY app/requirements.txt .
    RUN pip install -r requirements.txt
    COPY app/ .
    EXPOSE 8000
    CMD ["uvicorn", "main_app:app", "--host", "0.0.0.0", "--port", "8000"]
