
def _validate_push_notification_url(url: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme != "https":
        raise HTTPException(
            status_code=400,
            detail="Push notification URL must use HTTPS",
        )
    try:
        validate_url(url)
    except (SSRFError, ValueError) as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

