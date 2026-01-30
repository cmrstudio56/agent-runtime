from fastapi import APIRouter, BackgroundTasks, Depends
from datetime import datetime
import logging

from app.models.task import TaskRequest, TaskResponse
from app.storage.metadata import store_task_metadata, update_task_status
from app.utils.ids import generate_task_id
from app.utils.timing import async_timer
from app.security.auth import verify_api_key

router = APIRouter()  # 👈 THIS WAS MISSING OR NOT LOADED
logger = logging.getLogger("task-execute")


@router.post("/execute", response_model=TaskResponse)
async def execute_task(
    request: TaskRequest,
    background_tasks: BackgroundTasks,
    api_key: str = Depends(verify_api_key),
):
    task_id = generate_task_id()

    response = TaskResponse(
        task_id=task_id,
        status="queued",
        intent=request.intent,
        action=request.action,
        created_at=datetime.utcnow(),
    )

    await store_task_metadata(task_id, response.dict())

    background_tasks.add_task(
        run_task,
        task_id,
        request,
    )

    return response


async def run_task(task_id: str, request: TaskRequest):
    try:
        async with async_timer() as timer:
            await update_task_status(task_id, "processing")

            # MOCK execution (local proof only)
            result = {
                "intent": request.intent,
                "action": request.action,
                "parameters": request.parameters,
            }

            await update_task_status(
                task_id,
                "completed",
                result=result,
                execution_time=timer.elapsed_ms(),
            )
    except Exception as e:
        await update_task_status(task_id, "failed", error=str(e))
