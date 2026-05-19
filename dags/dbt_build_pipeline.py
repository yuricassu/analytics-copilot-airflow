from cosmos import DbtTaskGroup, ProjectConfig, ProfileConfig, ExecutionConfig
from cosmos.profiles import DatabricksTokenProfileMapping

from airflow import DAG
from airflow.operators.empty import EmptyOperator

from datetime import datetime

with DAG(
    dag_id="dbt_build_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["dbt", "databricks", "analytics"]
) as dag:

    start = EmptyOperator(task_id="start")

    dbt_run = DbtTaskGroup(
        group_id="dbt_build",

        project_config=ProjectConfig(
            "/usr/local/airflow/include/dbt"
        ),

        profile_config=ProfileConfig(
            profile_name="analytics_copilot",
            target_name="dev",

            profile_mapping=DatabricksTokenProfileMapping(
                conn_id="databricks_default",
                profile_args={
                    "schema": "silver",
                    "catalog": "analytics_copilot",
                }
            ),
        ),

        execution_config=ExecutionConfig(
            dbt_executable_path="/usr/local/bin/dbt",
        ),
    )

    end = EmptyOperator(task_id="end")

    start >> dbt_run >> end