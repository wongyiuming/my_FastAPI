# Office Automation API

# TODO

- 🚧 **文件名包含"&"会导致功能异常**
- 🚧 **Word 文档加水印**
- 🚧 **PDF水印乱码**
- 🚧 **定义层与调用层的拆分**
- 🚧 **to_English**
- 🚧 **播放积分制**

## READY

- ✅ **图片加水印 (PNG/JPG)**
- ✅ **PDF 每页自动加水印 (居中)**

- ✅ **匿名即焚墙**
    - ✅ **基于 Redis 的消息存储**：240秒（4分钟）自动物理销毁。
    - ✅ **安全防护**：基于真实 IP 的频率限制（4分钟内限发一条）。
    - ✅ **特权管理**：管理员令牌支持（可无视限速与手动删帖）。



1启动服务：

```bash
git clone https://github.com/wongyiuming/my_FastAPI.git
cd my_FastAPI
docker compose down && docker compose up -d --build
```

2环境变量
参考 `.env.example` 进行配置。


3更新
```bash
git pull https://github.com/wongyiuming/my_FastAPI.git
docker compose down && docker compose up -d --build
```


## ⚠️ Windows 部署注意事项（LTSC / Server 版本）

如果你在 **Windows LTSC** 或 **精简系统（如 Server Core）** 上运行该项目，请务必先安装：

👉 [Microsoft Visual C++ Redistributable (x64)](https://aka.ms/vs/17/release/vc_redist.x64.exe)

否则，`pymupdf`（即 `fitz`）模块会报错：

关于自我
我发现自己很容易被外部因素左右，最开始的动机是听歌，后面发现有GFW的存在听不了，当时电脑只会开机，开始自学计网方向，发现方向错了，转全栈，
接触到xray-core sing-box ng mysql redis ，然后python，pd requests  async到现在的FastAPI，
我应该没那么喜欢耀明的，但是共产党非要搞他，或许是从他身上看到自己的影子，亦或是为自己不平，
总之走到现在了，3年前的梦到今天超额实现了，不知道这3年怎么过来的，
99%的人烂尾了我带着仇恨撑到现在，感觉自己心理有问题，
我是不是报复心理特别强，我到底怎么了，为了听歌付出自己的全部吗，
我为什么会因为共针对耀明而爱上耀明呢，这是我的想法么，我好容易被左右，最近越来越心烦了

在本地“多提交”；推送频率取决于你的工作模式。
粒度小，易回滚：当出现 Bug 时，你可以精确撤销某一次微小的修改，而不是回滚整天的代码。
思路清晰：一次提交只做一件事（例如：修改了一个 Bug，或者新增了一个 API 字段）。
方便 Code Review：别人（或你自己以后）看代码变更时不会迷失在成千上万行的改动中。
多久推送 (Push) 一次？
个人独立开发：建议完成一个阶段性功能或一天下班前推送（即“多提交，一次推送”）。
这样既能避免向远程服务频繁触发 CI/CD 自动化构建，又能起到远程备份的作用，防止本地硬盘损坏。
二、 Commit 前缀：feat 及 Conventional Commits 规范
你提到的“f 开头的单词”是 feat（Feature 的缩写，意为“新功能”）。
目前业界最通用的提交规范叫 Conventional Commits（约定式提交）。它的核心格式是：
Plaintext

<type>: <描述信息>
常见的 Type（类型）前缀：
前缀全称含义与适用场景示例featFeature新增功能（最常用）
feat
fix
docs
refactor
style
perf
test
chore

三、 其他必须掌握的 Git 核心规范
1. 分支命名规范 (Branch Naming)
main / master：主分支，保持绝对稳定，随时可部署上线。
feature/xxx：新功能开发分支（例：feature/audio-cache）。
fix/xxx 或 bugfix/xxx：Bug 修复分支（例：fix/cors-issue）。
2. .gitignore 规范
永远不要把敏感信息推送到仓库：.env、配置文件中的密码、API 密钥、数据库连接串必须放入 .gitignore。
不要推动态生成的文件：__pycache__/、.venv/、日志文件（*.log）、编译中间产物等。
3. 提交信息 (Commit Message) 写作小技巧
用动词开头：如 add、fix、update、remove。
简明扼要：首行控制在 50-72 个字符以内，说明改了什么，而不是怎么写的。
保持一致性：全项目要么统一用英文，要么统一用中文（例：feat: 新增音频分片切片支持）。