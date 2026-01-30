from fastapi import APIRouter, HTTPException, Depends
from app.storage.metadata import get_task_metadata
from app.models.task import TaskStatusResponse
from app.security.auth import verify_api_key

router = APIRouter()


@router.get("/status/{task_id}", response_model=TaskStatusResponse)
async def get_status(
    task_id: str,
    api_key: str = Depends(verify_api_key),
):
    task = await get_task_metadata(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
