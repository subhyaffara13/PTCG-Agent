from typing import Any

def safe_get(client: Any, url: str, **kwargs: Any) -> Any:
    """
    Fetch a user-supplied URL with SSRF protection on every redirect hop.

    Validates the initial URL and each redirect target before making the
    request. No DNS rebinding (resolve-and-rewrite). No redirect bypass
    (each hop validated). No breaking change for legitimate CDN redirects.

    When ``litellm.user_url_validation`` is False, validation is bypassed
    and this function delegates to ``client.get(url, follow_redirects=True)``.

    Args:
        client: An httpx.Client (sync).
        url: The user-supplied URL.
        **kwargs: Additional kwargs passed to client.get().

    Returns:
        The final httpx.Response.
    """
    if not getattr(litellm, "user_url_validation", True):
        kwargs.setdefault("follow_redirects", True)
        return client.get(url, **kwargs)
    kwargs.pop("follow_redirects", None)
    caller_headers = kwargs.pop("headers", {})
    for _ in range(_MAX_REDIRECTS):
        validated_url, original_host = validate_url(url)
        response = client.get(
            validated_url,
            headers={**caller_headers, "Host": original_host},
            follow_redirects=False,
            **kwargs,
        )
        if not response.is_redirect:
            return response
        # Resolve the next hop against the ORIGINAL (pre-rewrite) URL so
        # relative Location headers keep the original hostname.
        url = _extract_redirect_url(response, url)
    raise SSRFError("Too many redirects")

