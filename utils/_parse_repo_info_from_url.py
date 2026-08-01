
def _parse_repo_info_from_url(url: str) -> tuple[str | None, str | None]:
    """Extract (repo_type, repo_id) from an API URL.

    Returns canonical repo_type values: "model", "dataset", "space" (or None).

    Examples:
        >>> _parse_repo_info_from_url("https://huggingface.co/api/models/user/repo")
        ("model", "user/repo")
        >>> _parse_repo_info_from_url("https://huggingface.co/api/datasets/user/repo/resolve/main/data.csv")
        ("dataset", "user/repo")
        >>> _parse_repo_info_from_url("https://huggingface.co/api/models/bert-base-cased/resolve/main/config.json")
        ("model", "bert-base-cased")
    """
    match = _REPO_ID_FROM_URL_REGEX.search(url)
    if not match:
        return None, None
    repo_type = constants.REPO_TYPES_MAPPING.get(match.group(1))
    first, second = match.group(2), match.group(3)
    if second and second not in _REPO_URL_SUBPATHS:
        repo_id = f"{first}/{second}"
    else:
        repo_id = first
    return repo_type, repo_id

