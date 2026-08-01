
def reset_xet_connection_info_cache_for_repo(repo_type: str | None, repo_id: str) -> None:
    """Reset the XET connection info cache for the given repo type and repo id.

    Used when a repo is deleted.
    """
    if repo_type is None:
        repo_type = constants.REPO_TYPE_MODEL
    prefix = f"{repo_type}-{repo_id}|"
    for k in list(XET_CONNECTION_INFO_CACHE.keys()):
        if k.startswith(prefix):
            XET_CONNECTION_INFO_CACHE.pop(k, None)

