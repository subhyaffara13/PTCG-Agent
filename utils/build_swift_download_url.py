
def build_swift_download_url(purl):
    """
    Return a Swift Package download URL from the `purl` string.
    """
    purl_data = PackageURL.from_string(purl)

    name = purl_data.name
    version = purl_data.version
    namespace = purl_data.namespace

    if not (namespace or name or version):
        return

    return f"https://{namespace}/{name}/archive/{version}.zip"

