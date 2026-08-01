
def build_cocoapods_repo_url(purl):
    """
    Return a CocoaPods repo URL from the `purl` string.
    """
    purl_data = PackageURL.from_string(purl)
    name = purl_data.name
    return name and f"https://cocoapods.org/pods/{name}"

