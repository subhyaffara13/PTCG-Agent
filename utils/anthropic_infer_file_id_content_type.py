
def anthropic_infer_file_id_content_type(
    file_id: str,
) -> Literal["document_url", "container_upload"]:
    """
    Use when 'format' not provided.

    - URL's - assume are document_url
    - Else - assume is container_upload
    """
    if file_id.startswith("http") or file_id.startswith("https"):
        return "document_url"
    else:
        return "container_upload"

