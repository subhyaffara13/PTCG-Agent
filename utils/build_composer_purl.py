
def build_composer_purl(uri):
    # We use a more general route pattern instead of using `composer_pattern`
    # below by itself because we want to capture all packagist download URLs,
    # even the ones that are not completely formed. This helps prevent url2purl
    # from attempting to create a generic PackageURL from an invalid packagist
    # download URL.

    # https://packagist.org/packages/ralouphie/getallheaders
    # https://packagist.org/packages/symfony/process#v7.0.0-BETA3
    composer_pattern = r"^https?://packagist\.org/packages/(?P<namespace>[^/]+)/(?P<name>[^\#]+?)(\#(?P<version>.+))?$"
    return purl_from_pattern("composer", composer_pattern, uri)

