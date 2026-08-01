
def _get_implementation():
    if hasattr(sys, 'pypy_version_info'):
        return 'PyPy'
    else:
        return 'Python'

