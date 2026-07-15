from databricks.sdk import WorkspaceClient
import os
ws = WorkspaceClient(
    host = 'dbc-c44b4dd7-5f31.cloud.databricks.com',
    token = os.getenv("DATBRICKS_API_KEY")
)
job_trigger = ws.jobs.run_now(job_id=988589484506012)

while True:
    job_run = ws.jobs.get_run(job_trigger.run_id)
    if job_run.state.life_cycle_state in ["TERMINATED", "SKIPPED", "INTERNAL_ERROR"]: pass