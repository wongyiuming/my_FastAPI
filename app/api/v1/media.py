import os
import sys
import json
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

# ----------------- 环境与路径初始化 -----------------
if sys.platform.startswith("win"):
    # app/api/v1/media.py -> 向上退4层到达项目根目录
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    MEDIA_DIR = os.path.join(BASE_DIR, "data", "media")
else:
    MEDIA_DIR = "/data/media"

os.makedirs(MEDIA_DIR, exist_ok=True)

AUDIO_EXTS = ('.mp3', '.m4a', '.flac', '.wav')
VIDEO_EXTS = ('.mp4', '.webm', '.mkv')


def scan_media_files(valid_exts, media_type):
    """扫描指定扩展名的媒体文件"""
    media_list = []
    for root, dirs, files in os.walk(MEDIA_DIR):
        for file in files:
            if file.lower().endswith(valid_exts):
                relative_path = os.path.relpath(os.path.join(root, file), MEDIA_DIR)
                url_friendly_path = relative_path.replace(chr(92), '/')

                media_list.append({
                    "title": os.path.splitext(file)[0],
                    "artist": "私有云端",
                    "type": media_type,
                    "url": f"/static/media/{url_friendly_path}",
                    "cover": "https://api.dujin.org/pic/"
                })
    return media_list


