
def get_path_info(environ: WSGIEnvironment) -> str:
    """Return ``PATH_INFO`` from  the WSGI environment.

    :param environ: WSGI environment to get the path from.

    .. versionchanged:: 3.0
        The ``charset`` and ``errors`` parameters were removed.

    .. versionadded:: 0.9
    """
    path: bytes = environ.get("PATH_INFO", "").encode("latin1")
    return path.decode(errors="replace")

