
def parse_xet_connection_info_from_headers(headers: dict[str, str]) -> XetConnectionInfo | None:
    """
    Parse XET connection info from the HTTP headers or return None if not found.
    Args:
        headers (`dict`):
           HTTP headers to extract the XET metadata from.
    Returns:
        `XetConnectionInfo` or `None`:
            The information needed to connect to the XET storage service.
            Returns `None` if the headers do not contain the XET connection info.
    """
    try:
        endpoint = headers[constants.HUGGINGFACE_HEADER_X_XET_ENDPOINT]
        access_token = headers[constants.HUGGINGFACE_HEADER_X_XET_ACCESS_TOKEN]
        expiration_unix_epoch = int(headers[constants.HUGGINGFACE_HEADER_X_XET_EXPIRATION])
    except (KeyError, ValueError, TypeError):
        return None

    return XetConnectionInfo(
        endpoint=endpoint,
        access_token=access_token,
        expiration_unix_epoch=expiration_unix_epoch,
    )

