
def build_bitbucket_repo_url(purl):
    """
    Return a bitbucket repo URL from the `purl` string.
    """
    purl_data = PackageURL.from_string(purl)

    namespace = purl_data.namespace
    name = purl_data.name

    if name and namespace:
        return f"https://bitbucket.org/{namespace}/{name}"

