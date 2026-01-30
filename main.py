from fastapi import FastAPI, UploadFile, File
import subprocess
import tempfile
import os
import json
import shutil

app = FastAPI(title="Agent Runtime", version="0.1")

# ✅ FAIL FAST if ffprobe is missing
if not shutil.which("ffprobe"):
    raise RuntimeError("ffprobe (FFmpeg) not found in environment")
    
if not shutil.which("ffmpeg"):
    raise RuntimeError("ffmpeg not found in environment")

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/media/metadata")
async def media_metadata(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        cmd = [
            "ffprobe",
            "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            "-show_streams",
            tmp_path
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )

        return json.loads(result.stdout)

    finally:
        os.unlink(tmp_path)
