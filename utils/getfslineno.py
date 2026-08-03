from pathlib import Path


def getfslineno(obj: object) -> tuple[str | Path, int]:
    """Return source location (path, lineno) for the given object.

    If the source cannot be determined return ("", -1).

    The line number is 0-based.
    """
    # xxx let decorators etc specify a sane ordering
    # NOTE: this used to be done in _pytest.compat.getfslineno, initially added
    #       in 6ec13a2b9.  It ("place_as") appears to be something very custom.
    obj = get_real_func(obj)
    if hasattr(obj, "place_as"):
        obj = obj.place_as

    try:
        code = Code.from_function(obj)
    except TypeError:
        try:
            fn = inspect.getsourcefile(obj) or inspect.getfile(obj)  # type: ignore[arg-type]
        except TypeError:
            return "", -1

        fspath = (fn and absolutepath(fn)) or ""
        lineno = -1
        if fspath:
            try:
                _, lineno = findsource(obj)
            except OSError:
                pass
        return fspath, lineno

    return code.path, code.firstlineno

