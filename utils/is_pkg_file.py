
def is_pkg_file(fp):
    """Is this file inside a package dir (has __init__.py in parent)?"""
    return fp.parent.resolve() in PKG_DIRS

