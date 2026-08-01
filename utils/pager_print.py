
def pager_print(expr, **settings):
    """Prints expr using the pager, in pretty form.

    This invokes a pager command using pydoc. Lines are not wrapped
    automatically. This routine is meant to be used with a pager that allows
    sideways scrolling, like ``less -S``.

    Parameters are the same as for ``pretty_print``. If you wish to wrap lines,
    pass ``num_columns=None`` to auto-detect the width of the terminal.

    """
    from pydoc import pager
    from locale import getpreferredencoding
    if 'num_columns' not in settings:
        settings['num_columns'] = 500000  # disable line wrap
    pager(pretty(expr, **settings).encode(getpreferredencoding()))

