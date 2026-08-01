
def build_cargo_repo_url(purl):
    """
    Return a cargo repo URL from the `purl` string.
    """
    purl_data = PackageURL.from_string(purl)

    name = purl_data.name
    version = purl_data.version

    if name and version:
        return f"https://crates.io/crates/{name}/{version}"
    elif name:
        return f"https://crates.io/crates/{name}"

