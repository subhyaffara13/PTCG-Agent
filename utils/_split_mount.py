
def _split_mount(body: str, *, raw: str) -> tuple[str, str | None, bool | None]:
    """Split the ':<MOUNT_PATH>[:ro|:rw]' suffix from 'body'.

    Returns '(location, mount_path, read_only)' where 'mount_path' is 'None' if no mount segment is present.
    """
    if body.endswith(":ro"):
        read_only, body = True, body.removesuffix(":ro")
    elif body.endswith(":rw"):
        read_only, body = False, body.removesuffix(":rw")
    else:
        read_only = None

    # Mount paths always start with '/', so the delimiter is ':/'.
    # We use rfind() because the mount segment is always trailing
    idx = body.rfind(":/")
    if idx == -1:
        if read_only is not None:
            raise HfUriError(
                uri=raw,
                msg="':ro'/':rw' suffix is only valid when a mount path is provided (e.g. 'hf://...:/<MOUNT_PATH>:ro').",
            )
        return body, None, None

    location = body[:idx]
    mount_path = body[idx + 1 :]  # includes the leading '/'
    if not location:
        raise HfUriError(uri=raw, msg="Missing location before mount path.")
    return location, mount_path, read_only

