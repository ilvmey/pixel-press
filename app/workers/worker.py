import os
import random
import time
from PIL import Image
from celery import Celery

# 讀取環境變數
BROKER_URL = os.getenv("CELERY_BROKER_URL", "amqp://guest:guest@localhost:5672//")
RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

celery_app = Celery(
    "image_worker",
    broker=BROKER_URL,
    backend=RESULT_BACKEND,
    include=['app.workers.worker']
)

# 專業優化設定
celery_app.conf.update(
    task_acks_late=True,             # 任務執行完才確認，失敗會重啟
    worker_prefetch_multiplier=1,    # 一次只拿一個任務，防止卡死
    task_track_started=True,         # 追蹤任務開始狀態
)

@celery_app.task(name="app.workers.worker.process_image_task", bind=True, max_retries=3)
def process_image_task(self, file_path: str, output_path: str):
    # 這裡放你的 Pillow 處理邏輯
    pass
    try:
        num = random.randint(1, 60)
        # 模擬耗時處理 (如影像辨識)
        time.sleep(num)

        with Image.open(file_path) as img:
            # 轉換為縮圖 (128x128)
            img.thumbnail((128, 128))
            img.save(output_path)

        return {"status": "Success", "output": output_path}
    except Exception as e:
        return {"status": "Error", "message": str(e)}
