
def build_nuget_download_url(purl):
    """
    Return a nuget download URL from the `purl` string.
    """
    purl_data = PackageURL.from_string(purl)

    name = purl_data.name
    version = purl_data.version

    if name and version:
        return f"https://www.nuget.org/api/v2/package/{name}/{version}"

