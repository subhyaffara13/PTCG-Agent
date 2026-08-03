from typing import Optional

def sanitize_cloud_object_path(value: Optional[str], fallback: str = "file") -> str:
    if not isinstance(value, str):
        return fallback

    segments = []
    for segment in value.replace("\\", "/").split("/"):
        sanitized_segment = sanitize_cloud_object_component(segment, fallback="")
        if sanitized_segment:
            segments.append(sanitized_segment)

    if not segments:
        return fallback
    return "/".join(segments)

