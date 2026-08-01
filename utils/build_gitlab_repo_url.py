
def build_gitlab_repo_url(purl):
    """
    Return a gitlab repo URL from the `purl` string.
    """
    purl_data = PackageURL.from_string(purl)

    namespace = purl_data.namespace
    name = purl_data.name

    if name and namespace:
        return f"https://gitlab.com/{namespace}/{name}"

