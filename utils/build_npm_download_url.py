
def build_npm_download_url(purl):
    """
    Return a npm download URL from the `purl` string.
    """
    purl_data = PackageURL.from_string(purl)

    namespace = purl_data.namespace
    name = purl_data.name
    version = purl_data.version

    base_url = "https://registry.npmjs.org"

    if namespace:
        base_url += f"/{namespace}"

    if name and version:
        return f"{base_url}/{name}/-/{name}-{version}.tgz"

