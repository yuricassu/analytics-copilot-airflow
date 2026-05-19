from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="dbt_build_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["dbt", "analytics"]
) as dag:

    dbt_build = BashOperator(
        task_id="dbt_build",
        bash_command="""
        cd /usr/local/airflow/dbt &&
        dbt build
        """
    )

    dbt_docs = BashOperator(
        task_id="dbt_docs",
        bash_command="""
        cd /usr/local/airflow/dbt &&
        dbt docs generate
        """
    )

    dbt_build >> dbt_docs