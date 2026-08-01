
def _clean_file_url_path(part: str) -> str:
    """
    Clean the first part of a URL path that corresponds to a local
    filesystem path (i.e. the first part after splitting on "@" characters).
    """
    # We unquote prior to quoting to make sure nothing is double quoted.
    # Also, on Windows the path part might contain a drive letter which
    # should not be quoted. On Linux where drive letters do not
    # exist, the colon should be quoted. We rely on urllib.request
    # to do the right thing here.
    ret = urllib.request.pathname2url(urllib.request.url2pathname(part))
    if ret.startswith("///"):
        # Remove any URL authority section, leaving only the URL path.
        ret = ret.removeprefix("//")
    return ret

