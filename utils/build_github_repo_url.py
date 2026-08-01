
def build_github_repo_url(purl):
    """
    Return a github repo URL from the `purl` string.
    """
    purl_data = PackageURL.from_string(purl)

    namespace = purl_data.namespace
    name = purl_data.name
    version = purl_data.version
    qualifiers = purl_data.qualifiers

    if not (name and namespace):
        return

    repo_url = f"https://github.com/{namespace}/{name}"

    if version:
        version_prefix = qualifiers.get("version_prefix", "")
        repo_url = f"{repo_url}/tree/{version_prefix}{version}"

    return repo_url

