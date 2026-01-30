TASKS = {}


async def store_task_metadata(task_id: str, data: dict):
    TASKS[task_id] = data


async def get_task_metadata(task_id: str):
    return TASKS.get(task_id)


async def update_task_status(
    task_id: str,
    status: str,
    result=None,
    error=None,
    execution_time=None,
):
    task = TASKS.get(task_id, {})
    task.update(
        {
            "task_id": task_id,
            "status": status,
            "result": result,
            "error": error,
            "execution_time_ms": execution_time,
        }
    )
    TASKS[task_id] = task
