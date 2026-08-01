
def has_jspi() -> bool:
    """
    Return true if jspi can be used.

    This requires both browser support and also WebAssembly
    to be in the correct state - i.e. that the javascript
    call into python was async not sync.

    :return: True if jspi can be used.
    :rtype: bool
    """
    try:
        from pyodide.ffi import can_run_sync, run_sync  # noqa: F401

        return bool(can_run_sync())
    except ImportError:
        return False


def has_jspi() -> bool:
    """
    Return true if jspi can be used.

    This requires both browser support and also WebAssembly
    to be in the correct state - i.e. that the javascript
    call into python was async not sync.

    :return: True if jspi can be used.
    :rtype: bool
    """
    try:
        from pyodide.ffi import can_run_sync, run_sync  # noqa: F401

        return bool(can_run_sync())
    except ImportError:
        return False

