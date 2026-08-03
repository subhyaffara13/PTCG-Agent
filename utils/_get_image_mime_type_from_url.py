from typing import Optional

def _get_image_mime_type_from_url(url: str) -> Optional[str]:
    """
    Get mime type for common image URLs
    See gemini mime types: https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-understanding#image-requirements

    Supported by Gemini:
     application/pdf
    audio/mpeg
    audio/mp3
    audio/wav
    audio/ogg
    image/png
    image/jpeg
    image/webp
    text/plain
    video/mov
    video/mpeg
    video/mp4
    video/mpg
    video/avi
    video/wmv
    video/mpegps
    video/flv
    """
    from urllib.parse import urlparse

    url = url.lower()

    # Parse URL to extract path without query parameters
    # This handles URLs like: https://example.com/image.jpg?signature=...
    parsed = urlparse(url)
    path = parsed.path

    # Map file extensions to mime types
    mime_types = {
        # Images
        (".jpg", ".jpeg"): "image/jpeg",
        (".png",): "image/png",
        (".webp",): "image/webp",
        # Videos
        (".mp4",): "video/mp4",
        (".mov",): "video/mov",
        (".mpeg", ".mpg"): "video/mpeg",
        (".avi",): "video/avi",
        (".wmv",): "video/wmv",
        (".mpegps",): "video/mpegps",
        (".flv",): "video/flv",
        # Audio
        (".mp3",): "audio/mp3",
        (".wav",): "audio/wav",
        (".mpeg",): "audio/mpeg",
        (".ogg",): "audio/ogg",
        # Documents
        (".pdf",): "application/pdf",
        (".txt",): "text/plain",
    }

    # Check each extension group against the URL
    for extensions, mime_type in mime_types.items():
        if any(path.endswith(ext) for ext in extensions):
            return mime_type

    return None

