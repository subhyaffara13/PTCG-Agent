
def build_hackage_repo_url(purl):
    """
    Return a hackage repo URL from the `purl` string.
    """
    purl_data = PackageURL.from_string(purl)

    name = purl_data.name
    version = purl_data.version

    if name and version:
        return f"https://hackage.haskell.org/package/{name}-{version}"
    elif name:
        return f"https://hackage.haskell.org/package/{name}"

