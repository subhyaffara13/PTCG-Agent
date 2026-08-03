from pathlib import Path


def _get_cache_file_to_return(
    path_or_repo_id: str,
    full_filename: str,
    cache_dir: str | Path | None = None,
    revision: str | None = None,
    repo_type: str | None = None,
):
    # We try to see if we have a cached version (not up to date):
    resolved_file = try_to_load_from_cache(
        path_or_repo_id, full_filename, cache_dir=cache_dir, revision=revision, repo_type=repo_type
    )
    if resolved_file is not None and resolved_file != _CACHED_NO_EXIST:
        return resolved_file
    return None

