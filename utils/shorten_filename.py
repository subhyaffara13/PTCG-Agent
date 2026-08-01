
def shorten_filename(fn, *, base=None):
    """Shorten a source filepath, with the assumption that torch/ subdirectories don't need to be shown to user."""
    if base is None:
        base = os.path.dirname(os.path.dirname(__file__))
    # Truncate torch/foo.py to foo.py
    try:
        prefix = os.path.commonpath([fn, base])
    except ValueError:
        return fn
    else:
        return fn[len(prefix) + 1 :]

