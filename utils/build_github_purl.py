import re

def build_github_purl(url):
    """
    Return a PackageURL object from GitHub `url`.
    """

    # https://github.com/apache/nifi/archive/refs/tags/rel/nifi-2.0.0-M3.tar.gz
    archive_tags_pattern = (
        r"https?://github.com/(?P<namespace>.+)/(?P<name>.+)"
        r"/archive/refs/tags/"
        r"(?P<version>.+).(zip|tar.gz|tar.bz2|.tgz)"
    )

    # https://github.com/nexB/scancode-toolkit/archive/v3.1.1.zip
    archive_pattern = (
        r"https?://github.com/(?P<namespace>.+)/(?P<name>.+)"
        r"/archive/(.*/)*"
        r"((?P=name)(-|_|@))?"
        r"(?P<version>.+).(zip|tar.gz|tar.bz2|.tgz)"
    )

    # https://github.com/downloads/mozilla/rhino/rhino1_7R4.zip
    download_pattern = (
        r"https?://github.com/downloads/(?P<namespace>.+)/(?P<name>.+)/"
        r"((?P=name)(-|@)?)?"
        r"(?P<version>.+).(zip|tar.gz|tar.bz2|.tgz)"
    )

    # https://github.com/pypa/get-virtualenv/raw/20.0.31/public/virtualenv.pyz
    raw_pattern = (
        r"https?://github.com/(?P<namespace>.+)/(?P<name>.+)"
        r"/raw/(?P<version>[^/]+)/(?P<subpath>.*)$"
    )

    # https://github.com/fanf2/unifdef/blob/master/unifdef.c
    blob_pattern = (
        r"https?://github.com/(?P<namespace>.+)/(?P<name>.+)"
        r"/blob/(?P<version>[^/]+)/(?P<subpath>.*)$"
    )

    releases_download_pattern = (
        r"https?://github.com/(?P<namespace>.+)/(?P<name>.+)"
        r"/releases/download/(?P<version>[^/]+)/.*$"
    )

    # https://github.com/pombredanne/schematics.git
    git_pattern = r"https?://github.com/(?P<namespace>.+)/(?P<name>.+).(git)"

    # https://github.com/<namespace>/<name>/commit/<sha>
    commit_pattern = (
        r"https?://github.com/"
        r"(?P<namespace>[^/]+)/(?P<name>[^/]+)/commit/(?P<version>[0-9a-fA-F]{7,40})/?$"
    )

    patterns = (
        commit_pattern,
        archive_tags_pattern,
        archive_pattern,
        raw_pattern,
        blob_pattern,
        releases_download_pattern,
        download_pattern,
        git_pattern,
    )

    for pattern in patterns:
        matches = re.search(pattern, url)
        qualifiers = {}
        if matches:
            if pattern == releases_download_pattern:
                qualifiers["download_url"] = url
            return purl_from_pattern(
                type_="github", pattern=pattern, url=url, qualifiers=qualifiers
            )

    segments = get_path_segments(url)
    if not len(segments) >= 2:
        return

    namespace = segments[0]
    name = segments[1]
    version = None
    subpath = None

    # https://github.com/TG1999/fetchcode/master
    if len(segments) >= 3 and segments[2] != "tree":
        version = segments[2]
        subpath = "/".join(segments[3:])

    # https://github.com/TG1999/fetchcode/tree/master
    if len(segments) >= 4 and segments[2] == "tree":
        version = segments[3]
        subpath = "/".join(segments[4:])

    return PackageURL(
        type="github",
        namespace=namespace,
        name=name,
        version=version,
        subpath=subpath,
    )

