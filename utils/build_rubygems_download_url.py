
def build_rubygems_download_url(purl):
    """
    Return a rubygems download URL from the `purl` string.
    """
    purl_data = PackageURL.from_string(purl)

    name = purl_data.name
    version = purl_data.version

    if name and version:
        return f"https://rubygems.org/downloads/{name}-{version}.gem"

