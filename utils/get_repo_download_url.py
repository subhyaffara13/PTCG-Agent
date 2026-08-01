
def get_repo_download_url(purl):
    """
    Return ``download_url`` if present in ``purl`` qualifiers or
    if ``namespace``, ``name`` and ``version`` are present in ``purl``
    else return None.
    """
    purl_data = PackageURL.from_string(purl)

    namespace = purl_data.namespace
    type = purl_data.type
    name = purl_data.name
    version = purl_data.version
    qualifiers = purl_data.qualifiers

    download_url = qualifiers.get("download_url")
    if download_url:
        return download_url

    if not (namespace and name and version):
        return

    version_prefix = qualifiers.get("version_prefix", "")
    version = f"{version_prefix}{version}"

    return get_repo_download_url_by_package_type(
        type=type, namespace=namespace, name=name, version=version
    )

