# PixelPress

PixelPress 是一個基於 **FastAPI**、**Celery** 與 **Redis** 構建的高效能分散式大量圖片處理系統。它採用「生產者-消費者」架構，能有效處理大規模圖片上傳與異步加工（如縮圖生成），確保 API 響應不阻塞。



## 核心特性

- **非同步處理**：前端上傳圖片後立即獲得任務 ID，無需等待處理完成。
- **分散式架構**：計算密集型的圖片處理任務由獨立的 Worker 執行，與 API 伺服器解耦。
- **可擴展性**：可透過增加 Worker 容器數量輕鬆達成橫向擴展。
- **即時監控**：整合 Flower 儀表板，掌握任務執行狀態與系統負載。
- **容器化部署**：內建 Docker Compose 配置，一鍵啟動完整開發環境。

## 專案架構

- **FastAPI (Producer)**: 負責接收圖片並派發任務。
- **Redis (Broker/Backend)**: 負責任務調度與儲存處理結果。
- **Celery Worker (Consumer)**: 負責執行 Pillow 影像處理邏輯。
- **Flower**: 提供視覺化任務監控介面。

## 啟動專案
‵‵
docker-compose up -d --scale worker=3
‵‵