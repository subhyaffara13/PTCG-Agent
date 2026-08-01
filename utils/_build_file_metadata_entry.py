
def _build_file_metadata_entry(
    response: Any,
    file_data: Optional[Tuple[str, bytes, str]] = None,
    file_url: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Build a file metadata entry for storing in vector_store_metadata.

    Args:
        response: The response from litellm.aingest containing file_id
        file_data: Optional tuple of (filename, content, content_type)
        file_url: Optional URL if file was ingested from URL

    Returns:
        Dictionary with file metadata (file_id, filename, file_url, ingested_at, etc.)
    """
    from datetime import datetime, timezone

    # Extract file_id from response
    file_id = None
    if hasattr(response, "get"):
        file_id = response.get("file_id")
    elif hasattr(response, "file_id"):
        file_id = response.file_id

    # Extract file information from file_data tuple
    filename = None
    file_size = None
    content_type = None

    if file_data:
        filename = file_data[0]
        file_size = len(file_data[1]) if len(file_data) > 1 else None
        content_type = file_data[2] if len(file_data) > 2 else None

    # Build file metadata entry
    file_entry = {
        "file_id": file_id,
        "filename": filename,
        "file_url": file_url,
        "ingested_at": datetime.now(timezone.utc).isoformat(),
    }

    # Add optional fields if available
    if file_size is not None:
        file_entry["file_size"] = file_size
    if content_type is not None:
        file_entry["content_type"] = content_type

    return file_entry

