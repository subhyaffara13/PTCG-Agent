
def _try_fetch_remote_description(
    owner: str, repo_name: str, branch: str, candidate_description: str | None
) -> str | None:
    """Try to fetch project description either from:
    - manifest.json
    - pyproject.toml

    Only best effort, no error handling.
    """
    # from manifest.json
    try:
        response = get_session().get(
            f"https://raw.githubusercontent.com/{owner}/{repo_name}/refs/heads/{branch}/{MANIFEST_FILENAME}",
            follow_redirects=True,
        )
        response.raise_for_status()
        data = response.json()
        description = data.get("description")
        if isinstance(description, str):
            return description
    except Exception:
        pass

    # from pyproject.toml
    try:
        response = get_session().get(
            f"https://raw.githubusercontent.com/{owner}/{repo_name}/refs/heads/{branch}/pyproject.toml",
            follow_redirects=True,
        )
        response.raise_for_status()

        # Weak parser but ok for "best effort"
        for line in response.text.splitlines():
            line = line.strip()
            if line.startswith("description"):
                _, _, value = line.partition("=")
                return value.strip().strip("\"'")
    except Exception:
        pass

    # fallback to value fetched from GH API directly
    return candidate_description

