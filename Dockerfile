FROM python:3.12-slim

WORKDIR /app

# 安装系统字体（解决图片中文水印乱码问题，网络工程师注意，这一步很关键）
RUN apt-get update && apt-get install -y fonts-wqy-zenhei && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 设置时区
ENV TZ=Asia/Shanghai
ENV PROJECT_NAME="Office-Automation"

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]