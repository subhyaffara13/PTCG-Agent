
def build_apk_download_url(purl):
    """
    Return a download URL for a fully qualified Alpine Linux package PURL.

    Example:
    pkg:apk/acct@6.6.4-r0?arch=x86&alpine_version=v3.11&repo=main
    """
    purl = PackageURL.from_string(purl)
    name = purl.name
    version = purl.version
    arch = purl.qualifiers.get("arch")
    repo = purl.qualifiers.get("repo")
    alpine_version = purl.qualifiers.get("alpine_version")

    if not name or not version or not arch or not repo or not alpine_version:
        raise ValueError(
            "All qualifiers (arch, repo, alpine_version) and name/version must be present in apk purl"
        )

    return (
        f"https://dl-cdn.alpinelinux.org/alpine/{alpine_version}/{repo}/{arch}/{name}-{version}.apk"
    )

