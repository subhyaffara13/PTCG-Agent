
def select_anthropic_content_block_type_for_file(
    format: str,
) -> Literal["document", "image", "container_upload"]:
    if format == "application/pdf" or format == "text/plain":
        return "document"
    elif format in ["image/jpeg", "image/png", "image/gif", "image/webp"]:
        return "image"
    else:
        return "container_upload"

