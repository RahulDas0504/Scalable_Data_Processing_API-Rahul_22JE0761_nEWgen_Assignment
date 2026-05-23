from concurrent.futures import (
    ThreadPoolExecutor
)

from fastapi import FastAPI

import uuid

from core.join_engine import (
    execute_large_scale_join
)

service = FastAPI()

executor = ThreadPoolExecutor(
    max_workers=4
)

task_store = {}


def process_task(task_id):

    task_store[task_id] = "running"

    execute_large_scale_join(
        final_output=
        f"outputs/result_{task_id}.csv"
    )

    task_store[task_id] = "completed"


@service.post("/start-processing")
async def start_processing():

    task_id = str(uuid.uuid4())

    task_store[task_id] = "queued"

    executor.submit(
        process_task,
        task_id
    )

    return {
        "task_id": task_id,
        "status": "accepted"
    }