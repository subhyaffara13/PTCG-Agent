
def build_luarocks_download_url(purl):
    """
    Return a LuaRocks download URL from the `purl` string.
    """
    purl_data = PackageURL.from_string(purl)

    qualifiers = purl_data.qualifiers or {}

    repository_url = qualifiers.get("repository_url", "https://luarocks.org")

    name = purl_data.name
    version = purl_data.version

    if name and version:
        return f"{repository_url}/{name}-{version}.src.rock"

