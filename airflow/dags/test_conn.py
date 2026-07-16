from databricks.sdk import WorkspaceClient
from databricks.sdk.service.jobs import RunLifeCycleState, RunResultState

import os
import time
ws = WorkspaceClient(
    host = 'dbc-c44b4dd7-5f31.cloud.databricks.com',
    token = os.getenv("DATBRICKS_API_KEY")
)
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