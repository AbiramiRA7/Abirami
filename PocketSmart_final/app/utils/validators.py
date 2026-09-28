from fastapi import HTTPException, UploadFile
from ..config import get_settings

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}

async def read_optional_image(upload: UploadFile | None):
    if not upload or not upload.filename:
        return None, None
    if upload.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(415, "Only JPEG, PNG, or WebP images are supported")
    data = await upload.read()
    if len(data) > get_settings().max_upload_mb * 1024 * 1024:
        raise HTTPException(413, f"Image exceeds {get_settings().max_upload_mb} MB limit")
    return data, upload.content_type
