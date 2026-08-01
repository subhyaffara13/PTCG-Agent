
def _infer_mime_type_from_gcs_url(gcs_url: str) -> str:
    """
    Infer MIME type from GCS URL file extension.

    Args:
        gcs_url: GCS URL like gs://bucket/path/to/file.png

    Returns:
        str: Inferred MIME type

    Raises:
        ValueError: If file extension is not supported
    """
    extension_to_mime = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".mp3": "audio/mpeg",
        ".wav": "audio/wav",
        ".mp4": "video/mp4",
        ".mov": "video/quicktime",
        ".pdf": "application/pdf",
    }

    gcs_url_lower = gcs_url.lower()
    for ext, mime_type in extension_to_mime.items():
        if gcs_url_lower.endswith(ext):
            return mime_type

    raise ValueError(
        f"Unable to infer MIME type from GCS URL: {gcs_url}. "
        f"Supported extensions: {', '.join(extension_to_mime.keys())}"
    )

