from typing import Optional

def infer_content_type_from_url_and_content(
    url: str,
    content: bytes,
    current_content_type: Optional[str] = None,
) -> str:
    """
    Infer content type from URL extension and binary content when content-type header is missing or generic.

    This helper implements a fallback strategy for determining MIME types when HTTP headers
    are missing or provide generic values (like binary/octet-stream). It's commonly used
    when processing images and documents from various sources (S3, URLs, etc.).

    Fallback Strategy:
    1. If current_content_type is valid (not None and not generic octet-stream), return it
    2. Try to infer from URL extension (handles query parameters)
    3. Try to detect from binary content signature (magic bytes)
    4. Raise ValueError if all methods fail

    Args:
        url: The URL of the content (used to extract file extension)
        content: The binary content (first ~100 bytes are sufficient for detection)
        current_content_type: The current content-type from headers (may be None or generic)

    Returns:
        str: The inferred MIME type (e.g., "image/png", "application/pdf")

    Raises:
        ValueError: If content type cannot be determined by any method

    Example:
        >>> content_type = infer_content_type_from_url_and_content(
        ...     url="https://s3.amazonaws.com/bucket/image.png?AWSAccessKeyId=123",
        ...     content=png_binary_data,
        ...     current_content_type="binary/octet-stream"
        ... )
        >>> print(content_type)
        "image/png"
    """
    from litellm.litellm_core_utils.token_counter import get_image_type

    # If we have a valid content type that's not generic, use it
    if current_content_type and current_content_type not in [
        "binary/octet-stream",
        "application/octet-stream",
    ]:
        return current_content_type

    # Extension to MIME type mapping
    # Supports images, documents, and other common file types
    extension_to_mime = {
        # Image formats
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "png": "image/png",
        "gif": "image/gif",
        "webp": "image/webp",
        # Document formats
        "pdf": "application/pdf",
        "csv": "text/csv",
        "doc": "application/msword",
        "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "xls": "application/vnd.ms-excel",
        "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "html": "text/html",
        "txt": "text/plain",
        "md": "text/markdown",
    }

    # Try to infer from URL extension
    if url:
        extension = url.split(".")[-1].lower().split("?")[0]  # Remove query params
        inferred_type = extension_to_mime.get(extension)
        if inferred_type:
            return inferred_type

    # Try to detect from binary content signature (magic bytes)
    if content:
        detected_type = get_image_type(content[:100])
        if detected_type:
            type_to_mime = {
                "png": "image/png",
                "jpeg": "image/jpeg",
                "gif": "image/gif",
                "webp": "image/webp",
                "heic": "image/heic",
            }
            if detected_type in type_to_mime:
                return type_to_mime[detected_type]

    # If all fallbacks failed, raise error
    raise ValueError(
        f"Unable to determine content type from URL: {url}. "
        f"Response content-type: {current_content_type}"
    )

