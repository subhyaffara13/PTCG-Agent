import re

def _is_anthropic_document_data_uri(url: str) -> bool:
    # Anthropic's base64 document source accepts only application/pdf and
    # text/plain (see select_anthropic_content_block_type_for_file). Routing
    # other mimes here would produce a document block the API rejects, so we
    # leave them on the image code path.
    match = re.match(r"data:([^;,]+)", url)
    if not match:
        return False
    return match.group(1) in _ANTHROPIC_DOCUMENT_BASE64_MEDIA_TYPES

