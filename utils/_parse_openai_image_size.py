from typing import Optional

def _parse_openai_image_size(size: str) -> Optional[tuple[int, int]]:
    if size == "auto":
        return None

    width_str, separator, height_str = size.lower().partition("x")
    if not separator:
        return None

    try:
        width = int(width_str)
        height = int(height_str)
    except ValueError:
        return None

    if width <= 0 or height <= 0:
        return None

    return width, height

