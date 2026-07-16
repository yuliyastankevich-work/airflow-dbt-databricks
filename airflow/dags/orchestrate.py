from airflow.sdk import dag, task
from airflow.operators.bash import BashOperator

from databricks.sdk import WorkspaceClient
from databricks.sdk.service.jobs import RunLifeCycleState, RunResultState
import os
import time

@dag
def orchestrate():

    @task
    def ingest_cdc():
        ws = WorkspaceClient(
                    host = 'dbc-c44b4dd7-5f31.cloud.databricks.com',
                    token = os.getenv("DATBRICKS_API_KEY"))
        job_trigger = ws.jobs.run_now(job_id=988589484506012)

        while True:
            job_run = ws.jobs.get_run(job_trigger.run_id)

            print(f"Job run status: {job_run.state.life_cycle_state}\nJob result state: {job_run.state.result_state}")
            if job_run.state.life_cycle_state in [RunLifeCycleState.TERMINATED, RunLifeCycleState.SKIPPED, RunLifeCycleState.INTERNAL_ERROR]:
                if job_run.state.result_state == RunResultState.SUCCESS:
                    print("Job completed successfully")
                    break
                else:
                    raise Exception(f"Job failed with state: {job_run.state.result_state}")
            time.sleep(5)
        return "CDC ingestion completed"
    
    @task.bash
    def clean_target_logs():
        return "rm -rf /opt/airflow/wallmart_dbt/target && rm -rf /opt/airflow/wallmart_dbt/logs"
    
    @task.bash
    def source_freshness():
        return "cd /opt/airflow/wallmart_dbt && dbt source freshness"
    
    silver_tech_task = BashOperator(
        task_id = "silver_tech_task",
        bash_command = "cd /opt/airflow/wallmart_dbt && dbt run --select silver_tech"
    )
    
    silver_tech_tests_task = BashOperator(
        task_id = "silver_tech_test_task",
        bash_command = "cd /opt/airflow/wallmart_dbt && dbt test --select silver_tech"
    )

    silver_business_task = BashOperator(
        task_id = 'silver_business_task',
        bash_command= "cd /opt/airflow/wallmart_dbt && dbt run --select silver"
            )
    
    silver_business_tests_task = BashOperator(
        task_id = "silver_business_tests_task",
        bash_command = "cd /opt/airflow/wallmart_dbt && dbt test --select silver"
    )

    gold_ephemeral_task = BashOperator(
        task_id = 'gold_ephemeral',
        cwd = '/opt/airflow/wallmart_dbt',
        bash_command="dbt run --select gold/ephemeral"
    )

    gold_dimensions_task = BashOperator(
        task_id = 'gold_dimensions_task',
        cwd = '/opt/airflow/wallmart_dbt',
        bash_command='dbt snapshot'
    )

    gold_fact_task = BashOperator(
        task_id = 'gold_fact_task',
        cwd = '/opt/airflow/wallmart_dbt',
        bash_command='dbt run --select gold/fact'
    )
    ingest_cdc() >> clean_target_logs() >> source_freshness() >> silver_tech_task >> silver_tech_tests_task >> silver_business_task >> silver_business_tests_task >> gold_ephemeral_task >> gold_dimensions_task >> gold_fact_task
orchectrate_dag = orchestrate()