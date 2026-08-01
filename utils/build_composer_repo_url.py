
def build_composer_repo_url(purl):
    """
    Return a composer repo URL from the `purl` string.
    """
    purl_data = PackageURL.from_string(purl)

    name = purl_data.name
    version = purl_data.version
    namespace = purl_data.namespace

    if name and version:
        return f"https://packagist.org/packages/{namespace}/{name}#{version}"
    elif name:
        return f"https://packagist.org/packages/{namespace}/{name}"

