
def build_cran_purl(uri):
    cran_pattern = r"^https?://(cran\.r-project\.org|packagemanager\.rstudio\.com/cran)/.*?src/contrib/(?P<name>.+)_(?P<version>.+)\.tar.gz$"
    qualifiers = {}
    if "//cran.r-project.org/" not in uri:
        qualifiers["download_url"] = uri
    return purl_from_pattern("cran", cran_pattern, uri, qualifiers)

