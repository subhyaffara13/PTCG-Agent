
def build_pub_download_url(purl):
    """
    Return a pub download URL from the `purl` string.
    """
    purl_data = PackageURL.from_string(purl)

    name = purl_data.name
    version = purl_data.version

    if name and version:
        return f"https://pub.dev/api/archives/{name}-{version}.tar.gz"

