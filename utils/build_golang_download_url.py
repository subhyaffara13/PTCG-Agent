
def build_golang_download_url(purl):
    """
    Return a golang download URL from the `purl` string.
    """
    purl_data = PackageURL.from_string(purl)

    namespace = purl_data.namespace
    name = purl_data.name
    version = purl_data.version

    if not name:
        return

    # TODO: https://github.com/package-url/packageurl-python/issues/197
    if namespace:
        name = f"{namespace}/{name}"

    ename = escape_golang_path(name)
    eversion = escape_golang_path(version)

    if not eversion.startswith("v"):
        eversion = "v" + eversion

    if name and version:
        return f"https://proxy.golang.org/{ename}/@v/{eversion}.zip"

