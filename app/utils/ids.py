import uuid
from datetime import datetime


def generate_task_id() -> str:
    ts = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    uid = uuid.uuid4().hex[:8]
    return f"task_{ts}_{uid}"
