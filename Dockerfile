FROM python:3.11-slim

WORKDIR /app

# 安裝圖片處理所需的系統依賴 (OpenCV 等可能需要)
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 預先建立圖片存放目錄
RUN mkdir -p uploads results

EXPOSE 8000