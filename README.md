# Office Automation API

# TODO

- 🚧 **文件名包含"&"会导致功能异常**
- 🚧 **Word 文档加水印**
- 🚧 **PDF水印乱码**
- 🚧 **定义层与调用层的拆分**

## READY

- ✅ **图片加水印 (PNG/JPG)**
- ✅ **PDF 每页自动加水印 (居中)**

- ✅ **匿名即焚墙**
    - ✅ **基于 Redis 的消息存储**：240秒（4分钟）自动物理销毁。
    - ✅ **安全防护**：基于真实 IP 的频率限制（4分钟内限发一条）。
    - ✅ **特权管理**：管理员令牌支持（可无视限速与手动删帖）。

## 快速启动(本项目 Nginx 默认开启 HTTPS)

1启动服务：

```bash
git clone [https://github.com/wongyiuming/my_FastAPI.git](https://github.com/wongyiuming/my_FastAPI.git)
cd my_FastAPI
docker compose up -d
```

2环境变量
参考 `.env.example` 进行配置。

```bash
nano .env
```

3本地测试:

```bash
WEB_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' office_automation_web)
echo "Web Container IP: $WEB_IP"
curl http://$WEB_IP:8000
```

## ⚠️ Windows 部署注意事项（LTSC / Server 版本）

如果你在 **Windows LTSC** 或 **精简系统（如 Server Core）** 上运行该项目，请务必先安装：

👉 [Microsoft Visual C++ Redistributable (x64)](https://aka.ms/vs/17/release/vc_redist.x64.exe)

否则，`pymupdf`（即 `fitz`）模块会报错：