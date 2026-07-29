from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

from load.load_clickhouse import sync

with DAG(
    dag_id="sync_pg_clickhouse",
    start_date=datetime(2026,1,1),
    schedule="0 8 * * *",
    catchup=False,
):
    PythonOperator(
        task_id="sync",
        python_callable=sync
    )