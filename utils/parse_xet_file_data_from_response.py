
def parse_xet_file_data_from_response(response: httpx.Response, endpoint: str | None = None) -> XetFileData | None:
    """
    Parse XET file metadata from an HTTP response.

    This function extracts XET file metadata from the HTTP headers or HTTP links
    of a given response object. If the required metadata is not found, it returns `None`.

    Args:
        response (`httpx.Response`):
            The HTTP response object containing headers dict and links dict to extract the XET metadata from.
    Returns:
        `Optional[XetFileData]`:
            An instance of `XetFileData` containing the file hash and refresh route if the metadata
            is found. Returns `None` if the required metadata is missing.
    """
    if response is None:
        return None
    try:
        file_hash = response.headers[constants.HUGGINGFACE_HEADER_X_XET_HASH]

        if constants.HUGGINGFACE_HEADER_LINK_XET_AUTH_KEY in response.links:
            refresh_route = response.links[constants.HUGGINGFACE_HEADER_LINK_XET_AUTH_KEY]["url"]
        else:
            refresh_route = response.headers[constants.HUGGINGFACE_HEADER_X_XET_REFRESH_ROUTE]
    except KeyError:
        return None
    endpoint = endpoint if endpoint is not None else constants.ENDPOINT
    if refresh_route.startswith(constants.HUGGINGFACE_CO_URL_HOME):
        refresh_route = refresh_route.replace(constants.HUGGINGFACE_CO_URL_HOME.rstrip("/"), endpoint.rstrip("/"))
    return XetFileData(
        file_hash=file_hash,
        refresh_route=refresh_route,
    )

