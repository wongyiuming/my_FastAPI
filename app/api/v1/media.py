import os
import json
from fastapi import APIRouter, Query
from fastapi.responses import HTMLResponse

router = APIRouter()

# ----------------- 环境与路径初始化 -----------------
# 自动定位项目根目录 (app/api/v1/media.py 向上退4层到达项目根目录)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
MEDIA_DIR = os.path.join(BASE_DIR, "data", "media")

os.makedirs(MEDIA_DIR, exist_ok=True)

AUDIO_EXTS = ('.mp3', '.m4a', '.flac', '.wav')
VIDEO_EXTS = ('.mp4', '.webm', '.mkv')


def get_media_categories(media_type, valid_exts):
    """获取指定媒体类型下的分类目录列表"""
    categories = []
    if not os.path.exists(MEDIA_DIR):
        return categories

    for entry in sorted(os.listdir(MEDIA_DIR)):
        full_path = os.path.join(MEDIA_DIR, entry)
        if os.path.isdir(full_path):
            has_files = False
            for root, dirs, files in os.walk(full_path):
                if any(f.lower().endswith(valid_exts) for f in files):
                    has_files = True
                    break
            if has_files:
                categories.append({
                    "name": entry,
                    "url": f"/api/v1/media/{media_type}/category?path={entry}"
                })
    return categories


