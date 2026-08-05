import os
import time
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, Response
from app.api.v1.endpoints import router as api_v1_router

app = FastAPI(title="Office Automation Service")

# ----------------- 核心：真实 IP 与请求日志中间件 -----------------
@app.middleware("http")
async def log_requests_with_real_ip(request: Request, call_next):
    # 优先解析 Nginx 传过来的 X-Forwarded-For
    x_forwarded_for = request.headers.get("X-Forwarded-For")
    if x_forwarded_for:
        # 格式为 "client_ip, proxy1, proxy2"，取第一个即为真实客户端 IP
        client_ip = x_forwarded_for.split(",")[0].strip()
    else:
        # 兜底读取 X-Real-IP 或 直连的客户端 IP
        client_ip = request.headers.get("X-Real-IP", request.client.host if request.client else "127.0.0.1")

    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000

    # 同时打印真实公网 IP (REAL_IP) 和 上游代理 IP (PROXY_IP)
    proxy_ip = request.client.host if request.client else "127.0.0.1"
    print(
        f"[LOG] REAL_IP: {client_ip} | PROXY_IP: {proxy_ip} | "
        f"{request.method} {request.url.path} - {response.status_code} ({process_time:.2f}ms)"
    )

    return response


app.include_router(api_v1_router, prefix="/api/v1")

FAVICON_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FAVICON_PATH = os.path.join(FAVICON_BASE_DIR, "static", "favicon.ico")

@app.get("/favicon.ico", include_in_schema=False)
def get_favicon():
    if os.path.exists(FAVICON_PATH):
        return FileResponse(FAVICON_PATH)
    return Response(status_code=204)

@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Welcome to Office Automation Service. Go to /docs for API testing."}

if __name__ == "__main__":
    # 注意：添加了 proxy_headers=True 和 forwarded_allow_ips="*" 参数
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        proxy_headers=True,
        forwarded_allow_ips="*"
    )