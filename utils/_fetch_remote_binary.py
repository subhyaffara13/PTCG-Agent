
def _fetch_remote_binary(owner: str, repo_name: str, branch: str, short_name: str) -> bytes:
    executable_name = _get_executable_name(short_name)
    raw_url = f"https://raw.githubusercontent.com/{owner}/{repo_name}/refs/heads/{branch}/{executable_name}"
    response = get_session().get(raw_url, follow_redirects=True, timeout=_EXTENSIONS_DOWNLOAD_TIMEOUT)
    response.raise_for_status()
    return response.content

