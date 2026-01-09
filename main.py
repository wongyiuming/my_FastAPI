import os
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api.v1.endpoints import router as api_v1_router

app = FastAPI(title="Office Automation Service")

# 1. 统一挂载总路由即可，wall 路由已经在 api_v1_router 内部包含了
app.include_router(api_v1_router, prefix="/api/v1")

# 2. 静态资源处理
static_path = os.path.join(os.getcwd(), "app", "static")
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.get("/wall", include_in_schema=False)
async def read_wall_index():
    # 直接返回静态 index.html
    return FileResponse(os.path.join(static_path, "index.html"))

@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Welcome to Office Automation Service. Go to /docs for API testing."}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)