
def url2purl(url):
    """
    Return a PackageURL inferred from the `url` string or None.
    """
    if url:
        try:
            return purl_router.process(url)
        except NoRouteAvailable:
            # If `url` does not fit in one of the existing routes,
            # we attempt to create a generic PackageURL for `url`
            return build_generic_purl(url)

