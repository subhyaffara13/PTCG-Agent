
def _build_document_from_upload(
    file_content: bytes,
    filename: Optional[str],
    content_type: Optional[str],
) -> Dict[str, str]:
    """
    Convert uploaded file bytes into a Mistral-format document dict with base64 data URI.

    Delegates to convert_file_document_to_url_document after resolving MIME type
    from the upload's content_type header or filename.
    """
    mime_type = content_type.split(";")[0].strip() if content_type else None
    if not mime_type or mime_type == "application/octet-stream":
        if filename:
            mime_type = get_mime_type(filename)

    return convert_file_document_to_url_document(
        {
            "type": "file",
            "file": file_content,
            "mime_type": mime_type or "application/octet-stream",
        }
    )

