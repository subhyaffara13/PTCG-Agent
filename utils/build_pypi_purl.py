
def build_pypi_purl(uri):
    path = unquote_plus(urlparse(uri).path)
    segments = path.split("/")
    last_segment = segments[-1]

    # /wheel-0.29.0-py2.py3-none-any.whl
    if last_segment.endswith(".whl"):
        match = wheel_file_re.match(last_segment)
        if match:
            return PackageURL(
                "pypi",
                name=match.group("name"),
                version=match.group("version"),
            )

    if segments[1] == "project":
        return PackageURL(
            "pypi",
            name=segments[2],
            version=segments[3] if len(segments) > 3 else None,
        )

    return purl_from_pattern("pypi", pypi_pattern, last_segment)

