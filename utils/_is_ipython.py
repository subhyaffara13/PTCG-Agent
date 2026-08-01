
def _is_ipython(shell):
    """Is a shell instance an IPython shell?"""
    # shortcut, so we don't import IPython if we don't have to
    from sys import modules
    if 'IPython' not in modules:
        return False
    try:
        from IPython.core.interactiveshell import InteractiveShell
    except ImportError:
        # IPython < 0.11
        try:
            from IPython.iplib import InteractiveShell
        except ImportError:
            # Reaching this points means IPython has changed in a backward-incompatible way
            # that we don't know about. Warn?
            return False
    return isinstance(shell, InteractiveShell)

