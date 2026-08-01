
def _repo_cache_id_from_target(target: str) -> str:
    """Return the cache id matching a repo target passed to `hf cache rm`."""
    if not target.startswith("hf://"):
        return target

    uri = parse_hf_uri(target)
    if not uri.is_repo:
        raise CLIError("Only repository hf:// URIs are supported by `hf cache rm`.")
    if uri.revision is not None or uri.path_in_repo:
        raise CLIError("Only repo-level hf:// URIs are supported by `hf cache rm` for now.")
    return f"{uri.type}/{uri.id}"

