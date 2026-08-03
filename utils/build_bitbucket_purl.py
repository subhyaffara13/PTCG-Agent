import re

def build_bitbucket_purl(url):
    """
    Return a PackageURL object from BitBucket `url`.
    For example:
    https://bitbucket.org/TG1999/first_repo/src/master or
    https://bitbucket.org/TG1999/first_repo/src or
    https://bitbucket.org/TG1999/first_repo/src/master/new_folder
    https://bitbucket.org/TG1999/first_repo/commits/16a60c4a74ef477cd8c16ca82442eaab2fbe8c86
    """
    commit_matche = re.search(bitbucket_commit_pattern, url)
    if commit_matche:
        return PackageURL(
            type="bitbucket",
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

    bitbucket_download_pattern = (
        r"https?://bitbucket.org/"
        r"(?P<namespace>.+)/(?P<name>.+)/downloads/"
        r"(?P<version>.+).(zip|tar.gz|tar.bz2|.tgz|exe|msi)"
    )
    matches = re.search(bitbucket_download_pattern, url)

    qualifiers = {}
    if matches:
        qualifiers["download_url"] = url
        return PackageURL(type="bitbucket", namespace=namespace, name=name, qualifiers=qualifiers)

    version = None
    subpath = None

    # https://bitbucket.org/TG1999/first_repo/new_folder/
    if len(segments) >= 3 and segments[2] != "src":
        version = segments[2]
        subpath = "/".join(segments[3:])

    # https://bitbucket.org/TG1999/first_repo/src/master/new_folder/
    if len(segments) >= 4 and segments[2] == "src":
        version = segments[3]
        subpath = "/".join(segments[4:])

    return PackageURL(
        type="bitbucket",
        namespace=namespace,
        name=name,
        version=version,
        subpath=subpath,
    )

