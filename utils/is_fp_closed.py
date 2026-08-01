
def is_fp_closed(obj: object) -> bool:
    """
    Checks whether a given file-like object is closed.

    :param obj:
        The file-like object to check.
    """

    try:
        # Check `isclosed()` first, in case Python3 doesn't set `closed`.
        # GH Issue #928
        return obj.isclosed()  # type: ignore[no-any-return, attr-defined]
    except AttributeError:
        pass

    try:
        # Check via the official file-like-object way.
        return obj.closed  # type: ignore[no-any-return, attr-defined]
    except AttributeError:
        pass

    try:
        # Check if the object is a container for another file-like object that
        # gets released on exhaustion (e.g. HTTPResponse).
        return obj.fp is None  # type: ignore[attr-defined]
    except AttributeError:
        pass

    raise ValueError("Unable to determine whether fp is closed.")


def is_fp_closed(obj: object) -> bool:
    """
    Checks whether a given file-like object is closed.

    :param obj:
        The file-like object to check.
    """

    try:
        # Check `isclosed()` first, in case Python3 doesn't set `closed`.
        # GH Issue #928
        return obj.isclosed()  # type: ignore[no-any-return, attr-defined]
    except AttributeError:
        pass

    try:
        # Check via the official file-like-object way.
        return obj.closed  # type: ignore[no-any-return, attr-defined]
    except AttributeError:
        pass

    try:
        # Check if the object is a container for another file-like object that
        # gets released on exhaustion (e.g. HTTPResponse).
        return obj.fp is None  # type: ignore[attr-defined]
    except AttributeError:
        pass

    raise ValueError("Unable to determine whether fp is closed.")

