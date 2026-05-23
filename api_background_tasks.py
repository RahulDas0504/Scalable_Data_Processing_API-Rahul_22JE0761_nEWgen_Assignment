from fastapi import (
    FastAPI,
    BackgroundTasks
)

import uuid

from core.join_engine import (
    execute_large_scale_join
)

service = FastAPI()

task_store = {}


def process_task(task_id):

    task_store[task_id] = "running"

    execute_large_scale_join(
        final_output=
        f"outputs/result_{task_id}.csv"
    )

    task_store[task_id] = "completed"


@service.post("/start-processing")
async def start_processing(
    background_tasks: BackgroundTasks
):

    task_id = str(uuid.uuid4())

    task_store[task_id] = "queued"

    background_tasks.add_task(
        process_task,
        task_id
    )

    return {
        "task_id": task_id,
        "status": "accepted"
    }


@service.get("/task-status/{task_id}")
async def task_status(task_id: str):

    return {
        "task_id": task_id,
        "status": task_store.get(
            task_id,
            "unknown"
        )
    }