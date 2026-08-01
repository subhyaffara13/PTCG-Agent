
def _parse_bucket_body(
    location: str,
    type_: constants.HfUriType,
    *,
    raw: str,
) -> HfUri:
    """Parse the body of a bucket URI: 'namespace/name[/path]'."""
    location = location.strip("/")
    parts = location.split("/", 2)
    if len(parts) < 2 or not parts[0] or not parts[1]:
        raise HfUriError(uri=raw, msg=f"Bucket id must be 'namespace/name', got '{location}'.")
    bucket_id = f"{parts[0]}/{parts[1]}"
    if "@" in bucket_id:
        raise HfUriError(uri=raw, msg="Bucket URIs do not support a revision marker ('@').")
    path_in_bucket = parts[2] if len(parts) >= 3 else ""
    return HfUri(
        type=type_,
        id=bucket_id,
        revision=None,
        path_in_repo=path_in_bucket,
        _raw=raw,
    )

