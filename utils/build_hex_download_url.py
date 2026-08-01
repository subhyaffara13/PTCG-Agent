
def build_hex_download_url(purl):
    """
    Return a hex download URL from the `purl` string.
    """
    purl_data = PackageURL.from_string(purl)

    name = purl_data.name
    version = purl_data.version

    if name and version:
        return f"https://repo.hex.pm/tarballs/{name}-{version}.tar"

