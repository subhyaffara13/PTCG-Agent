
def get_download_url(purl):
    """
    Return a download URL inferred from the `purl` string.
    """
    download_url = _get_url_from_router(download_router, purl)
    if download_url:
        return download_url

    # Fallback on the `download_url` qualifier when available.
    purl_data = PackageURL.from_string(purl)
    return purl_data.qualifiers.get("download_url", None)

