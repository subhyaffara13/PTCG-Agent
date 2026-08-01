
def refresh_xet_connection_info(
    *,
    file_data: XetFileData,
    headers: dict[str, str],
) -> XetConnectionInfo:
    """
    Utilizes the information in the parsed metadata to request the Hub xet connection information.
    This includes the access token, expiration, and XET service URL.
    Args:
        file_data: (`XetFileData`):
            The file data needed to refresh the xet connection information.
        headers (`dict[str, str]`):
            Headers to use for the request, including authorization headers and user agent.
    Returns:
        `XetConnectionInfo`:
            The connection information needed to make the request to the xet storage service.
    Raises:
        [`~utils.HfHubHTTPError`]
            If the Hub API returned an error.
        [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError)
            If the Hub API response is improperly formatted.
    """
    if file_data.refresh_route is None:
        raise ValueError("The provided xet metadata does not contain a refresh endpoint.")
    return _fetch_xet_connection_info_with_url(file_data.refresh_route, headers)

