import os
import sys
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api.v1.endpoints import router as api_v1_router

app = FastAPI(title="Office Automation Service")

# 1. 统一挂载总路由
app.include_router(api_v1_router, prefix="/api/v1")

# 2. 计算并挂载媒体文件目录（供音视频播放器读取）
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEDIA_DIR = os.path.join(BASE_DIR, "data", "media")

os.makedirs(MEDIA_DIR, exist_ok=True)
app.mount("/static/media", StaticFiles(directory=MEDIA_DIR), name="media")

# 3. 原有静态资源处理
static_path = os.path.join(BASE_DIR, "app", "static")
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.get("/wall", include_in_schema=False)
async def read_wall_index():
    return FileResponse(os.path.join(static_path, "index.html"))

@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Welcome to Office Automation Service. Go to /docs for API testing."}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)