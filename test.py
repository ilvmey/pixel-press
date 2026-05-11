import requests

# 假設你有一張測試圖 test.jpg
url = "http://localhost:8000/upload/"
files = [('files', open('test.jpg', 'rb')) for _ in range(500)] # 模擬一次傳500張

response = requests.post(url, files=files)
print(response.json())