
def build_npm_api_purl(uri):
    path = unquote_plus(urlparse(uri).path)
    segments = [seg for seg in path.split("/") if seg]

    if len(segments) < 2:
        return

    # /@esbuild/freebsd-arm64/0.21.5
    if len(segments) == 3:
        return PackageURL("npm", namespace=segments[0], name=segments[1], version=segments[2])

    # /@invisionag/eslint-config-ivx
    if segments[0].startswith("@"):
        return PackageURL("npm", namespace=segments[0], name=segments[1])

    # /angular/1.6.6
    return PackageURL("npm", name=segments[0], version=segments[1])

