# PixelPress

PixelPress 是一個基於 **FastAPI**、**Celery**、**RabbitMQ** 與 **Redis** 構建的高效能分散式影像處理系統。採用「生產者-消費者」架構，專為大規模圖片非同步加工（如縮圖生成、影像辨識等）設計，確保 API 高可用性且不阻塞。

---

## 核心特性

- **專業消息隊列**：採用 RabbitMQ (AMQP) 確保任務在傳輸過程中不遺失，具備高可靠性。
- **非同步任務解耦**：前端上傳圖片後立即獲得 `task_id`，影像運算由後端 Worker 群組非同步完成。
- **負載平衡優化**：預設關閉任務預取（Prefetching），確保任務均勻分配，避免長任務阻塞短任務。
- **即時監控系統**：整合 Flower 與 RabbitMQ 管理介面，掌握任務狀態與系統負載。
- **容器化部署**：內建 Docker Compose 配置，一鍵啟動完整開發環境。

---

## 專案架構

- **FastAPI (Producer)**: 負責接收圖片並派發任務至 RabbitMQ。
- **RabbitMQ (Broker)**: 專業級訊息代理人，負責高可靠的任務調度與路由。
- **Celery Worker (Consumer)**: 負責執行 Pillow 影像處理邏輯。
- **Redis (Result Backend)**: 儲存任務執行結果與狀態，供 API 查詢。
- **Flower**: 提供視覺化任務監控介面。

---

## 快速啟動

### 1. 環境需求
請確保已安裝 **Docker**

### 2. 一鍵啟動
執行以下指令來啟動服務，並同時開啟 3 個 Worker 節點以提升處理效能：
```bash
docker-compose up --build --scale worker=3
```

| 服務名稱 | 訪問網址 | 預設帳號/密碼 | 職責說明 |
| :--- | :--- | :--- | :--- |
| **API Docs** | http://localhost:8000/docs | - | 測試圖片上傳與狀態查詢 (Swagger) |
| **RabbitMQ UI** | http://localhost:15672 | `guest` / `guest` | 監控訊息堆積與隊列健康度 |
| **Flower** | http://localhost:5555 | - | 追蹤每個任務的成功、失敗與耗時 |