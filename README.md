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


[root@DMIT-75JbUfNKch ~]# docker ps

CONTAINER ID   IMAGE                   COMMAND                  CREATED       STATUS      PORTS                                                                          NAMES

9aba3db37846   fatedier/frps:v0.54.0   "/usr/bin/frps -c /e…"   10 days ago   Up 9 days                                                                                  my-frps

6fd51fa5ba3f   nginx:latest            "/docker-entrypoint.…"   2 weeks ago   Up 9 days   0.0.0.0:80->80/tcp, [::]:80->80/tcp, 0.0.0.0:443->443/tcp, [::]:443->443/tcp   nginx-test

[root@DMIT-75JbUfNKch ~]# docker logs -fn 50 6fd51fa5ba3f

8.217.128.31 - - [05/Aug/2026:23:09:09 +0000] "GET /favicon.ico HTTP/1.1" 301 169 "-" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"

8.217.128.31 - - [05/Aug/2026:23:09:34 +0000] "GET /favicon.ico HTTP/1.1" 200 1081043 "-" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"

47.238.250.119 - - [05/Aug/2026:23:10:33 +0000] "GET / HTTP/1.1" 200 80 "-" "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"

47.238.250.119 - - [05/Aug/2026:23:10:59 +0000] "GET /favicon.ico HTTP/1.1" 200 966355 "-" "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"

112.96.175.209 - - [05/Aug/2026:23:12:07 +0000] "GET /api/v1/media/stream?file_path=%E9%95%BF%E6%9B%B2/%E5%BC%A0%E5%B4%87%E5%9F%BA_%E5%BC%A0%E5%B4%87%E5%BE%B7_2SSENTIAL%E6%BC%94%E5%94%B1%E4%BC%9A2006_%E9%AB%98%E6%B8%85%E6%97%A0%E6%8D%9F%E9%9F%B3%E8%B4%A8DVD.mp3 HTTP/1.1" 206 1474238 "https://rust.8nine64.icu/api/v1/media/music/category?path=%E9%95%BF%E6%9B%B2" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.7339.207 Safari/537.36"

195.182.16.23 - - [05/Aug/2026:23:22:44 +0000] "GET /SDK/webLanguage HTTP/1.1" 301 169 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 Edg/90.0.818.46"

85.217.149.18 - - [05/Aug/2026:23:33:31 +0000] "GET / HTTP/1.1" 200 80 "-" "Mozilla/5.0 (compatible; ModatScanner/1.2; +https://modat.io/)"

23.19.230.232 - - [05/Aug/2026:23:37:03 +0000] "GET /cdn-cgi/trace HTTP/1.1" 400 255 "-" "Python/3.11 aiohttp/3.8.4"

168.110.210.99 - - [05/Aug/2026:23:45:02 +0000] "GET /cdn-cgi/trace HTTP/1.1" 404 22 "-" "CFFinderSwiftBackend/1.0"

160.119.69.16 - - [06/Aug/2026:00:18:47 +0000] "GET / HTTP/1.1" 301 169 "-" "Mozilla/5.0"

160.119.69.16 - - [06/Aug/2026:00:18:47 +0000] "GET / HTTP/1.1" 200 80 "-" "Mozilla/5.0"

185.242.226.112 - - [06/Aug/2026:00:19:53 +0000] "\x16\x03\x01\x00\x8C\x01\x00\x00\x88\x03\x03\xD4\xC2\xAD\x9Bpn&Q\x92js\x82\xCFVi\xF8`\xF0\xF8N\x90\xC4\x5C\x8E\xEE\x01\x8C\x18\xB2oO\x89\x00\x00\x1A\xC0/\xC0+\xC0\x11\xC0\x07\xC0\x13\xC0\x09\xC0\x14\xC0" 400 157 "-" "-"

112.96.175.209 - - [06/Aug/2026:00:25:53 +0000] "GET /api/v1/media HTTP/1.1" 200 1637 "-" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.7339.207 Safari/537.36"

112.96.175.209 - - [06/Aug/2026:00:25:55 +0000] "GET /api/v1/media/video HTTP/1.1" 200 2442 "https://rust.8nine64.icu/api/v1/media" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.7339.207 Safari/537.36"

