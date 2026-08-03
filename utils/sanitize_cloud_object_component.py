from typing import Optional

def sanitize_cloud_object_component(
    value: Optional[str], fallback: str = "file"
) -> str:
    if not isinstance(value, str):
        return fallback

    component = posixpath.basename(value.replace("\\", "/")).strip()
    if component in {"", ".", ".."}:
        return fallback

    component = "".join(
        "_" if ord(char) < 32 or ord(char) == 127 else char for char in component
    )
    component = _SAFE_OBJECT_COMPONENT_PATTERN.sub("_", component)
    component = component.strip("._")
    if not component:
        return fallback
    return component[:255]