def scan_media_files_by_category(category_subpath, valid_exts, media_type):
    """扫描指定子分类目录下的媒体文件"""
    target_dir = os.path.normpath(os.path.join(MEDIA_DIR, category_subpath))
    if not target_dir.startswith(os.path.normpath(MEDIA_DIR)):
        return []

    media_list = []
    if os.path.exists(target_dir):
        for root, dirs, files in os.walk(target_dir):
            for file in files:
                if file.lower().endswith(valid_exts):
                    relative_path = os.path.relpath(os.path.join(root, file), MEDIA_DIR)
                    url_friendly_path = relative_path.replace(chr(92), '/')

                    media_list.append({
                        "title": os.path.splitext(file)[0],
                        "artist": "私有云端",
                        "type": media_type,
                        "url": f"/static/media/{url_friendly_path}",
                        "cover": "/favicon.ico"
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
                    <div class="card-title">音频分类</div>
                </a>
                <a href="/api/v1/media/video" class="card">
                    <div class="card-icon">🎬</div>
                    <div class="card-title">视频分类</div>
                </a>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content


# ----------------- 路由 2: 音频分类列表页 (/media/music) -----------------
@router.get("/music", response_class=HTMLResponse)
def get_music_categories_page():
    categories = get_media_categories("music", AUDIO_EXTS)
    return generate_category_list_html(categories, "音频分类目录", "/api/v1/media/music")


# ----------------- 路由 3: 视频分类列表页 (/media/video) -----------------
@router.get("/video", response_class=HTMLResponse)
def get_video_categories_page():
    categories = get_media_categories("video", VIDEO_EXTS)
    return generate_category_list_html(categories, "视频分类目录", "/api/v1/media/video")


# ----------------- 路由 4: 音频播放页面（带分类） -----------------
@router.get("/music/category", response_class=HTMLResponse)
def get_music_player_page(path: str = Query(...)):
    media_list = scan_media_files_by_category(path, AUDIO_EXTS, "audio")
    return generate_player_html(media_list, f"音乐播放 - {path}", "/api/v1/media/music")


# ----------------- 路由 5: 视频播放页面（带分类） -----------------
@router.get("/video/category", response_class=HTMLResponse)
def get_video_player_page(path: str = Query(...)):
    media_list = scan_media_files_by_category(path, VIDEO_EXTS, "video")
    return generate_player_html(media_list, f"视频播放 - {path}", "/api/v1/media/video")


# ----------------- 分类目录选择页面模板函数 -----------------
def generate_category_list_html(categories, page_title, back_url):
    categories_json = json.dumps(categories, ensure_ascii=False)
    return f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{page_title}</title>
        <style>
            * {{ box-sizing: border-box; margin: 0; padding: 0; }}
            body {{ background: #121212; color: #fff; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; display: flex; justify-content: center; align-items: center; min-height: 100vh; }}
            .container {{ text-align: center; max-width: 600px; width: 90%; }}
            .header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem; }}
            h1 {{ font-size: 1.75rem; color: #f5f5f5; }}
            .back-btn {{ color: #888; text-decoration: none; font-size: 14px; }}
            .back-btn:hover {{ color: #fff; }}
            .card-grid {{ display: flex; flex-direction: column; gap: 15px; }}
            .card {{ background: #1e1e1e; border: 1px solid #2d2d2d; border-radius: 10px; padding: 20px; text-decoration: none; color: #fff; display: flex; align-items: center; justify-content: space-between; transition: background 0.2s; }}
            .card:hover {{ background: #282828; }}
            .card-title {{ font-size: 1.1rem; font-weight: bold; }}
            .card-arrow {{ color: #666; font-size: 1.2rem; }}
            .empty {{ color: #666; padding: 40px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>{page_title}</h1>
                <a href="/api/v1/media" class="back-btn">← 返回首页</a>
            </div>
            <div id="categoryGrid" class="card-grid"></div>
        </div>
        <script>
            const categories = {categories_json};
            window.addEventListener('DOMContentLoaded', () => {{
                const grid = document.getElementById('categoryGrid');
                if (categories.length === 0) {{
                    grid.innerHTML = '<div class="empty">暂无分类目录，请在 data/media 下创建子文件夹</div>';
                    return;
                }}
                grid.innerHTML = categories.map(cat => `
                    <a href="${{cat.url}}" class="card">
                        <div class="card-title">📁 ${{cat.name}}</div>
                        <div class="card-arrow">→</div>
                    </a>
                `).join('');
            }});
        </script>
    </body>
    </html>
    """


# ----------------- 通用播放器模板函数 -----------------
def generate_player_html(media_list, page_title, category_list_url):
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
            body {{ background-color: #0f0f0f; color: #fff; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 0; padding: 0; display: flex; height: 100vh; overflow: hidden; touch-action: manipulation; flex-direction: row-reverse; }}
            .player-section {{ flex: 3; background: #000; position: relative; display: flex; flex-direction: column; justify-content: center; align-items: center; overflow: hidden; }}
            .artplayer-app {{ width: 100%; height: 100%; position: absolute; top: 0; left: 0; }}
            .audio-cover-container {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: none; justify-content: center; align-items: center; background-size: cover; background-position: center; z-index: 1; pointer-events: none; }}
            .audio-blur-bg {{ position: absolute; width: 100%; height: 100%; background-size: cover; background-position: center; filter: blur(40px) brightness(0.4); transform: scale(1.1); }}
            .audio-disk {{ width: 250px; height: 250px; border-radius: 50%; border: 8px solid rgba(255,255,255,0.1); box-shadow: 0 10px 40px rgba(0,0,0,0.6); z-index: 2; background-size: cover; background-position: center; }}
            .rotate-disk {{ animation: rotate 20s linear infinite; }}
            @keyframes rotate {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(360deg); }} }}
            .sidebar {{ flex: 1; min-width: 280px; background: #181818; border-right: 1px solid #282828; display: flex; flex-direction: column; z-index: 10; }}
            .sidebar-header {{ padding: 20px; font-size: 16px; font-weight: bold; border-bottom: 1px solid #282828; display: flex; justify-content: space-between; align-items: center; background: #181818; }}
            .back-btn {{ color: #888; text-decoration: none; font-size: 14px; }}
            .back-btn:hover {{ color: #fff; }}
            .player-controls {{ padding: 12px 15px; background: #1f1f1f; display: flex; gap: 10px; border-bottom: 1px solid #282828; }}
            .control-btn {{ flex: 1; background: #2a2a2a; color: #fff; border: 1px solid #3a3a3a; padding: 8px 12px; border-radius: 6px; cursor: pointer; font-size: 13px; font-weight: 500; text-align: center; transition: background 0.2s; user-select: none; }}
            .control-btn:hover {{ background: #3a3a3a; }}
            .media-list {{ flex: 1; overflow-y: auto; list-style: none; margin: 0; padding: 0; -webkit-overflow-scrolling: touch; touch-action: pan-y; }}
            .media-item {{ display: flex; align-items: center; padding: 15px; border-bottom: 1px solid #222; cursor: pointer; transition: background 0.2s; user-select: none; }}
            .media-item:hover {{ background: #282828; }}
            .media-item.active {{ background: #333; border-right: 4px solid #3498db; border-left: none; }}
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
                <span>播放列表</span>
                <a href="{category_list_url}" class="back-btn">← 返回分类</a>
            </div>
            <div class="player-controls">
                <button class="control-btn" onclick="playPrev()">⏮ 上一首</button>
                <button class="control-btn" onclick="playNext()">下一首 ⏭</button>
            </div>
            <ul id="mediaList" class="media-list"></ul>
        </div>

        <script src="https://cdnjs.cloudflare.com/ajax/libs/artplayer/5.1.1/artplayer.js"></script>
        <script>
            let art = null;
            let currentIndex = 0;
            const currentMediaList = {media_json_str};

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

                    navigator.mediaSession.setActionHandler('play', () => {{ if (art) art.play(); }});
                    navigator.mediaSession.setActionHandler('pause', () => {{ if (art) art.pause(); }});
                    navigator.mediaSession.setActionHandler('previoustrack', () => {{ playPrev(); }});
                    navigator.mediaSession.setActionHandler('nexttrack', () => {{ playNext(); }});
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

                // 强制修正：使用原生 video/audio 元素的 ended 绑定来确保自动连播不失效
                art.on('video:ended', () => {{
                    playNext();
                }});

                updateMediaSession(media);
            }}

            window.addEventListener('DOMContentLoaded', () => {{
                const listContainer = document.getElementById('mediaList');
                if (currentMediaList.length === 0) {{
                    listContainer.innerHTML = '<li style="padding:20px;color:#666;text-align:center;">该分类下暂无媒体数据</li>';
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

            window.addEventListener('keydown', (e) => {{
                if (e.key === 'ArrowRight' || e.key === 'MediaTrackNext' || e.code === 'MediaTrackNext') {{
                    e.preventDefault();
                    playNext();
                }} else if (e.key === 'ArrowLeft' || e.key === 'MediaTrackPrevious' || e.code === 'MediaTrackPrevious') {{
                    e.preventDefault();
                    playPrev();
                }}
            }});
        </script>
    </body>
    </html>
    """