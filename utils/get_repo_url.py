
def get_repo_url(purl):
    """
    Return a repository URL inferred from the `purl` string.
    """
    return _get_url_from_router(repo_router, purl)

