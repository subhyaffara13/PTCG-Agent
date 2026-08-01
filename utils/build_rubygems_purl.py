
def build_rubygems_purl(uri):
    # We use a more general route pattern instead of using `rubygems_pattern`
    # below by itself because we want to capture all rubygems download URLs,
    # even the ones that are not completely formed. This helps prevent url2purl
    # from attempting to create a generic PackageURL from an invalid rubygems
    # download URL.

    # https://rubygems.org/downloads/jwt-0.1.8.gem
    # https://rubygems.org/gems/i18n-js-3.0.11.gem
    rubygems_pattern = (
        r"^https?://rubygems.org/(downloads|gems)/(?P<name>.+)-(?P<version>.+)(\.gem)$"
    )
    return purl_from_pattern("gem", rubygems_pattern, uri)

