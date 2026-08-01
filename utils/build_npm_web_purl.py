
def build_npm_web_purl(uri):
    path = unquote_plus(urlparse(uri).path)
    if path.startswith("/package/"):
        path = path[9:]

    segments = [seg for seg in path.split("/") if seg]
    len_segments = len(segments)
    namespace = version = None

    # @angular/cli/v/10.1.2
    if len_segments == 4:
        namespace = segments[0]
        name = segments[1]
        version = segments[3]

    # express/v/4.17.1
    elif len_segments == 3:
        namespace = None
        name = segments[0]
        version = segments[2]

    # @angular/cli
    elif len_segments == 2:
        namespace = segments[0]
        name = segments[1]

    # express
    elif len_segments == 1 and len(segments) > 0 and segments[0][0] != "@":
        name = segments[0]

    else:
        return

    return PackageURL("npm", namespace, name, version)

