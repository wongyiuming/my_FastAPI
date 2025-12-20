from fastapi import FastAPI
from app.api.v1.endpoints import router as api_v1_router
import uvicorn

app = FastAPI(title="Office Automation Watermark Service")

# 挂载路由，前缀设为 /api/v1
app.include_router(api_v1_router, prefix="/api/v1", tags=["Watermark"])

@app.get("/")
async def root():
    return {"message": "Welcome to Watermark Service. Go to /docs for API testing."}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)