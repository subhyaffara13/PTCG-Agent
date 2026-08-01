
def build_maven_purl(uri):
    path = unquote_plus(urlparse(uri).path)
    segments = [seg for seg in path.split("/") if seg and seg != "maven2"]

    if len(segments) < 3:
        return

    before_last_segment, last_segment = segments[-2:]
    has_filename = before_last_segment in last_segment

    filename = None
    if has_filename:
        filename = segments.pop()

    version = segments[-1]
    name = segments[-2]
    namespace = ".".join(segments[:-2])
    qualifiers = {}

    if filename:
        name_version = f"{name}-{version}"
        _, _, classifier_ext = filename.rpartition(name_version)
        classifier, _, extension = classifier_ext.partition(".")
        if not extension:
            return

        qualifiers["classifier"] = classifier.strip("-")

        valid_types = ("aar", "ear", "mar", "pom", "rar", "rpm", "sar", "tar.gz", "war", "zip")
        if extension in valid_types:
            qualifiers["type"] = extension

    return PackageURL("maven", namespace, name, version, qualifiers)

