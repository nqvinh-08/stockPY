from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from business_data.etl.pipeline import run

with DAG(
    dag_id="stock_etl",
    start_date=datetime(2026, 1, 1),
    schedule="@daily", #*/1 * * * * : 1 phuts
    catchup=False,
    tags=["stock"]
) as dag:
    run_pipeline = PythonOperator(
        task_id="run_pipeline",
        python_callable=run
    )