
def build_pypi_repo_url(purl):
    """
    Return a pypi repo URL from the `purl` string.
    """
    purl_data = PackageURL.from_string(purl)

    name = (purl_data.name or "").replace("_", "-")
    version = purl_data.version

    if name and version:
        return f"https://pypi.org/project/{name}/{version}/"
    elif name:
        return f"https://pypi.org/project/{name}/"

