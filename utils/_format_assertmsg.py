
def _format_assertmsg(obj: object) -> str:
    r"""Format the custom assertion message given.

    For strings this simply replaces newlines with '\n~' so that
    util.format_explanation() will preserve them instead of escaping
    newlines.  For other objects saferepr() is used first.
    """
    # reprlib appears to have a bug which means that if a string
    # contains a newline it gets escaped, however if an object has a
    # .__repr__() which contains newlines it does not get escaped.
    # However in either case we want to preserve the newline.
    replaces = [("\n", "\n~"), ("%", "%%")]
    if not isinstance(obj, str):
        obj = saferepr(obj, _get_maxsize_for_saferepr(util._config))
        replaces.append(("\\n", "\n~"))

    for r1, r2 in replaces:
        obj = obj.replace(r1, r2)

    return obj

