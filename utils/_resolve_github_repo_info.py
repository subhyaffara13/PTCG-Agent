
def _resolve_github_repo_info(owner: str, repo_name: str) -> tuple[str, str | None]:
    try:
        response = get_session().get(
            f"https://api.github.com/repos/{owner}/{repo_name}",
            follow_redirects=True,
            timeout=_EXTENSIONS_DOWNLOAD_TIMEOUT,
        )
        response.raise_for_status()
        data = response.json()
        return data["default_branch"], data.get("description")
    except Exception:
        return _EXTENSIONS_DEFAULT_BRANCH, None

