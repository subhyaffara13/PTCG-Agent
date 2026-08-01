
def _file_info(url, session, size_policy="head", **kwargs):
    """Call HEAD on the server to get details about the file (size/checksum etc.)

    Default operation is to explicitly allow redirects and use encoding
    'identity' (no compression) to get the true size of the target.
    """
    logger.debug("Retrieve file size for %s", url)
    kwargs = kwargs.copy()
    ar = kwargs.pop("allow_redirects", True)
    head = kwargs.get("headers", {}).copy()
    # TODO: not allowed in JS
    # head["Accept-Encoding"] = "identity"
    kwargs["headers"] = head

    info = {}
    if size_policy == "head":
        r = session.head(url, allow_redirects=ar, **kwargs)
    elif size_policy == "get":
        r = session.get(url, allow_redirects=ar, **kwargs)
    else:
        raise TypeError(f'size_policy must be "head" or "get", got {size_policy}')
    r.raise_for_status()

    # TODO:
    #  recognise lack of 'Accept-Ranges',
    #                 or 'Accept-Ranges': 'none' (not 'bytes')
    #  to mean streaming only, no random access => return None
    if "Content-Length" in r.headers:
        info["size"] = int(r.headers["Content-Length"])
    elif "Content-Range" in r.headers:
        info["size"] = int(r.headers["Content-Range"].split("/")[1])
    elif "content-length" in r.headers:
        info["size"] = int(r.headers["content-length"])
    elif "content-range" in r.headers:
        info["size"] = int(r.headers["content-range"].split("/")[1])

    for checksum_field in ["ETag", "Content-MD5", "Digest"]:
        if r.headers.get(checksum_field):
            info[checksum_field] = r.headers[checksum_field]

    return info

