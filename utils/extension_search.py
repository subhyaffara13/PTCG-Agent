
def extension_search() -> None:
    """Search extensions available on GitHub (tagged with 'hf-extension' topic)."""
    response = get_session().get(
        "https://api.github.com/search/repositories",
        params={"q": f"topic:{_EXTENSIONS_GITHUB_TOPIC}", "sort": "stars", "order": "desc", "per_page": 100},
        follow_redirects=True,
        timeout=_EXTENSIONS_DOWNLOAD_TIMEOUT,
    )
    response.raise_for_status()
    data = response.json()

    installed = {m.short_name for m in _list_installed_extensions()}

    rows = []
    for repo in data.get("items", []):
        repo_name = repo["name"]
        short_name = repo_name[3:] if repo_name.startswith("hf-") else repo_name
        rows.append(
            {
                "name": short_name,
                "repo": repo["full_name"],
                "stars": repo.get("stargazers_count", 0),
                "description": repo.get("description") or "",
                "installed": "yes" if short_name in installed else "",
            }
        )

    out.table(rows, id_key="repo")

