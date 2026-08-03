from typing import Optional

def _validate_public_image_url(value: Optional[str], field_name: str) -> None:
    """
    Reject anything that isn't a plain http(s) URL with a host. This value is
    later served via the unauthenticated /get_image endpoint, so local paths
    like "/etc/passwd" or "file://..." must not be accepted.
    """
    if value is None:
        return
    if not isinstance(value, str) or not value.strip():
        return
    parsed = urlparse(value.strip())
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise HTTPException(
            status_code=400,
            detail={
                "error": (
                    f"Invalid {field_name}: must be an http(s) URL with a host. "
                    "Local filesystem paths and non-http schemes are not allowed."
                )
            },
        )

