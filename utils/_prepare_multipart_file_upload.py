from typing import Any, Dict

def _prepare_multipart_file_upload(
    file: Any,
    headers: Dict[str, Any],
) -> tuple:
    """
    Prepare file and headers for multipart upload.

    Returns:
        Tuple of (files_dict, headers_without_content_type)
    """
    from litellm.litellm_core_utils.prompt_templates.common_utils import (
        extract_file_data,
    )

    extracted = extract_file_data(file)
    filename = extracted.get("filename") or "file"
    content = extracted.get("content") or b""
    content_type = extracted.get("content_type") or "application/octet-stream"
    files = {"file": (filename, content, content_type)}

    # Remove content-type header - httpx will set it automatically for multipart
    headers_copy = headers.copy()
    headers_copy.pop("content-type", None)
    headers_copy.pop("Content-Type", None)

    return files, headers_copy

