
def _url_to_uri_body(url: str, endpoint: str | None = None) -> str:
    """Normalize a Hugging Face web URL into the body of a 'hf://' URI (everything after 'hf://').

    The returned string is fed back into the regular URI parsing logic, so all validation
    (repo id, revision, empty path segments, ...) is shared with the canonical 'hf://' path.
    Only unambiguous URLs are accepted: any unrecognized route raises [`HfUriError`]. When 'endpoint'
    is provided, URLs on that custom Hub host are recognized too (and its path prefix is stripped).
    """
    raw = url
    # Prefix '//' for scheme-less inputs so 'urlsplit' populates 'netloc' instead of 'path'.
    parsed = urlsplit(url if "://" in url else "//" + url)
    host = (parsed.hostname or "").lower()
    if host not in _recognized_hosts(endpoint):
        raise HfUriError(
            uri=raw,
            msg=f"Unrecognized host '{host or url}'. Expected a Hugging Face URL (e.g. 'https://huggingface.co/...').",
        )

    # Query string and fragment are intentionally dropped (e.g. '?download=true').
    path = parsed.path
    # For a self-hosted endpoint with a path prefix (e.g. 'http://localhost:8080/hf'), drop it so the
    # remaining segments are '[<TYPE>/]<namespace>/<name>[/...]' just like on the public Hub.
    endpoint_host, endpoint_path = _endpoint_host_and_path(endpoint)
    if endpoint_path and host == endpoint_host:
        prefix = "/" + endpoint_path
        if path == prefix or path.startswith(prefix + "/"):
            path = path[len(prefix) :]
    segments = [segment for segment in path.split("/") if segment]
    if not segments:
        raise HfUriError(uri=raw, msg=f"Missing repository or bucket identifier in URL '{url}'.")

    # Optional type prefix ('datasets', 'spaces', 'kernels', 'buckets', 'models').
    type_prefix: str | None = None
    if segments[0] in constants.HF_URI_TYPE_PREFIXES:
        type_prefix = segments[0]
        segments = segments[1:]

    # Everything in the web UI is namespaced ('<namespace>/<name>'); a single segment is a user or
    # organization page (or a listing page), which we cannot map to a repository -> reject.
    if len(segments) < 2:
        raise HfUriError(
            uri=raw,
            msg=(
                f"Cannot parse URL '{url}': expected a '<namespace>/<name>' repository or bucket. "
                "User/organization pages and single-segment URLs are not supported."
            ),
        )
    repo_id = f"{segments[0]}/{segments[1]}"
    rest = segments[2:]

    if type_prefix == "buckets":
        if not rest:
            return f"buckets/{repo_id}"
        action, *tail = rest
        if action not in _URL_BUCKET_LOCATION_ACTIONS:
            raise HfUriError(uri=raw, msg=f"Cannot parse bucket URL '{url}': unsupported '/{action}/' route.")
        path = "/".join(_decode_url_path_segment(segment) for segment in tail)
        return f"buckets/{repo_id}/{path}" if path else f"buckets/{repo_id}"

    prefix = f"{type_prefix}/" if type_prefix else ""
    if not rest:
        return f"{prefix}{repo_id}"
    action, *tail = rest
    if action not in _URL_REPO_LOCATION_ACTIONS:
        raise HfUriError(
            uri=raw,
            msg=(
                f"Cannot parse URL '{url}': unsupported '/{action}/' route. "
                "Only repository pages and file/folder viewer routes (blob, resolve, raw, tree, ...) can be parsed."
            ),
        )
    if not tail:
        # e.g. '.../tree' with nothing after -> repository root.
        return f"{prefix}{repo_id}"
    # 'tail' is '<revision>/<path>'; reuse the canonical '@<revision>/<path>' splitting logic
    # (special refs, URL-encoded slashes, ...) by handing it back to the URI parser. Each segment
    # is percent-decoded first so file names with spaces, '#', ... resolve correctly; the revision
    # segment's '%2F' survives (re-encoded by '_decode_url_path_segment') and is decoded downstream.
    decoded = "/".join(_decode_url_path_segment(segment) for segment in tail)
    return f"{prefix}{repo_id}@{decoded}"

