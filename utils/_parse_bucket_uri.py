
def _parse_bucket_uri(path: str) -> HfUri:
    """Parse a bucket path into a HfUri.

    Accepts:
    - `hf://buckets/namespace/name(/path/in/repo)` URIs,
    - Hugging Face web URLs such as `https://huggingface.co/buckets/namespace/name(/tree/path)`,
    - plain `namespace/name(/path/in/repo)` paths.
    """
    if path.startswith(constants.HF_PROTOCOL) or _looks_like_hf_url(path):
        # Don't use 'if is_hf_uri(...)' here as we prefer 'parse_hf_uri(...)' to raise the exact error message.
        parsed = parse_hf_uri(path)
        if not parsed.is_bucket:
            raise ValueError(f"Invalid bucket path: {path}. Must be a bucket URI (hf://buckets/...).")
        return parsed
    parts = path.split("/", 2)
    if len(parts) < 2 or not parts[0] or not parts[1]:
        raise ValueError(f"Invalid bucket path: '{path}'. Expected format: namespace/bucket_name")
    bucket_id = f"{parts[0]}/{parts[1]}"
    prefix = "/".join(parts[2:])
    return HfUri(type="bucket", id=bucket_id, path_in_repo=prefix)

