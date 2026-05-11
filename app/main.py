from fastapi import FastAPI, UploadFile, File
from celery.result import AsyncResult
from app.workers.worker import celery_app, process_image_task
import shutil
import os
import uuid

app = FastAPI(title="PixelPress API")

UPLOAD_DIR = "uploads"
RESULT_DIR = "results"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(RESULT_DIR, exist_ok=True)


@app.post("/upload/")
async def upload_images(files: list[UploadFile] = File(...)):
    task_ids = []

    for file in files:
        # 1. 儲存原始檔案
        file_id = str(uuid.uuid4())
        ext = file.filename.split(".")[-1]
        input_path = os.path.join(UPLOAD_DIR, f"{file_id}.{ext}")
        output_path = os.path.join(RESULT_DIR, f"{file_id}_thumb.{ext}")

        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 2. 將任務發送到 Celery 佇列，立即返回
        task = process_image_task.delay(input_path, output_path)
        task_ids.append({"file": file.filename, "task_id": task.id})

    return {"message": "任務已提交", "tasks": task_ids}


@app.get("/status/{task_id}")
async def get_status(task_id: str):
    """
    前端可以透過這個接口查詢圖片處理進度
    """
    task_result = AsyncResult(task_id, app=celery_app)
    return {
        "task_id": task_id,
        "status": task_result.status,  # PENDING, PROGRESS, SUCCESS
        "result": task_result.result if task_result.ready() else None,
    }
