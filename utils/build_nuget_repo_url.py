
def build_nuget_repo_url(purl):
    """
    Return a nuget repo URL from the `purl` string.
    """
    purl_data = PackageURL.from_string(purl)

    name = purl_data.name
    version = purl_data.version

    if name and version:
        return f"https://www.nuget.org/packages/{name}/{version}"
    elif name:
        return f"https://www.nuget.org/packages/{name}"

