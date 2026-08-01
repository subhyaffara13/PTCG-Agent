
def build_github_api_purl(url):
    """
    Return a PackageURL object from GitHub API `url`.
    For example:
    https://api.github.com/repos/nexB/scancode-toolkit/commits/40593af0df6c8378d2b180324b97cb439fa11d66
    https://api.github.com/repos/nexB/scancode-toolkit/
    and returns a `PackageURL` object
    """
    segments = get_path_segments(url)

    if not (len(segments) >= 3):
        return
    namespace = segments[1]
    name = segments[2]
    version = None

    # https://api.github.com/repos/nexB/scancode-toolkit/
    if len(segments) == 4 and segments[3] != "commits":
        version = segments[3]

    # https://api.github.com/repos/nexB/scancode-toolkit/commits/40593af0df6c8378d2b180324b97cb439fa11d66
    if len(segments) == 5 and segments[3] == "commits":
        version = segments[4]

    return PackageURL(type="github", namespace=namespace, name=name, version=version)

