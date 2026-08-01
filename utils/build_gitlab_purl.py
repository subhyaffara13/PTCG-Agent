
def build_gitlab_purl(url):
    """
    Return a PackageURL object from Gitlab `url`.
    For example:
    https://gitlab.com/TG1999/firebase/-/tree/1a122122/views
    https://gitlab.com/TG1999/firebase/-/tree
    https://gitlab.com/TG1999/firebase/-/master
    https://gitlab.com/tg1999/Firebase/-/tree/master
    https://gitlab.com/tg1999/Firebase/-/commit/bf04e5f289885cf2f20a92b387bcc6df33e30809
    """
    # https://gitlab.com/<ns>/<name>/-/commit/<sha>
    commit_pattern = (
        r"https?://gitlab.com/"
        r"(?P<namespace>[^/]+)/(?P<name>[^/]+)/-/commit/"
        r"(?P<version>[0-9a-fA-F]{7,64})/?$"
    )

    commit_matche = re.search(commit_pattern, url)
    if commit_matche:
        return PackageURL(
            type="gitlab",
            namespace=commit_matche.group("namespace"),
            name=commit_matche.group("name"),
            version=commit_matche.group("version"),
            qualifiers={},
            subpath="",
        )

    segments = get_path_segments(url)

    if not len(segments) >= 2:
        return
    namespace = segments[0]
    name = segments[1]
    version = None
    subpath = None

    # https://gitlab.com/TG1999/firebase/master
    if (len(segments) >= 3) and segments[2] != "-" and segments[2] != "tree":
        version = segments[2]
        subpath = "/".join(segments[3:])

    # https://gitlab.com/TG1999/firebase/-/tree/master
    if len(segments) >= 5 and (segments[2] == "-" and segments[3] == "tree"):
        version = segments[4]
        subpath = "/".join(segments[5:])

    return PackageURL(
        type="gitlab",
        namespace=namespace,
        name=name,
        version=version,
        subpath=subpath,
    )