112.96.175.209 - - [06/Aug/2026:00:25:56 +0000] "GET /api/v1/media/video/category?path=b HTTP/1.1" 200 14894 "https://rust.8nine64.icu/api/v1/media/video" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.7339.207 Safari/537.36"

2026/08/06 00:26:42 [error] 21#21: *15357 upstream prematurely closed connection while reading upstream, client: 112.96.175.209, server: rust.8nine64.icu, request: "GET /api/v1/media/stream?file_path=b/Wet_pantyhose_aes_Lindsey_Olsen_Cindy_have_orgasms_while_sucking_toes.mp4 HTTP/1.1", upstream: "http://172.17.0.1:8000/api/v1/media/stream?file_path=b/Wet_pantyhose_aes_Lindsey_Olsen_Cindy_have_orgasms_while_sucking_toes.mp4", host: "rust.8nine64.icu", referrer: "https://rust.8nine64.icu/api/v1/media/video/category?path=b"

112.96.175.209 - - [06/Aug/2026:00:26:42 +0000] "GET /api/v1/media/stream?file_path=b/Wet_pantyhose_aes_Lindsey_Olsen_Cindy_have_orgasms_while_sucking_toes.mp4 HTTP/1.1" 206 9830079 "https://rust.8nine64.icu/api/v1/media/video/category?path=b" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.7339.207 Safari/537.36"

2026/08/06 00:26:42 [error] 21#21: *15362 upstream prematurely closed connection while reading response header from upstream, client: 112.96.175.209, server: rust.8nine64.icu, request: "GET /api/v1/media/stream?file_path=b/Wet_pantyhose_aes_Lindsey_Olsen_Cindy_have_orgasms_while_sucking_toes.mp4 HTTP/1.1", upstream: "http://172.17.0.1:8000/api/v1/media/stream?file_path=b/Wet_pantyhose_aes_Lindsey_Olsen_Cindy_have_orgasms_while_sucking_toes.mp4", host: "rust.8nine64.icu", referrer: "https://rust.8nine64.icu/api/v1/media/video/category?path=b"

112.96.175.209 - - [06/Aug/2026:00:26:42 +0000] "GET /api/v1/media/stream?file_path=b/Wet_pantyhose_aes_Lindsey_Olsen_Cindy_have_orgasms_while_sucking_toes.mp4 HTTP/1.1" 502 559 "https://rust.8nine64.icu/api/v1/media/video/category?path=b" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.7339.207 Safari/537.36"

112.96.175.209 - - [06/Aug/2026:00:28:20 +0000] "GET /api/v1/media/stream?file_path=b/Wet_pantyhose_aes_Lindsey_Olsen_Cindy_have_orgasms_while_sucking_toes.mp4 HTTP/1.1" 206 0 "https://rust.8nine64.icu/api/v1/media/video/category?path=b" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.7339.207 Safari/537.36"

112.96.175.209 - - [06/Aug/2026:00:28:38 +0000] "GET /api/v1/media/video HTTP/1.1" 200 0 "https://rust.8nine64.icu/api/v1/media/video/category?path=b" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.7339.207 Safari/537.36"

112.96.175.209 - - [06/Aug/2026:00:28:40 +0000] "GET /api/v1/media/video HTTP/1.1" 200 0 "https://rust.8nine64.icu/api/v1/media/video/category?path=b" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.7339.207 Safari/537.36"

112.96.175.209 - - [06/Aug/2026:00:28:47 +0000] "GET /api/v1/media/video HTTP/1.1" 200 0 "https://rust.8nine64.icu/api/v1/media/video/category?path=b" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.7339.207 Safari/537.36"

112.96.175.209 - - [06/Aug/2026:00:28:51 +0000] "GET /api/v1/media/video HTTP/1.1" 200 0 "https://rust.8nine64.icu/api/v1/media/video/category?path=b" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.7339.207 Safari/537.36"

112.96.175.209 - - [06/Aug/2026:00:28:55 +0000] "GET /api/v1/media/music HTTP/1.1" 200 0 "https://rust.8nine64.icu/api/v1/media" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.7339.207 Safari/537.36"

112.96.175.209 - - [06/Aug/2026:00:28:58 +0000] "GET /api/v1/media/music HTTP/1.1" 200 2908 "https://rust.8nine64.icu/api/v1/media" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.7339.207 Safari/537.36"

