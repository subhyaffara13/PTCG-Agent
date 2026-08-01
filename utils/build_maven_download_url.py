
def build_maven_download_url(purl):
    """
    Return a maven download URL from the `purl` string.
    """
    purl_data = PackageURL.from_string(purl)

    namespace = purl_data.namespace
    name = purl_data.name
    version = purl_data.version
    qualifiers = purl_data.qualifiers

    base_url = qualifiers.get("repository_url", DEFAULT_MAVEN_REPOSITORY)
    maven_type = qualifiers.get("type", "jar")  # default to "jar"
    classifier = qualifiers.get("classifier")

    if namespace and name and version:
        namespace = namespace.replace(".", "/")
        classifier = f"-{classifier}" if classifier else ""
        return f"{base_url}/{namespace}/{name}/{version}/{name}-{version}{classifier}.{maven_type}"

