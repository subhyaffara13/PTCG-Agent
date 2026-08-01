
def hide_warnings(filter_fn=lambda *args, **kwargs: True):
    """
    A context manager that temporarily suppresses warnings,
    using public API: https://docs.python.org/3/library/warnings.html#warnings.showwarning.

    Useful to hide warnings without mutating warnings module state, see:
    https://github.com/pytorch/pytorch/issues/128427#issuecomment-2161496162.

    NOTE: Warnings issued under this context will still be cached in the __warningregistry__
    and count towards the once/default rule. So you should NEVER use this on a user-land function.

    Filter must implement the showwarning API:
    def filter_fn(message, category, filename, lineno, file=None, line=None) -> bool:
        return True  # show this warning entry
    """
    prior = warnings.showwarning

    def _showwarning(*args, **kwargs):
        if filter_fn(*args, **kwargs):
            prior(*args, **kwargs)

    try:
        warnings.showwarning = _showwarning
        yield
    finally:
        warnings.showwarning = prior

