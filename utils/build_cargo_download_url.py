
def build_cargo_download_url(purl):
    """
    Return a cargo download URL from the `purl` string.
    """
    purl_data = PackageURL.from_string(purl)

    name = purl_data.name
    version = purl_data.version

    if name and version:
        return f"https://crates.io/api/v1/crates/{name}/{version}/download"

