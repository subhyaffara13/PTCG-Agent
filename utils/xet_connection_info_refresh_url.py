
def xet_connection_info_refresh_url(
    *,
    token_type: XetTokenType,
    repo_id: str,
    repo_type: str,
    revision: str | None = None,
    endpoint: str | None = None,
) -> str:
    """
    Build the URL used to fetch or refresh a Xet access token for a given repo.
    Args:
        token_type (`XetTokenType`):
            Type of the token to request: `"read"` or `"write"`.
        repo_id (`str`):
            A namespace (user or an organization) and a repo name separated by a `/`.
        repo_type (`str`):
            Type of the repo (e.g. `"model"`, `"dataset"`, `"space"`, `"bucket"`).
        revision (`str`, `optional`):
            The revision of the repo to get the token for.
        endpoint (`str`, `optional`):
            The endpoint to use for the request. Defaults to the Hub endpoint.
    Returns:
        `str`:
            The fully-qualified URL of the token refresh endpoint.
    """
    endpoint = endpoint if endpoint is not None else constants.ENDPOINT
    url = f"{endpoint}/api/{repo_type}s/{repo_id}/xet-{token_type.value}-token"
    if repo_type != "bucket" or revision is not None:
        # On "bucket" repo type, the revision never needed => don't use it
        # Otherwise, use the revision.
        # Note: when creating a PR on a git-based repo, user needs write access but they don't know the revision in advance.
        # => pass "/None" in URL and server will return a token for PR refs.
        url += f"/{revision}"
    return url

