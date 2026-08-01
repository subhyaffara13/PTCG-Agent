
def get_inferred_urls(purl):
    """
    Return all inferred URLs (repo, download) from the `purl` string.
    """
    url_functions = (
        get_repo_url,
        get_download_url,
    )

    inferred_urls = []
    for url_func in url_functions:
        url = url_func(purl)
        if url:
            inferred_urls.append(url)

    return inferred_urls

