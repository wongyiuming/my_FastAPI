import os
import time
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, Response
from app.api.v1.endpoints import router as api_v1_router
from starlette.types import ASGIApp, Receive, Scope, Send


app = FastAPI(title="Office Automation Service")

# ----------------- 核心：真实 IP 与请求日志中间件 -----------------
class RealIPLogMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        start_time = time.time()
        headers = dict(scope.get("headers", []))

        x_forwarded_for = headers.get(b"x-forwarded-for", b"").decode("utf-8")
        if x_forwarded_for:
            client_ip = x_forwarded_for.split(",")[0].strip()
        else:
            x_real_ip = headers.get(b"x-real-ip", b"").decode("utf-8")
            if x_real_ip:
                client_ip = x_real_ip
            else:
                client_ip = (
                    scope.get("client")[0] if scope.get("client") else "127.0.0.1"
                )

        proxy_ip = scope.get("client")[0] if scope.get("client") else "127.0.0.1"
        status_code = 200

        async def send_wrapper(message):
            nonlocal status_code
            if message["type"] == "http.response.start":
                status_code = message["status"]
            await send(message)

        try:
            await self.app(scope, receive, send_wrapper)
        finally:
            process_time = (time.time() - start_time) * 1000
            method = scope.get("method", "")
            path = scope.get("path", "")
            print(
                f"[LOG] REAL_IP: {client_ip} | PROXY_IP: {proxy_ip} | "
                f"{method} {path} - {status_code} ({process_time:.2f}ms)"
            )

app.add_middleware(RealIPLogMiddleware)

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