
def _have_cython() -> bool:
    """
    Return True if Cython can be imported.
    """
    cython_impl = 'Cython.Distutils.build_ext'
    try:
        # from (cython_impl) import build_ext
        __import__(cython_impl, fromlist=['build_ext']).build_ext
    except Exception:
        return False
    return True

