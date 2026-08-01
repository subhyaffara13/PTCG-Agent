
def build_npm_repo_url(purl):
    """
    Return a npm repo URL from the `purl` string.
    """
    purl_data = PackageURL.from_string(purl)

    namespace = purl_data.namespace
    name = purl_data.name
    version = purl_data.version

    repo_url = "https://www.npmjs.com/package/"
    if namespace:
        repo_url += f"{namespace}/"

    repo_url += f"{name}"

    if version:
        repo_url += f"/v/{version}"

    return repo_url

