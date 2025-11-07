# 使用 Python 3.11 官方映像（slim 版本體積更小）
FROM python:3.11-slim

# 設定環境變數
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# 設定工作目錄
WORKDIR /app

# 安裝系統依賴（如果需要編譯某些 Python 套件）
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 複製依賴檔案並安裝
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製專案檔案
COPY . .

# 暴露 8000 port
EXPOSE 8000

# 啟動 Django 開發伺服器
# 注意：0.0.0.0 讓容器外部可以訪問
CMD ["python", "mysite/manage.py", "runserver", "0.0.0.0:8000"]
