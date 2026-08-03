from typing import Dict, Optional

def _build_part_for_input(
    element: str,
    resolved_files: Optional[Dict[str, Dict[str, str]]] = None,
) -> PartType:
    """
    Build a single PartType for an input element, handling text, data URIs,
    file references, and GCS URLs.
    """
    resolved_files = resolved_files or {}

    if element.startswith("data:") and ";base64," in element:
        mime_type, base64_data = _parse_data_url(element)
        blob: BlobType = {"mime_type": mime_type, "data": base64_data}
        return PartType(inline_data=blob)
    elif _is_gcs_url(element):
        mime_type = _infer_mime_type_from_gcs_url(element)
        file_data: FileDataType = {
            "mime_type": mime_type,
            "file_uri": element,
        }
        return PartType(file_data=file_data)
    elif _is_file_reference(element):
        if element not in resolved_files:
            raise ValueError(f"File reference {element} not resolved")
        file_info = resolved_files[element]
        file_data_ref: FileDataType = {
            "mime_type": file_info["mime_type"],
            "file_uri": file_info["uri"],
        }
        return PartType(file_data=file_data_ref)
    else:
        return PartType(text=element)

