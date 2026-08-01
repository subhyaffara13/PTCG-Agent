
def may_xfail(func):
    if sys.platform.lower() == 'darwin' or os.name == 'nt':
        # sympy.utilities._compilation needs more testing on Windows and macOS
        # once those two platforms are reliably supported this xfail decorator
        # may be removed.
        return XFAIL(func)
    else:
        return func

