# Office Automation API
# TODO
文件名中含有and连接符"&"会导致异常,计划后续修复

## 核心功能
- [x] 图片加水印 (PNG/JPG)
- [x] PDF 每页自动加水印 (居中)
- [x] Word 文档页眉自动加水印
- [x] 匿名即焚墙
  - [x] 基于 Redis 的消息存储，240秒（4分钟）自动物理销毁。
  - [x] 基于真实 IP 的频率限制（4分钟内限发一条）。
  - [x] 管理员令牌支持（可无视限速与手动删帖）。 

## 快速启动
1. 安装依赖：`pip install .`
2. 启动服务：`uvicorn main:app --reload`
3. 接口文档：`http://127.0.0.1:8000/docs`

## 环境变量
参考 `.env.example` 进行配置。

## ⚠️ Windows 部署注意事项（LTSC / Server 版本）

如果你在 **Windows LTSC** 或 **精简系统（如 Server Core）** 上运行该项目，请务必先安装：

👉 [Microsoft Visual C++ Redistributable (x64)](https://aka.ms/vs/17/release/vc_redist.x64.exe)

否则，`pymupdf`（即 `fitz`）模块会报错：