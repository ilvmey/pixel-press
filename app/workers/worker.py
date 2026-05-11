from celery import Celery
from PIL import Image
import os
import time
import random


# 設定 Redis 作為 Broker
CELERY_BROKER = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "image_worker",
    broker=CELERY_BROKER,
    backend=CELERY_BROKER,
    include=['app.workers.worker'],
    task_acks_late=True,
    worker_prefetch_multiplier=1,
)


@celery_app.task(name="app.workers.worker.process_image_task")
def process_image_task(file_path: str, output_path: str):
    try:
        num = random.randint(5, 20)
        # 模擬耗時處理 (如影像辨識)
        time.sleep(num)

        with Image.open(file_path) as img:
            # 轉換為縮圖 (128x128)
            img.thumbnail((128, 128))
            img.save(output_path)

        return {"status": "Success", "output": output_path}
    except Exception as e:
        return {"status": "Error", "message": str(e)}
