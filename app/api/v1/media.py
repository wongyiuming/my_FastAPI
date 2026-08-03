import os
import json
from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import HTMLResponse, FileResponse

router = APIRouter()

# ----------------- 环境与路径初始化 -----------------
# 定位项目根目录 (app/api/v1/media.py 向上退4层)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
MEDIA_DIR = os.path.join(BASE_DIR, "data", "media")
STATIC_MEDIA_DIR = os.path.join(BASE_DIR, "static", "media")

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

                    # 修改：将媒体文件的请求地址指向我们自己写的 API 接口，而不是静态挂载点
                    media_list.append({
                        "title": os.path.splitext(file)[0],
                        "artist": "私有云端",
                        "type": media_type,
                        "url": f"/api/v1/media/stream?file_path={url_friendly_path}",
                        "cover": "/favicon.ico"
                    })
    return media_list


def load_html_template(filename: str) -> str:
    """读取 static/media/ 下的独立 HTML 文件"""
    file_path = os.path.join(STATIC_MEDIA_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"Template {filename} not found in static/media/")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


# ----------------- 路由 0: 媒体文件流式传输接口 -----------------
@router.get("/stream")
def stream_media_file(file_path: str = Query(...)):
    """通过 API 安全读取并返回 data/media 下的媒体文件，支持范围请求（播放/快进）"""
    safe_path = os.path.normpath(os.path.join(MEDIA_DIR, file_path))
    if not safe_path.startswith(os.path.normpath(MEDIA_DIR)) or not os.path.exists(safe_path):
        raise HTTPException(status_code=404, detail="Media file not found")

    return FileResponse(safe_path)


# ----------------- 路由 1: 媒体导航首页 (/media/) -----------------
@router.get("/", response_class=HTMLResponse)
@router.get("", response_class=HTMLResponse)
def get_media_index_page():
    return load_html_template("index.html")


# ----------------- 路由 2: 音频分类列表页 (/media/music) -----------------
@router.get("/music", response_class=HTMLResponse)
def get_music_categories_page():
    categories = get_media_categories("music", AUDIO_EXTS)
    html = load_html_template("category.html")
    html = html.replace("{{PAGE_TITLE}}", "音频分类目录")
    html = html.replace("{{BACK_URL}}", "/api/v1/media")
    html = html.replace("{{CATEGORIES_JSON}}", json.dumps(categories, ensure_ascii=False))
    return html


# ----------------- 路由 3: 视频分类列表页 (/media/video) -----------------
@router.get("/video", response_class=HTMLResponse)
def get_video_categories_page():
    categories = get_media_categories("video", VIDEO_EXTS)
    html = load_html_template("category.html")
    html = html.replace("{{PAGE_TITLE}}", "视频分类目录")
    html = html.replace("{{BACK_URL}}", "/api/v1/media")
    html = html.replace("{{CATEGORIES_JSON}}", json.dumps(categories, ensure_ascii=False))
    return html


# ----------------- 路由 4: 音频播放页面（带分类） -----------------
@router.get("/music/category", response_class=HTMLResponse)
def get_music_player_page(path: str = Query(...)):
    media_list = scan_media_files_by_category(path, AUDIO_EXTS, "audio")
    html = load_html_template("player.html")
    html = html.replace("{{PAGE_TITLE}}", f"音乐播放 - {path}")
    html = html.replace("{{CATEGORY_LIST_URL}}", "/api/v1/media/music")
    html = html.replace("{{MEDIA_JSON}}", json.dumps(media_list, ensure_ascii=False))
    return html


# ----------------- 路由 5: 视频播放页面（带分类） -----------------
@router.get("/video/category", response_class=HTMLResponse)
def get_video_player_page(path: str = Query(...)):
    media_list = scan_media_files_by_category(path, VIDEO_EXTS, "video")
    html = load_html_template("player.html")
    html = html.replace("{{PAGE_TITLE}}", f"视频播放 - {path}")
    html = html.replace("{{CATEGORY_LIST_URL}}", "/api/v1/media/video")
    html = html.replace("{{MEDIA_JSON}}", json.dumps(media_list, ensure_ascii=False))
    return html