from airflow.sdk import dag, task

@dag
def orchestrate():

    @task
    def ingest_cdc():
        return "CDC data ingested"
    
    @task.bash
    def source_freshness():
        return "rm -rf /opt/airflow/wallmart_dbt/target && cd /opt/airflow/wallmart_dbt && dbt source freshness"
    
    ingest_cdc() >> source_freshness()
orchectrate_dag = orchestrate()