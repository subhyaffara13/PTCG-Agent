
def get_path_segments(url):
    """
    Return a list of path segments from a `url` string.
    """
    path = unquote_plus(urlparse(url).path)
    segments = [seg for seg in path.split("/") if seg]
    return segments

