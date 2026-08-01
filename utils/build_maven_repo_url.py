
def build_maven_repo_url(purl):
    """
    Return a Maven repo URL from the `purl` string.
    """
    purl_data = PackageURL.from_string(purl)
    namespace = purl_data.namespace
    name = purl_data.name
    version = purl_data.version
    qualifiers = purl_data.qualifiers

    base_url = qualifiers.get("repository_url", DEFAULT_MAVEN_REPOSITORY)

    if namespace and name and version:
        namespace = namespace.replace(".", "/")
        return f"{base_url}/{namespace}/{name}/{version}"

