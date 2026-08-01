
def build_golang_repo_url(purl):
    """
    Return a golang repo URL from the `purl` string.
    """
    purl_data = PackageURL.from_string(purl)

    namespace = purl_data.namespace
    name = purl_data.name
    version = purl_data.version

    if name and version:
        return f"https://pkg.go.dev/{namespace}/{name}@{version}"
    elif name:
        return f"https://pkg.go.dev/{namespace}/{name}"

