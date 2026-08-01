
def _as_url(content: ContentT, default_mime_type: str) -> str:
    if isinstance(content, str) and content.startswith(("http://", "https://", "data:")):
        return content

    # Convert content to bytes
    raw_bytes = _open_as_mime_bytes(content)

    # Get MIME type
    mime_type = raw_bytes.mime_type or default_mime_type

    # Encode content to base64
    encoded_data = base64.b64encode(raw_bytes).decode()

    # Build data URL
    return f"data:{mime_type};base64,{encoded_data}"

