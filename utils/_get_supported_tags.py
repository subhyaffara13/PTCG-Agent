
def _get_supported_tags():
    # We calculate the supported tags only once, otherwise calling
    # this method on thousands of wheels takes seconds instead of
    # milliseconds.
    return {(t.interpreter, t.abi, t.platform) for t in sys_tags()}

