from typing import Optional

def detect_local_image_media_type(header: bytes) -> Optional[str]:
    """Return a browser image media type for supported local image signatures."""
    if header[0:8] == b"\x89PNG\r\n\x1a\n":
        return "image/png"
    if header[0:4] == b"GIF8" and header[5:6] == b"a":
        return "image/gif"
    if header[0:3] == b"\xff\xd8\xff":
        return "image/jpeg"
    if header[0:4] == b"RIFF" and header[8:12] == b"WEBP":
        return "image/webp"
    if header[0:4] in (b"\x00\x00\x01\x00", b"\x00\x00\x02\x00"):
        return "image/x-icon"
    return None

