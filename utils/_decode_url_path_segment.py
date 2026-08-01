
def _decode_url_path_segment(segment: str) -> str:
    """Percent-decode a single URL path segment (e.g. 'file%20name.txt' -> 'file name.txt').

    A decoded '/' is re-encoded as '%2F' so the segment stays atomic when the normalized body is
    re-split by the shared parser. This decodes ordinary path characters (spaces, '#', ...) that
    browsers encode, while keeping '%2F'-encoded revisions (e.g. 'feature%2Ffoo') intact.
    """
    return unquote(segment).replace("/", "%2F")

