
def _normalize_langfuse_base_url(base_target_url: str) -> str:
    if not (
        base_target_url.startswith("http://") or base_target_url.startswith("https://")
    ):
        # Existing behavior allows host-only Langfuse settings.
        base_target_url = "http://" + base_target_url

    try:
        base_url = httpx.URL(base_target_url)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": f"Invalid Langfuse host: {str(e)}"},
        )

    if base_url.scheme not in ("http", "https") or not base_url.host:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Invalid Langfuse host"},
        )

    if base_url.userinfo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Langfuse host must not include credentials"},
        )

    return str(base_url)

