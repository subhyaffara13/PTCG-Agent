
def _build_option_description(k: str) -> str:
    """Builds a formatted description of a registered option and prints it"""
    o = _get_registered_option(k)
    d = _get_deprecated_option(k)

    s = f"{k} "

    if o.doc:
        s += "\n".join(o.doc.strip().split("\n"))
    else:
        s += "No description available."

    if o:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", FutureWarning)
            warnings.simplefilter("ignore", DeprecationWarning)
            s += f"\n    [default: {o.defval}] [currently: {get_option(k)}]"

    if d:
        rkey = d.rkey or ""
        s += "\n    (Deprecated"
        s += f", use `{rkey}` instead."
        s += ")"

    return s

