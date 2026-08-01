
def _build_langfuse_proxy_target(
    *,
    endpoint: str,
    base_target_url: str,
    dynamic_host_supplied: bool,
):
    endpoint_path = _validate_langfuse_proxy_path(endpoint)
    base_url = httpx.URL(_normalize_langfuse_base_url(base_target_url))
    updated_url = base_url.copy_with(path=endpoint_path)
    custom_headers = {}

    if dynamic_host_supplied and getattr(litellm, "user_url_validation", True):
        try:
            target_url, host_header = validate_url(str(updated_url))
        except SSRFError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": f"Invalid Langfuse host: {str(e)}"},
            )
        custom_headers["Host"] = host_header
        return target_url, custom_headers

    return str(updated_url), custom_headers

