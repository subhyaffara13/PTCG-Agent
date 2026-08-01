
def build_cran_repo_url(purl):
    """
    Return a cran repo URL from the `purl` string.
    """
    purl_data = PackageURL.from_string(purl)

    name = purl_data.name
    version = purl_data.version

    return f"https://cran.r-project.org/src/contrib/{name}_{version}.tar.gz"