# ----------------- 路由 1: 媒体导航首页 (/media/) -----------------
@router.get("/", response_class=HTMLResponse)
@router.get("", response_class=HTMLResponse)
def get_media_index_page():
    html_content = """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>私有媒体中心</title>
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; }
            body { background: #121212; color: #fff; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
            .container { text-align: center; max-width: 600px; width: 90%; }
            h1 { font-size: 2rem; margin-bottom: 2rem; letter-spacing: 1px; color: #f5f5f5; }
            .card-grid { display: flex; gap: 20px; justify-content: center; }
            .card { flex: 1; background: #1e1e1e; border: 1px solid #2d2d2d; border-radius: 12px; padding: 40px 20px; text-decoration: none; color: #fff; transition: transform 0.2s, background 0.2s; }
            .card:hover { transform: translateY(-5px); background: #282828; }
            .card-icon { font-size: 48px; margin-bottom: 12px; }
            .card-title { font-size: 1.25rem; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>特斯拉私有媒体中心</h1>
            <div class="card-grid">
                <a href="/api/v1/media/music" class="card">
                    <div class="card-icon">🎵</div>
                    <div class="card-title">音频播放</div>
                </a>
                <a href="/api/v1/media/video" class="card">
                    <div class="card-icon">🎬</div>
                    <div class="card-title">视频播放</div>
                </a>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content


# ----------------- 通用播放器模板函数 -----------------
def generate_player_html(media_list, page_title):
    media_json_str = json.dumps(media_list, ensure_ascii=False)
    return f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>{page_title}</title>
        <style>
            * {{ box-sizing: border-box; }}
            body {{ background-color: #0f0f0f; color: #fff; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 0; padding: 0; display: flex; height: 100vh; overflow: hidden; touch-action: manipulation; }}
            .player-section {{ flex: 3; background: #000; position: relative; display: flex; flex-direction: column; justify-content: center; align-items: center; overflow: hidden; }}
            .artplayer-app {{ width: 100%; height: 100%; position: absolute; top: 0; left: 0; }}
            .audio-cover-container {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: none; justify-content: center; align-items: center; background-size: cover; background-position: center; z-index: 1; pointer-events: none; }}
            .audio-blur-bg {{ position: absolute; width: 100%; height: 100%; background-size: cover; background-position: center; filter: blur(40px) brightness(0.4); transform: scale(1.1); }}
            .audio-disk {{ width: 250px; height: 250px; border-radius: 50%; border: 8px solid rgba(255,255,255,0.1); box-shadow: 0 10px 40px rgba(0,0,0,0.6); z-index: 2; background-size: cover; background-position: center; }}
            .rotate-disk {{ animation: rotate 20s linear infinite; }}
            @keyframes rotate {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(360deg); }} }}
            .sidebar {{ flex: 1; min-width: 280px; background: #181818; border-left: 1px solid #282828; display: flex; flex-direction: column; z-index: 10; }}
            .sidebar-header {{ padding: 20px; font-size: 18px; font-weight: bold; border-bottom: 1px solid #282828; display: flex; justify-content: space-between; align-items: center; background: #181818; }}
            .back-btn {{ color: #888; text-decoration: none; font-size: 14px; }}
            .back-btn:hover {{ color: #fff; }}
            .media-list {{ flex: 1; overflow-y: auto; list-style: none; margin: 0; padding: 0; -webkit-overflow-scrolling: touch; touch-action: pan-y; }}
            .media-item {{ display: flex; align-items: center; padding: 15px; border-bottom: 1px solid #222; cursor: pointer; transition: background 0.2s; user-select: none; }}
            .media-item:hover {{ background: #282828; }}
            .media-item.active {{ background: #333; border-left: 4px solid #3498db; }}
            .media-item img {{ width: 50px; height: 50px; border-radius: 6px; margin-right: 15px; object-fit: cover; pointer-events: none; }}
            .media-info {{ flex: 1; overflow: hidden; }}
            .media-title {{ font-size: 14px; font-weight: 500; margin-bottom: 4px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
            .media-artist {{ font-size: 12px; color: #888; }}
        </style>
    </head>
    <body>
        <div class="player-section">
            <div id="audioCover" class="audio-cover-container">
                <div id="audioBlurBg" class="audio-blur-bg"></div>
                <div id="audioDisk" class="audio-disk"></div>
            </div>
            <div id="artplayer" class="artplayer-app"></div>
        </div>
        <div class="sidebar">
            <div class="sidebar-header">
                <span>{page_title}</span>
                <a href="/api/v1/media" class="back-btn">← 返回首页</a>
            </div>
            <ul id="mediaList" class="media-list"></ul>
        </div>

        <script src="https://cdnjs.cloudflare.com/ajax/libs/artplayer/5.1.1/artplayer.js"></script>
        <script>
            let art = null;
            let currentIndex = 0;
            const currentMediaList = {media_json_str};

            // 注册 MediaSession 向特斯拉 OS 汇报曲目元数据并接收硬件按键
            function updateMediaSession(media) {{
                if ('mediaSession' in navigator) {{
                    navigator.mediaSession.metadata = new MediaMetadata({{
                        title: media.title || '未知曲目',
                        artist: media.artist || '私有云端',
                        album: '{page_title}',
                        artwork: [
                            {{ src: media.cover, sizes: '512x512', type: 'image/png' }}
                        ]
                    }});

                    navigator.mediaSession.setActionHandler('play', () => {{
                        if (art) art.play();
                    }});
                    navigator.mediaSession.setActionHandler('pause', () => {{
                        if (art) art.pause();
                    }});
                    navigator.mediaSession.setActionHandler('previoustrack', () => {{
                        playPrev();
                    }});
                    navigator.mediaSession.setActionHandler('nexttrack', () => {{
                        playNext();
                    }});
                }}
            }}

            function playNext() {{
                if (!currentMediaList || currentMediaList.length === 0) return;
                const nextIndex = (currentIndex + 1) % currentMediaList.length;
                selectMedia(nextIndex);
            }}

            function playPrev() {{
                if (!currentMediaList || currentMediaList.length === 0) return;
                const prevIndex = (currentIndex - 1 + currentMediaList.length) % currentMediaList.length;
                selectMedia(prevIndex);
            }}

            function initPlayer(media, index) {{
                currentIndex = index;
                const isAudio = media.type === 'audio';
                const audioCover = document.getElementById('audioCover');
                const audioDisk = document.getElementById('audioDisk');
                const audioBlurBg = document.getElementById('audioBlurBg');

                if (isAudio) {{
                    audioCover.style.display = 'flex';
                    audioDisk.style.backgroundImage = `url('${{media.cover}}')`;
                    audioBlurBg.style.backgroundImage = `url('${{media.cover}}')`;
                }} else {{
                    audioCover.style.display = 'none';
                }}

                if (art) {{
                    art.switchUrl(media.url).then(() => {{
                        art.title = media.title;
                        art.play();
                        if (isAudio) {{
                            audioDisk.classList.add('rotate-disk');
                        }} else {{
                            audioDisk.classList.remove('rotate-disk');
                        }}
                        updateMediaSession(media);
                    }}).catch(() => {{
                        art.url = media.url;
                        art.play();
                        updateMediaSession(media);
                    }});
                    return;
                }}

                art = new Artplayer({{
                    container: '#artplayer',
                    url: media.url,
                    title: media.title,
                    volume: 0.7,
                    autoplay: true,
                    autoSize: true,
                    fullscreen: true,
                    fullscreenWeb: true,
                }});

                art.on('play', () => {{
                    if (media.type === 'audio') audioDisk.classList.add('rotate-disk');
                    if ('mediaSession' in navigator) navigator.mediaSession.playbackState = 'playing';
                }});

                art.on('pause', () => {{
                    audioDisk.classList.remove('rotate-disk');
                    if ('mediaSession' in navigator) navigator.mediaSession.playbackState = 'paused';
                }});

                // 自动连播功能
                art.on('ended', () => {{
                    playNext();
                }});

                updateMediaSession(media);
            }}

            window.addEventListener('DOMContentLoaded', () => {{
                const listContainer = document.getElementById('mediaList');
                if (currentMediaList.length === 0) {{
                    listContainer.innerHTML = '<li style="padding:20px;color:#666;text-align:center;">暂无媒体数据</li>';
                    return;
                }}

                listContainer.innerHTML = currentMediaList.map((item, index) => `
                    <li class="media-item ${{index === 0 ? 'active' : ''}}" onclick="selectMedia(${{index}})">
                        <img src="${{item.cover}}" alt="cover">
                        <div class="media-info">
                            <div class="media-title">${{item.title}}</div>
                            <div class="media-artist">${{item.artist}}</div>
                        </div>
                    </li>
                `).join('');

                initPlayer(currentMediaList[0], 0);
            }});

            function selectMedia(index) {{
                const items = document.querySelectorAll('.media-item');
                items.forEach(item => item.classList.remove('active'));

                const targetElement = items[index];
                if (targetElement) {{
                    targetElement.classList.add('active');
                    targetElement.scrollIntoView({{ block: 'nearest', behavior: 'smooth' }});
                }}

                initPlayer(currentMediaList[index], index);
            }}

            // 补充处理部分硬件按键的 keydown 映射
            window.addEventListener('keydown', (e) => {{
                if (e.key === 'ArrowDown' || e.key === 'MediaTrackNext') {{
                    playNext();
                }} else if (e.key === 'ArrowUp' || e.key === 'MediaTrackPrevious') {{
                    playPrev();
                }}
            }});
        </script>
    </body>
    </html>
    """


# ----------------- 路由 2: 音频播放页面 (/media/music) -----------------
@router.get("/music", response_class=HTMLResponse)
def get_music_player_page():
    media_list = scan_media_files(AUDIO_EXTS, "audio")
    return generate_player_html(media_list, "音乐播放器")


# ----------------- 路由 3: 视频播放页面 (/media/video) -----------------
@router.get("/video", response_class=HTMLResponse)
def get_video_player_page():
    media_list = scan_media_files(VIDEO_EXTS, "video")
    return generate_player_html(media_list, "视频播放器")