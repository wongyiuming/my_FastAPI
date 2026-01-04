from fastapi import FastAPI
from app.api.v1.endpoints import router as api_v1_router
import uvicorn
from app.api.v1.wall import router as wall_router
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(title="Office Automation Watermark Service")

# 挂载路由，前缀设为 /api/v1
app.include_router(api_v1_router, prefix="/api/v1", tags=["Watermark"])
app.include_router(wall_router, prefix="/api/v1/wall", tags=["Wall"])

static_path = os.path.join(os.getcwd(), "app", "static")
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.get("/wall", include_in_schema=False)
async def read_wall_index():
    from fastapi.responses import FileResponse
    return FileResponse(os.path.join(static_path, "index.html"))
@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Welcome to Watermark Service. Go to /docs for API testing."}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
