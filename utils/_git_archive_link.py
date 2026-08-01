
def _git_archive_link(repo_owner, repo_name, ref):
    # See https://docs.github.com/en/rest/reference/repos#download-a-repository-archive-zip
    return f"https://github.com/{repo_owner}/{repo_name}/zipball/{ref}"

