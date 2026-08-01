
def build_rubygems_repo_url(purl):
    """
    Return a rubygems repo URL from the `purl` string.
    """
    purl_data = PackageURL.from_string(purl)

    name = purl_data.name
    version = purl_data.version

    if name and version:
        return f"https://rubygems.org/gems/{name}/versions/{version}"
    elif name:
        return f"https://rubygems.org/gems/{name}"