112.96.175.209 - - [06/Aug/2026:00:29:21 +0000] "GET /api/v1/media/music/category?path=%E6%BF%80%E8%BF%9B HTTP/1.1" 200 0 "https://rust.8nine64.icu/api/v1/media/music" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.7339.207 Safari/537.36"

112.96.175.209 - - [06/Aug/2026:00:29:27 +0000] "GET /api/v1/media/music/category?path=%E6%BF%80%E8%BF%9B HTTP/1.1" 200 20370 "https://rust.8nine64.icu/api/v1/media/music" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.7339.207 Safari/537.36"

112.96.175.209 - - [06/Aug/2026:00:29:28 +0000] "GET /api/v1/media/stream?file_path=%E6%BF%80%E8%BF%9B/%E9%BE%8D%E5%A9%B7%E5%B0%8F%E9%BE%8D%E5%A5%B3_%E5%A4%A7%E7%9F%B3%E5%A7%90%E6%99%B6%E6%99%B6_%E5%90%88%E5%94%B1_%E5%AF%B6%E8%B2%9D%E5%B0%8D%E4%B8%8D%E8%B5%B7_%E4%B8%AD%E7%92%B010%E8%99%9F%E7%A2%BC%E9%A0%AD20190525.mp3 HTTP/1.1" 206 7834796 "https://rust.8nine64.icu/api/v1/media/music/category?path=%E6%BF%80%E8%BF%9B" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.7339.207 Safari/537.36"

79.124.49.102 - - [06/Aug/2026:00:29:51 +0000] "GET /auth_portal/Default/logo.gif HTTP/1.1" 400 657 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

79.124.49.102 - - [06/Aug/2026:00:29:51 +0000] "GET /auth_portal/Default/logo.gif HTTP/1.1" 404 0 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

79.124.49.102 - - [06/Aug/2026:00:29:59 +0000] "GET /+CSCOU+/csco_logo.gif HTTP/1.1" 499 0 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

79.124.49.102 - - [06/Aug/2026:00:29:59 +0000] "GET /+CSCOU+/csco_logo.gif HTTP/1.1" 400 657 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

79.124.49.102 - - [06/Aug/2026:00:30:07 +0000] "GET /fonts/ftnt-icons.woff HTTP/1.1" 499 0 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

79.124.49.102 - - [06/Aug/2026:00:30:15 +0000] "GET /auth1.js HTTP/1.1" 400 657 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

79.124.49.102 - - [06/Aug/2026:00:30:16 +0000] "GET /auth1.js HTTP/1.1" 404 0 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

161.35.49.224 - - [06/Aug/2026:00:30:56 +0000] "GET /.git/config HTTP/1.1" 301 169 "-" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"

161.35.49.224 - - [06/Aug/2026:00:31:04 +0000] "GET /.git/config HTTP/1.1" 404 0 "-" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"

112.96.175.209 - - [06/Aug/2026:00:37:50 +0000] "GET /api/v1/media/stream?file_path=%E6%BF%80%E8%BF%9B/%E9%BD%90%E7%A7%A6_%E4%B8%8D%E8%AE%A9%E6%88%91%E7%9A%84%E7%9C%BC%E6%B3%AA%E9%99%AA%E6%88%91%E8%BF%87%E5%A4%9C.mp3 HTTP/1.1" 206 2309828 "https://rust.8nine64.icu/api/v1/media/music/category?path=%E6%BF%80%E8%BF%9B" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.7339.207 Safari/537.36"

199.45.154.123 - - [06/Aug/2026:00:39:15 +0000] "GET / HTTP/1.1" 301 169 "-" "Mozilla/5.0 (compatible; CensysInspect/1.1; +https://about.censys.io/)"

199.45.154.123 - - [06/Aug/2026:00:39:17 +0000] "PRI * HTTP/2.0" 400 157 "-" "-"

199.45.154.123 - - [06/Aug/2026:00:39:19 +0000] "\x16\x03\x01\x00\xEE\x01\x00\x00\xEA\x03\x03H\xC8\x88\xC4\xBE5\xD3\xFE8\x92(;\xD0\xC0\xCA\x9C\xE9!\xF5\x5C~\xCA\x95\xE4\xDE\x8C\xA3v\xFF\xA4\x10\xAA \x8E\xCD\xF3[e\xF2\xA8y\x97t\xD0\x1Bi2\xE5\x98R\xB1ps\x90D\xB1+\xB8a\x82n\x86\xAB\xFB1\x00&\xCC\xA8\xCC\xA9\xC0/\xC00\xC0+\xC0,\xC0\x13\xC0\x09\xC0\x14\xC0" 400 157 "-" "-"

