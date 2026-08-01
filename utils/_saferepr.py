
def _saferepr(obj: object) -> str:
    r"""Get a safe repr of an object for assertion error messages.

    The assertion formatting (util.format_explanation()) requires
    newlines to be escaped since they are a special character for it.
    Normally assertion.util.format_explanation() does this but for a
    custom repr it is possible to contain one of the special escape
    sequences, especially '\n{' and '\n}' are likely to be present in
    JSON reprs.
    """
    if isinstance(obj, types.MethodType):
        # for bound methods, skip redundant <bound method ...> information
        return obj.__name__

    maxsize = _get_maxsize_for_saferepr(util._config)
    if not maxsize:
        return saferepr_unlimited(obj).replace("\n", "\\n")
    return saferepr(obj, maxsize=maxsize).replace("\n", "\\n")

