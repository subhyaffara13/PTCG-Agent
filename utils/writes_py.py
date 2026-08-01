
def writes_py(nb, **kwargs):
    """DEPRECATED: use nbconvert"""
    _warn_format()
    return versions[3].writes_py(nb, **kwargs)

