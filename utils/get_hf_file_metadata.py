
def get_hf_file_metadata(
    url: str,
    token: bool | str | None = None,
    timeout: float | None = constants.HF_HUB_ETAG_TIMEOUT,
    library_name: str | None = None,
    library_version: str | None = None,
    user_agent: dict | str | None = None,
    headers: dict[str, str] | None = None,
    endpoint: str | None = None,
    retry_on_errors: bool = False,
) -> HfFileMetadata:
    """Fetch metadata of a file versioned on the Hub for a given url.

    Args:
        url (`str`):
            File url, for example returned by [`hf_hub_url`].
        token (`str` or `bool`, *optional*):
            A token to be used for the download.
                - If `True`, the token is read from the HuggingFace config
                  folder.
                - If `False` or `None`, no token is provided.
                - If a string, it's used as the authentication token.
        timeout (`float`, *optional*, defaults to 10):
            How many seconds to wait for the server to send metadata before giving up.
        library_name (`str`, *optional*):
            The name of the library to which the object corresponds.
        library_version (`str`, *optional*):
            The version of the library.
        user_agent (`dict`, `str`, *optional*):
            The user-agent info in the form of a dictionary or a string.
        headers (`dict`, *optional*):
            Additional headers to be sent with the request.
        endpoint (`str`, *optional*):
            Endpoint of the Hub. Defaults to <https://huggingface.co>.
        retry_on_errors (`bool`, *optional*, defaults to `False`):
            Whether to retry on errors (429, 5xx, timeout, network errors).
            If False, no retry for fast fallback to local cache.

    Returns:
        A [`HfFileMetadata`] object containing metadata such as location, etag, size and
        commit_hash.
    """
    hf_headers = build_hf_headers(
        token=token,
        library_name=library_name,
        library_version=library_version,
        user_agent=user_agent,
        headers=headers,
    )
    hf_headers["Accept-Encoding"] = "identity"  # prevent any compression => we want to know the real size of the file

    # Retrieve metadata
    response = _httpx_follow_relative_redirects_with_backoff(
        method="HEAD", url=url, headers=hf_headers, timeout=timeout, retry_on_errors=retry_on_errors
    )
    hf_raise_for_status(response)

    # Return
    return HfFileMetadata(
        commit_hash=response.headers.get(constants.HUGGINGFACE_HEADER_X_REPO_COMMIT),
        # We favor a custom header indicating the etag of the linked resource, and we fall back to the regular etag header.
        etag=_normalize_etag(
            response.headers.get(constants.HUGGINGFACE_HEADER_X_LINKED_ETAG) or response.headers.get("ETag")
        ),
        # Either from response headers (if redirected) or defaults to request url
        # Do not use directly `url` as we might have followed relative redirects.
        location=response.headers.get("Location") or str(response.request.url),  # type: ignore
        size=_int_or_none(
            response.headers.get(constants.HUGGINGFACE_HEADER_X_LINKED_SIZE) or response.headers.get("Content-Length")
        ),
        xet_file_data=parse_xet_file_data_from_response(response, endpoint=endpoint),  # type: ignore
    )

