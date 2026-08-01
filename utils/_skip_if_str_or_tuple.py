
def _skip_if_str_or_tuple(window):
    """Handle `window` being a str or a tuple or an array-like.
    """
    if isinstance(window, str) or isinstance(window, tuple) or callable(window):
        return None
    else:
        return window