199.45.154.123 - - [06/Aug/2026:00:39:25 +0000] "GET /sitemap.xml HTTP/1.1" 301 169 "-" "Mozilla/5.0 (compatible; CensysInspect/1.1; +https://about.censys.io/)"

199.45.154.123 - - [06/Aug/2026:00:39:29 +0000] "\x16\x03\x01\x00\xEE\x01\x00\x00\xEA\x03\x03\xB8^#\xD3\xD4'0QZ\x06X\xF9\x98\xDE\xC7\xBCV\x11\x1F\x18x\x1D\x81\x00a\xE1\xB17\x8AC\x83\xFD \xEAPw\xE0\xEE\xFA\x80\xF1\x86\x8C\x9Dkg\xAB\xBE\xF5\x1D(\x96\xB3\x91\xCDJQ\xAD\x87\xFERY\xAE\xED\x92\x00&\xCC\xA8\xCC\xA9\xC0/\xC00\xC0+\xC0,\xC0\x13\xC0\x09\xC0\x14\xC0" 400 157 "-" "-"

223.104.164.49 - - [06/Aug/2026:00:41:55 +0000] "GET /api/v1/media/stream?file_path=%E9%95%BF%E6%9B%B2/%E8%AA%B0%E4%BB%A4%E4%BD%A0%E5%BF%83%E7%97%B4_%E7%8F%BE%E4%BB%A3%E6%84%9B%E6%83%85%E6%95%85%E4%BA%8B_%E7%B8%BD%E6%9C%89%E4%BD%A0%E9%BC%93%E5%8B%B5_%E5%80%86%E5%BF%98%E7%85%99%E6%B0%B4%E8%A3%A1_%E7%AC%91%E7%9C%8B%E9%A2%A8%E9%9B%B2%E8%AE%8A_%E6%98%8E%E5%A4%A9%E4%BD%A0%E6%98%AF%E5%90%A6%E4%BE%9D%E7%84%B6%E6%84%9B%E6%88%91_Tonight_I_Celebrate_My_LoveZita_%E8%AC%9D%E9%9C%88%E8%87%BB_R.mp3 HTTP/1.1" 206 0 "https://rust.8nine64.icu/api/v1/media/music/category?path=%E9%95%BF%E6%9B%B2" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36"

223.104.164.49 - - [06/Aug/2026:00:41:55 +0000] "GET /favicon.ico HTTP/1.1" 304 0 "https://rust.8nine64.icu/api/v1/media/music/category?path=%E9%95%BF%E6%9B%B2" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36"

223.104.164.49 - - [06/Aug/2026:00:42:16 +0000] "GET /api/v1/media/stream?file_path=%E9%95%BF%E6%9B%B2/%E5%BC%A0%E5%B4%87%E5%9F%BA%E5%BC%A0%E5%B4%87%E5%BE%B7%E4%BA%8C%E4%BA%BA%E4%B9%8B%E9%87%8D%E5%94%B12002.mp3 HTTP/1.1" 206 21724866 "https://rust.8nine64.icu/api/v1/media/music/category?path=%E9%95%BF%E6%9B%B2" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36"

223.104.164.49 - - [06/Aug/2026:00:42:40 +0000] "GET /api/v1/media/music/category?path=%E9%95%BF%E6%9B%B2 HTTP/1.1" 200 14752 "https://rust.8nine64.icu/api/v1/media/music" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36"

112.96.175.209 - - [06/Aug/2026:00:43:49 +0000] "GET /api/v1/media/stream?file_path=b/Wet_pantyhose_aes_Lindsey_Olsen_Cindy_have_orgasms_while_sucking_toes.mp4 HTTP/1.1" 206 1031866 "https://rust.8nine64.icu/api/v1/media/video/category?path=b" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.7339.207 Safari/537.36"

20.169.105.48 - - [06/Aug/2026:00:46:46 +0000] "GET /ReportServer HTTP/1.1" 301 169 "-" "Mozilla/5.0 zgrab/0.x"

[root@DMIT-75JbUfNKch ~]#