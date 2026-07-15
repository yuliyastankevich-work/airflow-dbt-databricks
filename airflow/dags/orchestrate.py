from airflow.sdk import dag, task
from airflow.operators.bash import BashOperator
@dag
def orchestrate():

    @task
    def ingest_cdc():
        return "CDC data ingested"
    
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