
def _parse_repo_body(
    location: str,
    type_: constants.HfUriType,
    *,
    raw: str,
) -> HfUri:
    """Parse the body of a repo URI: '<repo_id>[@<revision>][/<path>]'."""
    location = location.strip("/")
    if not location:
        raise HfUriError(uri=raw, msg="Missing repository id.")

    # The '@' separates the repo_id from the revision, but only when it
    # appears right after 'namespace/name' (at most one '/' before it).
    # An '@' deeper in the path (e.g. in a filename like 'file@1.txt') is literal.
    at_idx = location.find("@")
    revision: str | None

    if at_idx == -1 or location[:at_idx].count("/") > 1:
        # No '@' at all, or the '@' is past the repo_id portion (in a filename).
        revision = None
        parts = location.split("/", 2)
        if len(parts) < 2:
            raise HfUriError(uri=raw, msg=f"Repository id must be 'namespace/name', got '{location}'. ")
        repo_id = f"{parts[0]}/{parts[1]}"
        path_in_repo = parts[2] if len(parts) > 2 else ""
    else:
        repo_id = location[:at_idx]
        rev_and_path = location[at_idx + 1 :]
        if not repo_id:
            raise HfUriError(uri=raw, msg="Missing repository id before '@'.")
        if repo_id.count("/") != 1:
            raise HfUriError(uri=raw, msg=f"Repository id must be 'namespace/name', got '{repo_id}'.")
        # Special refs like 'refs/pr/10' contain '/' and must be matched eagerly,
        # otherwise we would split them at the first '/' and treat the rest as a path.
        match = _SPECIAL_REFS_REVISION_REGEX.match(rev_and_path)
        if match is not None:
            revision = match.group()
            path_in_repo = rev_and_path[len(revision) :].removeprefix("/")
        else:
            slash_idx = rev_and_path.find("/")
            if slash_idx == -1:
                revision = rev_and_path
                path_in_repo = ""
            else:
                revision = rev_and_path[:slash_idx]
                path_in_repo = rev_and_path[slash_idx + 1 :]
        revision = unquote(revision)
        if not revision:
            raise HfUriError(uri=raw, msg="Empty revision after '@'.")

    return HfUri(
        type=type_,
        id=repo_id,
        revision=revision,
        path_in_repo=path_in_repo,
        _raw=raw,
    )

