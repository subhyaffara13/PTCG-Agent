
def build_sourceforge_purl(uri):
    # We use a more general route pattern instead of using `sourceforge_pattern`
    # below by itself because we want to capture all sourceforge download URLs,
    # even the ones that do not fit `sourceforge_pattern`. This helps prevent
    # url2purl from attempting to create a generic PackageURL from a sourceforge
    # URL that we can't handle.

    # http://master.dl.sourceforge.net/project/libpng/zlib/1.2.3/zlib-1.2.3.tar.bz2
    sourceforge_pattern = (
        r"^https?://.*sourceforge.net/projects?/"
        r"(?P<namespace>([^/]+))/"  # do not allow more "/" segments
        r"(OldFiles/)?"
        r"(?P<name>.+)/"
        r"(?P<version>[v0-9\.]+)/"  # version restricted to digits and dots
        r"(?P=name).*(?P=version).*"  # {name}-{version} repeated in the filename
        r"[^/]$"  # not ending with "/"
    )

    sourceforge_purl = purl_from_pattern("sourceforge", sourceforge_pattern, uri)

    if not sourceforge_purl:
        # Get the project name from `uri` and use that as the Package name
        # http://master.dl.sourceforge.net/project/aloyscore/aloyscore/0.1a1%2520stable/0.1a1_stable_AloysCore.zip
        split_uri = uri.split("/project/")

        # http://master.dl.sourceforge.net, aloyscore/aloyscore/0.1a1%2520stable/0.1a1_stable_AloysCore.zip
        if len(split_uri) >= 2:
            # aloyscore/aloyscore/0.1a1%2520stable/0.1a1_stable_AloysCore.zip
            remaining_uri_path = split_uri[1]
            # aloyscore, aloyscore, 0.1a1%2520stable, 0.1a1_stable_AloysCore.zip
            remaining_uri_path_segments = remaining_uri_path.split("/")
            if remaining_uri_path_segments:
                project_name = remaining_uri_path_segments[0]  # aloyscore
                sourceforge_purl = PackageURL(
                    type="sourceforge", name=project_name, qualifiers={"download_url": uri}
                )
    return sourceforge_purl

