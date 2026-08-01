
def get_repo_download_url_by_package_type(
    type, namespace, name, version, archive_extension="tar.gz"
):
    """
    Return the download URL for a hosted git repository given a package type
    or None.
    """
    if archive_extension not in ("zip", "tar.gz"):
        raise ValueError("Only zip and tar.gz extensions are supported")

    download_url_by_type = {
        "github": f"https://github.com/{namespace}/{name}/archive/{version}.{archive_extension}",
        "bitbucket": f"https://bitbucket.org/{namespace}/{name}/get/{version}.{archive_extension}",
        "gitlab": f"https://gitlab.com/{namespace}/{name}/-/archive/{version}/{name}-{version}.{archive_extension}",
    }
    return download_url_by_type.get(type)

