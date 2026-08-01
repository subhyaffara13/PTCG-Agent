
def reads_py(s, **kwargs):
    """DEPRECATED: use nbconvert"""
    _warn_format()
    nbf, nbm, s = parse_py(s, **kwargs)
    if nbf in (2, 3):
        nb = versions[nbf].to_notebook_py(s, **kwargs)
    else:
        raise NBFormatError("Unsupported PY nbformat version: %i" % nbf)
    return nb

