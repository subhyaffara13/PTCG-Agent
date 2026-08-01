
def fetch_xet_connection_info_from_repo_info(
    *,
    token_type: XetTokenType,
    repo_id: str,
    repo_type: str,
    revision: str | None = None,
    headers: dict[str, str],
    endpoint: str | None = None,
    params: dict[str, str] | None = None,
) -> XetConnectionInfo:
    """
    Uses the repo info to request a xet access token from Hub.
    Args:
        token_type (`XetTokenType`):
            Type of the token to request: `"read"` or `"write"`.
        repo_id (`str`):
            A namespace (user or an organization) and a repo name separated by a `/`.
        repo_type (`str`):
            Type of the repo to upload to: `"model"`, `"dataset"` or `"space"`.
        revision (`str`, `optional`):
            The revision of the repo to get the token for.
        headers (`dict[str, str]`):
            Headers to use for the request, including authorization headers and user agent.
        endpoint (`str`, `optional`):
            The endpoint to use for the request. Defaults to the Hub endpoint.
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
    url = xet_connection_info_refresh_url(
        token_type=token_type,
        repo_id=repo_id,
        repo_type=repo_type,
        revision=revision,
        endpoint=endpoint,
    )
    return _fetch_xet_connection_info_with_url(url, headers, params, cache_key_prefix=f"{repo_type}-{repo_id}")

