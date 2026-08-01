
def _fetch_xet_connection_info_with_url(
    url: str,
    headers: dict[str, str],
    params: dict[str, str] | None = None,
    cache_key_prefix: str | None = None,
) -> XetConnectionInfo:
    """
    Requests the xet connection info from the supplied URL. This includes the
    access token, expiration time, and endpoint to use for the xet storage service.

    Result is cached to avoid redundant requests.

    Args:
        url: (`str`):
            The access token endpoint URL.
        headers (`dict[str, str]`):
            Headers to use for the request, including authorization headers and user agent.
        params (`dict[str, str]`, `optional`):
            Additional parameters to pass with the request.
    Returns:
        `XetConnectionInfo`:
            The connection information needed to make the request to the xet storage service.
    Raises:
        [`~utils.HfHubHTTPError`]
            If the Hub API returned an error.
        [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError)
            If the Hub API response is improperly formatted.
    """
    # Check cache first
    cache_key = _cache_key(url, headers, params, prefix=cache_key_prefix)
    cached_info = XET_CONNECTION_INFO_CACHE.get(cache_key)
    if cached_info is not None:
        if not _is_expired(cached_info):
            return cached_info

    # Fetch from server
    resp = http_backoff("GET", url, headers=headers, params=params)
    hf_raise_for_status(resp)

    metadata = parse_xet_connection_info_from_headers(resp.headers)  # type: ignore
    if metadata is None:
        raise ValueError("Xet headers have not been correctly set by the server.")

    # Delete expired cache entries
    for k, v in list(XET_CONNECTION_INFO_CACHE.items()):
        if _is_expired(v):
            XET_CONNECTION_INFO_CACHE.pop(k, None)

    # Enforce cache size limit
    if len(XET_CONNECTION_INFO_CACHE) >= XET_CONNECTION_INFO_CACHE_SIZE:
        XET_CONNECTION_INFO_CACHE.pop(next(iter(XET_CONNECTION_INFO_CACHE)))

    # Update cache
    XET_CONNECTION_INFO_CACHE[cache_key] = metadata

    return metadata

