import io
import zipfile
from datetime import datetime
from typing import List

from fastapi import APIRouter, Request, Header, HTTPException
from fastapi import UploadFile, File, Response, Query

from app.core import utils
from app.api.v1.wall import router as wall_router

router = APIRouter()

router.include_router(wall_router, prefix="/wall", tags=["AnonymousWall"])

# 统一支持的压缩格式列表
ARCHIVE_EXTS = ('.zip', '.7z', '.tar', '.gz', '.bz2', '.xz', '.tgz')


@router.get("/health")
async def health_check():
    """K8s 存活探针使用的接口"""
    return {"status": "healthy", "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')}


@router.post("/watermark")
async def apply_watermark(
        files: List[UploadFile] = File(...),
        text: str = Query("内部资源_请勿外泄")
):
    # 场景 1: 单文件上传
    if len(files) == 1:
        file = files[0]
        name = file.filename.lower()
        content = await file.read()

        # 检查是否为压缩包
        is_archive = any(name.endswith(ext) for ext in ARCHIVE_EXTS)

        if is_archive:
            current_ext = next(ext for ext in ARCHIVE_EXTS if name.endswith(ext))
            result_zip = utils.process_any_archive(content, text, current_ext)
            return Response(
                content=result_zip,
                media_type="application/zip",
                headers={"Content-Disposition": f"attachment; filename=marked_{file.filename}"}
            )

        # 单个普通文件处理
        _, result_content = utils.dispatch_task((file.filename, content), text)

        # 确定 MIME 类型
        if name.endswith(".pdf"):
            m_type = "application/pdf"
        elif name.endswith((".docx", ".doc")):
            m_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        else:
            m_type = "image/jpeg"

        return Response(
            content=result_content,
            media_type=m_type,
            headers={"Content-Disposition": f"attachment; filename=marked_{file.filename}"}
        )

    # 场景 2: 用户在浏览器一次性选择了多个文件上传
    files_to_process = []
    for f in files:
        files_to_process.append((f.filename, await f.read()))

    # 执行批量保序任务
    processed_results = utils.run_batch_task(files_to_process, text)

    # 多个文件统一打包成 ZIP 返回
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED) as out_zip:
        for name, data in processed_results:
            out_zip.writestr(name, data)

    return Response(
        content=zip_buffer.getvalue(),
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=batch_results.zip"}
    )
