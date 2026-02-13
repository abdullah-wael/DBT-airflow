from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'abdullah wael',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='dbt_dag',
    default_args=default_args,
    description='first dbt pipeline',
    schedule='@daily',
    start_date=datetime(2026, 2, 10),
    catchup=False,
) as dag:

    DBT_PROJECT_DIR = "/opt/airflow/dbt_project/dbt_potgres"
    DBT_PROFILES_DIR = "/opt/airflow/.dbt"

    seed_all_files = BashOperator(
        task_id='seed_all_files',
        bash_command=f'dbt seed --profiles-dir {DBT_PROFILES_DIR} --project-dir {DBT_PROJECT_DIR}'
    )

    run_all_models = BashOperator(
        task_id='run_all_models',
        bash_command=f'dbt run --profiles-dir {DBT_PROFILES_DIR} --project-dir {DBT_PROJECT_DIR}'
    )

    test_all_models = BashOperator(
        task_id='test_all_models',
        bash_command=f'dbt test --profiles-dir {DBT_PROFILES_DIR} --project-dir {DBT_PROJECT_DIR}'
    )

    seed_all_files >> run_all_models >> test_all_models