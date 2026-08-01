
def _parse_data_url(data_url: str) -> Optional[Tuple[bytes, str, str]]:
    """
    Parse data URL (base64 image).

    Returns:
        Tuple of (content_bytes, content_type, extension) or None
    """
    match = re.match(r"data:([^;]+);base64,(.+)", data_url)
    if not match:
        return None

    content_type = match.group(1)
    base64_data = match.group(2)
    content_bytes = base64.b64decode(base64_data)
    ext = content_type.split("/")[-1].split(";")[0] or "jpg"

    return content_bytes, content_type, ext


def _parse_data_url(data_url: str) -> Tuple[str, str]:
    """
    Parse a data URL to extract the media type and base64 data.

    Args:
        data_url: Data URL in format: data:image/jpeg;base64,/9j/4AAQ...

    Returns:
        tuple: (media_type, base64_data)
            media_type: e.g., "image/jpeg", "video/mp4", "audio/mpeg"
            base64_data: The base64-encoded data without the prefix

    Raises:
        ValueError: If data URL format is invalid or MIME type is unsupported
    """
    if not data_url.startswith("data:"):
        raise ValueError(f"Invalid data URL format: {data_url[:50]}...")

    if "," not in data_url:
        raise ValueError(f"Invalid data URL format (missing comma): {data_url[:50]}...")

    metadata, base64_data = data_url.split(",", 1)

    metadata = metadata[5:]

    if ";" in metadata:
        media_type = metadata.split(";")[0]
    else:
        media_type = metadata

    if media_type not in SUPPORTED_EMBEDDING_MIME_TYPES:
        raise ValueError(
            f"Unsupported MIME type for embedding: {media_type}. "
            f"Supported types: {', '.join(sorted(SUPPORTED_EMBEDDING_MIME_TYPES))}"
        )

    return media_type, base64_data

