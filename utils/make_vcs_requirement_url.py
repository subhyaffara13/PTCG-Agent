
def make_vcs_requirement_url(
    repo_url: str, rev: str, project_name: str, subdir: str | None = None
) -> str:
    """
    Return the URL for a VCS requirement.

    Args:
      repo_url: the remote VCS url, with any needed VCS prefix (e.g. "git+").
      project_name: the (unescaped) project name.
    """
    quoted_rev = urllib.parse.quote(rev, "/")
    egg_project_name = project_name.replace("-", "_")
    req = f"{repo_url}@{quoted_rev}#egg={egg_project_name}"
    if subdir:
        req += f"&subdirectory={subdir}"

    return req

