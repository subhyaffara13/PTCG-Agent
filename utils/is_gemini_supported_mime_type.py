
def is_gemini_supported_mime_type(mime_type: str) -> bool:
    """
    Check if a MIME type is supported by Gemini multimodal models.

    Supported categories:
    - Images: image/png, image/jpeg, image/webp
    - Video: 3gpp, wmv, webm, mp4, mpg, mpegps, mpeg, quicktime, x-flv
    - Audio: webm, wav, pcm, opus, mp4, mpga, mpeg, m4a, mp3, flac, aac
    - Documents: text/plain, application/pdf

    Args:
        mime_type: MIME type to check

    Returns:
        bool: True if supported, False otherwise
    """
    normalized = normalize_mime_type_for_provider(mime_type, provider="gemini")
    return normalized in (
        GEMINI_SUPPORTED_IMAGE_TYPES
        | GEMINI_SUPPORTED_VIDEO_TYPES
        | GEMINI_SUPPORTED_AUDIO_TYPES
        | GEMINI_SUPPORTED_DOCUMENT_TYPES
    )

