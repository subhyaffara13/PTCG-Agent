import os
from typing import Optional, Tuple

def resolve_validated_local_image_path(candidate: str) -> Optional[Tuple[str, str]]:
    """Resolve ``candidate`` only when it is an existing supported image file."""
    if not candidate:
        return None
    try:
        resolved = os.path.realpath(os.path.expanduser(candidate))
    except (OSError, ValueError):
        return None
    if not os.path.isfile(resolved):
        return None

    try:
        with open(resolved, "rb") as f:
            header = f.read(LOCAL_IMAGE_HEADER_BYTES)
    except OSError as exc:
        verbose_proxy_logger.debug("Could not read local asset %r: %s", candidate, exc)
        return None

    media_type = detect_local_image_media_type(header)
    if media_type is None:
        verbose_proxy_logger.warning(
            "Local asset %r is not a supported image file; falling back to default.",
            candidate,
        )
        return None

    return resolved, media_type

