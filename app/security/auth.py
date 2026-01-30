import os
from fastapi import Header, HTTPException
from typing import Optional

API_KEY = os.getenv("API_KEY", "local-dev-key")


async def verify_api_key(x_api_key: Optional[str] = Header(None)):
    if not x_api_key:
        raise HTTPException(status_code=401, detail="API key required")
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return x_api_key
